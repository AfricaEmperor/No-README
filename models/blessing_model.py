
from pydantic import BaseModel
from typing import Optional

class Blessing(BaseModel):
    id: str
    title: str
    description: str
    agent_id: str
    qr_code_url: Optional[str] = None
