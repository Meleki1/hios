from typing import Protocol
from urllib.parse import urljoin, urlparse

from hios.capabilities.pest_control.referral.models import (
    PestControlContactSubmissionRequest,
    PestControlContactSubmissionResult,
)

_PLAYWRIGHT_MISSING = (
    "Automated form submission is unavailable on this server "
    "(browser automation is not set up). "
    "Please use the partner contact link to reach them directly."
)

_PLAYWRIGHT_BROWSERS_MISSING = (
    "Automated form submission is unavailable because Chromium "
    "is not installed for browser automation. "
    "Please use the partner contact link to reach them directly."
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
        except ImportError:
            return PestControlContactSubmissionResult(
                success=False,
                detail=_PLAYWRIGHT_MISSING,
            )

        message_body = (
            f"Service address: {request.address}\n"
            f"Problem: {request.problem_description}\n"
            f"Urgency: {request.urgency}\n"
            f"Submitted via HIOS on behalf of the homeowner."
        )

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(
                    headless=self._headless,
                )
                try:
                    page = await browser.new_page()
                    await _open_contact_page(page, request.contact_url)

                    await _fill_first_matching(
                        page,
                        [
                            'input[name="your-name"]',
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
                            'input[name="your-email"]',
                            'input[name="email"]',
                            'input[id*="email" i]',
                        ],
                        request.email,
                    )
                    await _fill_first_matching(
                        page,
                        [
                            'input[type="tel"]',
                            'input[name="your-phone"]',
                            'input[name="phone"]',
                            'input[id*="phone" i]',
                            'input[placeholder*="phone" i]',
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
                            'textarea[name="your-message"]',
                            'textarea[name="message"]',
                            'textarea[id*="message" i]',
                            'textarea[name="comments"]',
                            'textarea[placeholder*="message" i]',
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
                            'input[type="submit"]',
                            'button[type="submit"]',
                            'button:has-text("Submit")',
                            'button:has-text("Send")',
                            'button:has-text("Send Message")',
                            ".wpcf7-submit",
                        ],
                    )

                    if not submitted:
                        return PestControlContactSubmissionResult(
                            success=False,
                            detail=(
                                "Opened the partner contact page but "
                                "could not submit the form automatically."
                            ),
                        )

                    await page.wait_for_timeout(2000)

                    return PestControlContactSubmissionResult(
                        success=True,
                        detail=(
                            "Contact request submitted to the pest "
                            "control partner website."
                        ),
                    )
                finally:
                    await browser.close()
        except Exception as exc:
            error_text = str(exc).lower()
            if "executable doesn't exist" in error_text or (
                "browser" in error_text and "install" in error_text
            ):
                return PestControlContactSubmissionResult(
                    success=False,
                    detail=_PLAYWRIGHT_BROWSERS_MISSING,
                )
            return PestControlContactSubmissionResult(
                success=False,
                detail=(
                    "Something went wrong while submitting the "
                    "partner contact form."
                ),
            )


async def _open_contact_page(page, contact_url: str) -> None:
    await page.goto(contact_url, wait_until="domcontentloaded")

    has_form = await page.locator("form").count() > 0
    if has_form:
        return

    contact_link = page.locator(
        'a[href*="contact" i]',
    ).first
    if await contact_link.count() > 0:
        await contact_link.click(timeout=3000)
        await page.wait_for_load_state("domcontentloaded")
        return

    parsed = urlparse(contact_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    for path in ("/contact/", "/contact-us/", "/contact"):
        candidate = urljoin(base, path)
        if candidate.rstrip("/") == contact_url.rstrip("/"):
            continue
        await page.goto(candidate, wait_until="domcontentloaded")
        if await page.locator("form").count() > 0:
            return


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
