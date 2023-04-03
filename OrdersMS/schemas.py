from typing import Optional
from pydantic import BaseModel 

class Order(BaseModel):
    id:int
    title: str
    author:str
    quantity: int
    price:int

class ShowOrder(BaseModel):
    id:int
    title: str
    author:str
    quantity: int
    price:int

    class Config():
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
   