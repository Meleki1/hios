from typing import Protocol

from hios.capabilities.pest_control.referral.models import (
    PestControlContactSubmissionRequest,
    PestControlContactSubmissionResult,
)


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
        except ImportError as exc:
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
                    wait_until="domcontentloaded",
                )

                await _fill_first_matching(
                    page,
                    [
                        'input[name="name"]',
                        'input[id*="name" i]',
                        'input[placeholder*="name" i]',
                    ],
                    request.full_name,
                )
                await _fill_first_matching(
                    page,
                    [
                        'input[type="email"]',
                        'input[name="email"]',
                        'input[id*="email" i]',
                    ],
                    request.email,
                )
                await _fill_first_matching(
                    page,
                    [
                        'input[type="tel"]',
                        'input[name="phone"]',
                        'input[id*="phone" i]',
                    ],
                    request.phone,
                )
                await _fill_first_matching(
                    page,
                    [
                        'input[name="address"]',
                        'textarea[name="address"]',
                        'input[id*="address" i]',
                    ],
                    request.address,
                )
                await _fill_first_matching(
                    page,
                    [
                        'textarea[name="message"]',
                        'textarea[id*="message" i]',
                        'textarea[name="comments"]',
                    ],
                    message_body,
                )
                await _fill_first_matching(
                    page,
                    [
                        'select[name*="urgent" i]',
                        'input[name*="urgent" i]',
                    ],
                    request.urgency,
                )

                submitted = await _click_first_matching(
                    page,
                    [
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
            await locator.fill(value, timeout=2000)
            return
        except Exception:
            continue


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
