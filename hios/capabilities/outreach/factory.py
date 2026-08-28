from hios.capabilities.outreach.default_capability import (
    DefaultOutreachCapability,
)
from hios.capabilities.outreach.channels.email import (
    EmailOutreachProvider,
)
from hios.capabilities.outreach.transports.smtp import (
    SMTPEmailTransport,
)
from hios.core.config import Settings


def build_outreach_capability(
    settings: Settings,
) -> DefaultOutreachCapability:

    email_transport = SMTPEmailTransport(
        host=settings.email_host,
        port=settings.email_port,
        username=settings.email_username,
        password=settings.email_password,
        sender=settings.email_from,
    )

    email_provider = EmailOutreachProvider(
        transport=email_transport,
    )

    return DefaultOutreachCapability(
        email_provider=email_provider,
    )