from fastapi import APIRouter,Depends,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from app.routers import user
from .. import database,schemas,model,utils,oauth2

router=APIRouter(
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def user_login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    
    UL=db.query(model.User).filter( model.User.email == user_credential.username).first()
    if not UL:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    verify1=utils.verify(user_credential.password , UL.password)
    if not verify1:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":UL.id})
    return {"access_token":access_token,"token_type":"bearer"}
    # return {"token":"example token"}