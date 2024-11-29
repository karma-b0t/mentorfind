from typing import Optional, ForwardRef
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None
    language_code: Optional[str] = None

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля

class Chat(BaseModel):
    id: int
    type: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля

# Используем ForwardRef для ссылки на необъявленную модель Message
Message = ForwardRef('Message')

class CallbackQuery(BaseModel):
    id: str
    from_user: User = Field(..., alias='from')
    message: Optional[Message]  # Используем ForwardRef здесь
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля

class Location(BaseModel):
    longitude: float
    latitude: float

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля


class Document(BaseModel):
    file_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class LabeledPrice(BaseModel):
    label: str
    amount: int

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля


class PreCheckoutQuery(BaseModel):
    id: str
    from_user: User = Field(..., alias='from')
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[dict] = None

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля


class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[dict] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля


class Message(BaseModel):
    message_id: int
    from_user: Optional[User] = Field(None, alias='from')
    chat: Optional[Chat] = None
    date: int
    text: Optional[str] = None
    callback_query: Optional[CallbackQuery] = None
    location: Optional[Location] = None
    successful_payment: Optional[SuccessfulPayment] = None
    document: Optional[Document] = None
    # pre_checkout_query: Optional[PreCheckoutQuery] = None

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля


class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None

    class Config:
        extra = "ignore"  # Игнорировать неизвестные поля

# Объявляем ссылку на Message для разрешения ForwardRef
CallbackQuery.model_rebuild()
Message.model_rebuild()
