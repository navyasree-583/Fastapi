import token_1
from fastapi import Depends, FastAPI, Response, HTTPException, status
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from typing import List
import models,schemas
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
import oauth2
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


#authentication 

# @app.post('/Login authentication')
# def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
#     staff = db.query(models.Staff).filter(models.Staff.email == request.username).first()
#     if not staff:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')

#     if not Hash.verify(staff.password,request.password): # if the password doesnt match 
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Incorrect password')
#     # generate a jwt token and return
    
#     access_token = token_1.create_access_token(data={"sub": staff.email})
#     return {"access_token": access_token, "token_type": "bearer"}
origins = [
 
    "http://localhost:4200",
    "http://localhost:8002",
    "https://localhost:4200",
    "http://localhost:4200/staffRegister"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#creating staff member
@app.post('/staff',response_model = schemas.ShowStaff)
def create_staff(request:schemas.Staffs,db:Session = Depends(get_db),get_current_user: schemas.Staffs= Depends(oauth2.get_current_user)):
    #, password = Hash.bcrypt(request.password), mobile = request.mobile

        new_staff = models.Staff( id = request.id,name = request.name, email = request.email, password = Hash.bcrypt(request.password), mobile = request.mobile)
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        db.close()
        return new_staff


#staff login
@app.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
         member =  db.query(models.Staff).filter(models.Staff.email == request.username).first()
         if not member:
             raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail ="Invalid Credentials")
     
         if not Hash.verify(member.password,request.password):
             raise HTTPException(status_code = 404 , detail ="Incorrect password")
     
         access_token = token_1.create_access_token(data={"sub": member.email})
         return {"access_token": access_token, "token_type" : "bearer"}

@app.get('/allStaff',response_model = List[schemas.ShowStaff])
def all_staff(db: Session= Depends(get_db),get_current_user: schemas.Staffs= Depends(oauth2.get_current_user)):
    staff = db.query(models.Staff).all()
    return staff

@app.get('/staff/{id}')
def staff_by_id(id,response:Response, db: Session = Depends(get_db),get_current_user: schemas.Staffs= Depends(oauth2.get_current_user)):
    staff = db.query(models.Staff).filter(models.Staff.id==id).first()
    if not staff:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail= f'Staff with the id {id} is not available')
    return staff

@app.put('/staff/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Staffs, db:Session = Depends(get_db),get_current_user: schemas.Staffs= Depends(oauth2.get_current_user)):  # request Schemas.Blog we write because v get schemas of Blog i.e. title and body
    staff = db.query(models.Staff).filter(models.Staff.id == id)

    if not staff.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Staff with id {id} not found")
    staff.update({'name':request.name , 'email':request.email, 'mobile':request.mobile, 'password':request.password})

    db.commit()
    return 'updated'

@app.delete('/staff/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db),get_current_user: schemas.Staffs= Depends(oauth2.get_current_user)):
    staff=db.query(models.Staff).filter(models.Staff.id==id)
    if not staff.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"staff with id {id} not found")
    
    staff.delete(synchronize_session = False)

    db.commit()
    return 'deleted successfully'
