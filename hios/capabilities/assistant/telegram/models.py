from pydantic import BaseModel, Field


class TelegramChat(BaseModel):
    id: int


class TelegramUser(BaseModel):
    id: int


class TelegramMessage(BaseModel):
    message_id: int
    from_: TelegramUser = Field(alias="from")
    chat: TelegramChat
    text: str | None = None

    model_config = {
        "populate_by_name": True,
    }


class TelegramUpdate(BaseModel):
    update_id: int
    message: TelegramMessage | None = None