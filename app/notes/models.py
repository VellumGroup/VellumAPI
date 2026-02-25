from pydantic import BaseModel
from typing import Optional

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str

class NotePatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class InviteCollaborator(BaseModel):
    user_id: str
    role: str