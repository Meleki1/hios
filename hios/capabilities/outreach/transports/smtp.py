import asyncio
import smtplib
from email.message import EmailMessage
from hios.capabilities.outreach.channels.email import EmailTransport

class SMTPEmailTransport(EmailTransport):

    def __init__(
        self,
        *,
        host: str,
        port: int,
        username: str,
        password: str,
        sender: str,
        use_tls: bool = True,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._sender = sender
        self._use_tls = use_tls

    async def send(
        self,
        *,
        recipient: str,
        subject: str,
        message: str,
    ) -> str:

        email = EmailMessage()
        email["From"] = self._sender
        email["To"] = recipient
        email["Subject"] = subject
        email.set_content(message)

        def send_sync() -> str:

            if self._port == 465:
                with smtplib.SMTP_SSL(
                    self._host,
                    self._port,
                ) as server:

                    server.login(
                        self._username,
                        self._password,
                    )

                    server.send_message(email)

            else:
                with smtplib.SMTP(
                    self._host,
                    self._port,
                ) as server:

                    if self._use_tls:
                        server.starttls()

                    server.login(
                        self._username,
                        self._password,
                    )

                    server.send_message(email)

            return "smtp-delivered"

        return await asyncio.to_thread(
            send_sync,
        )