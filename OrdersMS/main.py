import token_4
from fastapi import Depends, FastAPI, Response, HTTPException, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import schemas
import models
from hashing import Hash
from typing import List
from fastapi.security import OAuth2PasswordRequestForm


models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

#creating  member
@app.post('/order',response_model = schemas.ShowOrder)
def create_order(request:schemas.Order,db:Session = Depends(get_db)):
    #, password = Hash.bcrypt(request.password), mobile = request.mobile ,get_current_user: schemas.Order= Depends(oauth2.get_current_user)
    new_ord = models.Orders( id= request.id,title = request.title, author = request.author, quantity = request.quantity, price = request.price)
    db.add(new_ord)
    db.commit()
    db.refresh(new_ord)
    db.close()
    return new_ord

@app.get('/all orders',response_model = List[schemas.ShowOrder])
def all_orders(db: Session = Depends(get_db)):
    all_orders = db.query(models.Orders).all()
    return all_orders

@app.get('/order/{id}')
def order_by_id(id,db: Session= Depends(get_db)):
    order_by_id = db.query(models.Orders).filter(models.Orders.id==id).first()
    return order_by_id

@app.put('/order/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Order, db:Session = Depends(get_db)):  # request Schemas.Blog we write because v get schemas of Blog i.e. title and body
    order = db.query(models.Orders).filter(models.Orders.id == id)

    if not order.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    order.update({'id':request.id,'title':request.title , 'author':request.author, 'quantity':request.quantity, 'price': request.price})

    db.commit()
    return 'updated'

@app.delete('/order/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db)):
    order=db.query(models.Orders).filter(models.Orders.id==id)
    if not order.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"order with id {id} not found")
    
    order.delete(synchronize_session = False)

    db.commit()
    return 'deleted successfully'


