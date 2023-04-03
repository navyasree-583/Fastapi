from typing import Optional
from pydantic import BaseModel 

class Books(BaseModel):
    id:int
    title: str
    author:str
    price: int
    quantity:str

class ShowBooks(BaseModel):
    id:int
    title: str
    author:str
    price: int
    quantity:str

    class Config():
        orm_mode=True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
   