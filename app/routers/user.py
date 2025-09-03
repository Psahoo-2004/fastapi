from fastapi import Depends,HTTPException,APIRouter
from .. import schemas,oauth2
from sqlalchemy.orm import Session
from .. database import get_db
from .. model import User
from .. utils import hashed

router=APIRouter(
    prefix ="/users",
    tags=["User"]
)

@router.get("/",response_model=list[schemas.UserOut])
def get_user(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    return db.query(User).all()

@router.get("/{id}",response_model=schemas.UserOut)
def get_user_by_id(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    users=db.query(User).filter(User.id==id).first()
    if users:
        return users
    raise HTTPException(status_code=404,detail="User does not exists")

@router.post("/",response_model=schemas.UserOut)
def create_user(users:schemas.UserCreate,db:Session=Depends(get_db)):
    checkuser=db.query(User).filter(User.email==users.email).first()
    if checkuser:
        raise HTTPException(status_code=409,detail="email already exists")
    # hashed Password
    hashed_password=hashed(users.password)
    users.password=hashed_password

    CU=User(**users.model_dump())
    db.add(CU)
    db.commit()
    db.refresh(CU)
    return CU

@router.put("/{id}",response_model=schemas.Users)
def update_user(users:schemas.UserCreate,id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    UU=db.query(User).filter(User.id==id).first()
    if UU:
        for key,value in users.model_dump().items():
            setattr(UU,key,value)
        db.commit()
        db.refresh(UU)
        return UU
    raise HTTPException(status_code=404,detail="User does not found")

@router.delete("/{id}",response_model=schemas.Users)
def delete_user(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    DU=db.query(User).filter(User.id==id).first()
    if DU:
        db.delete(DU)
        db.commit()
        return DU
    raise HTTPException(status_code=404,detail="User does not found")