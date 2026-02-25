from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ConvertGuest(BaseModel):
    guest_id: str
    email: str
    password: str