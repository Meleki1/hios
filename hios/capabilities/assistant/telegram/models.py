from pydantic import BaseModel, Field


class TelegramChat(BaseModel):
    id: int


class TelegramUser(BaseModel):
    id: int


class TelegramPhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None = None

class TelegramMessage(BaseModel):
    message_id: int
    from_: TelegramUser = Field(alias="from")
    chat: TelegramChat
    text: str | None = None

    caption: str | None = None
    photo: list[TelegramPhotoSize] | None = None

    model_config = {
        "populate_by_name": True,
    }


class TelegramUpdate(BaseModel):
    update_id: int
    message: TelegramMessage | None = None