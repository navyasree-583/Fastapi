from typing import Optional
from pydantic import BaseModel 

class User(BaseModel):
    id:int
    name: str
    email:str
    mobile: str
    password:str

class ShowUser(BaseModel):
    id:int
    name:str
    email:str
    mobile: str
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
   