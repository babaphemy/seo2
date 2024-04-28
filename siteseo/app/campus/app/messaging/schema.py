from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class MailerDto(BaseModel):
    recipients: list[EmailStr]
    subject: str
    message: str
    create_at: datetime
    is_html: bool
class Message(BaseModel):
    id: Optional[int] = 0
    sender: str
    recipient: str
    content: str
