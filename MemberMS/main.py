import token_2
from fastapi import Depends, FastAPI, Response, HTTPException, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import schemas
import models
from hashing import Hash
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
import oauth2
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

origins = [
 
    "http://localhost:4200",
    "http://localhost:8000",
    "https://localhost:4200",
    "http://localhost:4200/signup"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#creating  member
@app.post('/member',response_model = schemas.ShowUser)
def create_member(request:schemas.User,db:Session = Depends(get_db),get_current_user: schemas.User= Depends(oauth2.get_current_user)):
    #, password = Hash.bcrypt(request.password), mobile = request.mobile
    new_mem = models.Member( id= request.id,name = request.name, email = request.email, password = Hash.bcrypt(request.password), mobile = request.mobile)
    db.add(new_mem)
    db.commit()
    db.refresh(new_mem)
    db.close()
    return new_mem 

# member login
@app.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:SessionLocal = Depends(get_db)):
     member =  db.query(models.Member).filter(models.Member.email == request.username).first()
     if not member:
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail ="Invalid Credentials")
     
     if not Hash.verify(member.password,request.password):
          raise HTTPException(status_code = 404 , detail ="Incorrect password")
     
     access_token = token_2.create_access_token(data={"sub": member.email})
     return {"access_token": access_token, "token_type" : "bearer"}


@app.get('/all members',response_model = List[schemas.ShowUser])
def all_members(db: Session = Depends(get_db),get_current_user: schemas.User= Depends(oauth2.get_current_user)):
    all_members = db.query(models.Member).all()
    return all_members


@app.get('/member/{id}')
def member_by_id(id,db: Session= Depends(get_db),get_current_user: schemas.User= Depends(oauth2.get_current_user)):
    member_by_id = db.query(models.Member).filter(models.Member.id==id).first()
    return member_by_id

@app.put('/member/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.User, db:Session = Depends(get_db),get_current_user: schemas.User= Depends(oauth2.get_current_user)):  # request Schemas.Blog we write because v get schemas of Blog i.e. title and body
    user = db.query(models.Member).filter(models.Member.id == id)

    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Member with id {id} not found")
    user.update({'id':request.id,'name':request.name , 'email':request.email, 'mobile':request.mobile, 'password': request.password})

    db.commit()
    return 'updated'

@app.delete('/member/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db),get_current_user: schemas.User= Depends(oauth2.get_current_user)):
    member=db.query(models.Member).filter(models.Member.id==id)
    if not member.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"member with id {id} not found")
    
    member.delete(synchronize_session = False)

    db.commit()
    return 'deleted successfully'
