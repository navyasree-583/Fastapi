from typing import Optional
from pydantic import BaseModel 

class Staffs(BaseModel):
    id:int
    name: str
    email:str
    mobile: int
    password:str

class ShowStaff(BaseModel):
    id:int
    name:str
    email:str
    mobile: int
    password:str

    class Config():
        orm_mode=True

class login(BaseModel):
    username:str
    password:str
    class config():
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
   