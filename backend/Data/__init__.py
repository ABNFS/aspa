from pydantic import BaseModel
from typing import Optional


class DefaultMessageData(BaseModel):
    code: Optional[str]
    text: Optional[str]