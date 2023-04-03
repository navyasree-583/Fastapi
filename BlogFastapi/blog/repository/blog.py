from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, database, models
from sqlalchemy.orm import Session




def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request:schemas.Blog, db:Session):
    new_blog = models.Blog(title = request.title, body = request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int,db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.delete(synchronize_session = False)

    db.commit()
    return 'done'

def update(id:int,request:schemas.Blog, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update({'title':request.title , 'body':request.body})

    db.commit()
    return 'updated'

def show(id:int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}
        # sending response by raising http exception
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail= f'Blog with the id {id} is not available')
    return blog