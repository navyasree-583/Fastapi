from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, database, oauth2
from blog.repository import blog
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = '/blog',
    tags = ['Blogs']
)
get_db=database.get_db

@router.get('/', response_model = List[schemas.ShowBlog])
def all(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request,db)

@router.delete('/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
   return blog.destroy(id,db)

@router.put('/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):  # request Schemas.Blog we write because v get schemas of Blog i.e. title and body
    return blog.update(id,request,db)


# @app.get('/blog', response_model = List[schemas.ShowBlog], tags=['blogs'])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


@router.get('/{id}', status_code = 200, response_model=schemas.ShowBlog) # in FastAPI pydantic models are called schemas
def show(id,  db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id,db)







     
