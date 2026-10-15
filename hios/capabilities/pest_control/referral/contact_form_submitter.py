from typing import Protocol

from hios.capabilities.pest_control.referral.models import (
    PestControlContactSubmissionRequest,
    PestControlContactSubmissionResult,
)

# Veritex (default partner URL) uses ASP.NET WebForms field ids on the homepage.
_VERITEX_HOMEOWNER_FORM = {
    "name": "#ContentPlaceHolder1_txtname",
    "email": "#ContentPlaceHolder1_txtemail",
    "phone": "#ContentPlaceHolder1_txtphone",
    "address": "#ContentPlaceHolder1_txtaddress",
    "message": "#ContentPlaceHolder1_txtmessage",
    "urgency": "#ContentPlaceHolder1_txturgency",
    "submit": "#ContentPlaceHolder1_btnsubmit",
}


class PestControlContactFormSubmitter(Protocol):
    async def submit(
        self,
        request: PestControlContactSubmissionRequest,
    ) -> PestControlContactSubmissionResult: ...


class PlaywrightPestControlContactFormSubmitter:
    """
    Fills a pest-control partner "Contact us" form via Playwright.

    Replace `contact_url` in settings with the real site. Selectors
    are best-effort common patterns; adjust when wiring a specific site.
    """

    def __init__(
        self,
        *,
        headless: bool = True,
    ) -> None:
        self._headless = headless

    async def submit(
        self,
        request: PestControlContactSubmissionRequest,
    ) -> PestControlContactSubmissionResult:
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            return PestControlContactSubmissionResult(
                success=False,
                detail=(
                    "Playwright is not installed. "
                    "Add the browser extra: uv sync --extra browser"
                ),
            )

        message_body = (
            f"Problem: {request.problem_description}\n"
            f"Urgency: {request.urgency}\n"
            f"Submitted via HIOS on behalf of the homeowner."
        )

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=self._headless,
            )
            try:
                page = await browser.new_page()
                await page.goto(
                    request.contact_url,
                    wait_until="commit",
                    timeout=60_000,
                )
                await _wait_for_contact_form(page)

                await _fill_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["name"],
                        'input[name="name"]',
                        'input[id*="name" i]',
                        'input[placeholder*="name" i]',
                    ],
                    request.full_name,
                )
                await _fill_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["email"],
                        'input[type="email"]',
                        'input[name="email"]',
                        'input[id*="email" i]',
                    ],
                    request.email,
                )
                await _fill_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["phone"],
                        'input[type="tel"]',
                        'input[name="phone"]',
                        'input[id*="phone" i]',
                    ],
                    request.phone,
                )
                await _fill_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["address"],
                        'input[name="address"]',
                        'textarea[name="address"]',
                        'input[id*="address" i]',
                    ],
                    request.address,
                )
                await _fill_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["message"],
                        'textarea[name="message"]',
                        'textarea[id*="message" i]',
                        'textarea[name="comments"]',
                    ],
                    message_body,
                )
                await _fill_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["urgency"],
                        'select[name*="urgent" i]',
                        'input[name*="urgent" i]',
                    ],
                    request.urgency,
                )

                submitted = await _click_first_matching(
                    page,
                    [
                        _VERITEX_HOMEOWNER_FORM["submit"],
                        'button:has-text("Submit Request")',
                        'button[type="submit"]',
                        'input[type="submit"]',
                        'button:has-text("Submit")',
                        'button:has-text("Send")',
                    ],
                )

                if not submitted:
                    return PestControlContactSubmissionResult(
                        success=False,
                        detail=(
                            "Opened contact page but could not find "
                            "a submit control. Update selectors for "
                            "your partner site."
                        ),
                    )

                await page.wait_for_timeout(1500)

                return PestControlContactSubmissionResult(
                    success=True,
                    detail=(
                        "Contact request submitted to the pest "
                        "control partner website."
                    ),
                )
            finally:
                await browser.close()


def urgency_select_keywords(urgency: str) -> tuple[str, ...]:
    """Map HIOS severity labels to likely partner dropdown option text."""
    normalized = urgency.strip().lower()
    mapping: dict[str, tuple[str, ...]] = {
        "high": ("emergency", "very urgent", "same day"),
        "medium": ("moderate", "2-3"),
        "low": ("not urgent",),
        "critical": ("emergency", "same day"),
        "severe": ("very urgent", "emergency"),
    }
    if normalized in mapping:
        return mapping[normalized]
    if normalized:
        return (normalized,)
    return ("moderate",)


async def _wait_for_contact_form(page) -> None:
    try:
        await page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception:
        pass
    await page.locator(
        f"{_VERITEX_HOMEOWNER_FORM['name']}, "
        'input[name="name"], input[id*="name" i], input[placeholder*="name" i]'
    ).first.wait_for(state="visible", timeout=30_000)


async def _fill_first_matching(
    page,
    selectors: list[str],
    value: str,
) -> None:
    for selector in selectors:
        locator = page.locator(selector).first
        if await locator.count() == 0:
            continue
        try:
            tag = await locator.evaluate("el => el.tagName")
            if tag == "SELECT":
                await _select_option_matching(locator, value)
                return
            await locator.fill(value, timeout=2000)
            return
        except Exception:
            continue


async def _select_option_matching(locator, urgency: str) -> None:
    options: list[dict[str, str]] = await locator.locator("option").evaluate_all(
        """els => els.map(el => ({
            value: el.value || '',
            label: (el.textContent || '').trim(),
        }))"""
    )
    candidates = [
        opt
        for opt in options
        if opt["value"] or (opt["label"] and opt["label"] != "How urgent is it?")
    ]
    keywords = urgency_select_keywords(urgency)
    for keyword in keywords:
        needle = keyword.lower()
        for opt in candidates:
            hay = f"{opt['value']} {opt['label']}".lower()
            if needle in hay:
                if opt["value"]:
                    await locator.select_option(value=opt["value"], timeout=2000)
                else:
                    await locator.select_option(label=opt["label"], timeout=2000)
                return
    if candidates:
        first = candidates[0]
        if first["value"]:
            await locator.select_option(value=first["value"], timeout=2000)
        else:
            await locator.select_option(label=first["label"], timeout=2000)


async def _click_first_matching(
    page,
    selectors: list[str],
) -> bool:
    for selector in selectors:
        locator = page.locator(selector).first
        if await locator.count() == 0:
            continue
        try:
            await locator.click(timeout=2000)
            return True
        except Exception:
            continue
    return False
