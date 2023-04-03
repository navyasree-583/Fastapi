import token_3
from fastapi import Depends, FastAPI, Response, HTTPException, status
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from typing import List
import models,schemas
from hashing import Hash

models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


#creating Book
@app.post('/Book',response_model = schemas.ShowBooks)
def create_book(request:schemas.Books,db:Session = Depends(get_db)):
    new_book = models.Book( id= request.id, title = request.title, author = request.author, price = request.price, quantity = request.quantity)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    return new_book

@app.get('/All Books',response_model = List[schemas.ShowBooks])
def all_Books(db: Session= Depends(get_db)):
    book = db.query(models.Book).all()
    return book

@app.get('/Book/{id}')
def book_by_id(id,db: Session= Depends(get_db)):
    book= db.query(models.Book).filter(models.Book.id==id).first()
    if not book:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not available")
    return book

@app.put('/Book/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Books, db:Session = Depends(get_db)):  # request Schemas.Blog we write because v get schemas of Blog i.e. title and body
    book = db.query(models.Book).filter(models.Book.id == id)

    if not book.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    book.update({'id':request.id, 'title':request.title , 'author':request.author, 'price':request.price, 'quantity':request.quantity})

    db.commit()
    return 'updated'

@app.delete('/Book/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db)):
    book=db.query(models.Book).filter(models.Book.id==id)
    if not book.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    
    book.delete(synchronize_session = False)

    db.commit()
    return 'deleted successfully'

