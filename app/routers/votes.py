from fastapi import APIRouter,Response,Depends,HTTPException
from .. import schemas,model,oauth2,utils
from sqlalchemy.orm import session
from ..database import get_db

router=APIRouter(
    #prefix="/votes",
    tags=["Vote"]
)

@router.post("/votes")
def vote(vote:schemas.Vote,db:session=Depends(get_db),cuerrent_user:int=Depends(oauth2.get_current_user)):
    vote_query=db.query(model.Vote).filter(model.Vote.post_id == vote.post_id,model.Vote.user_id == cuerrent_user.id)
    found_vote=vote_query.first()
    if  not (db.query(model.Vote).filter(model.Vote.post_id!=cuerrent_user.id).first()):
        raise HTTPException(status_code=404,detail="Not Found")
    if vote.dir ==1:
        if found_vote:
            raise HTTPException(status_code=409,detail="Vote already exists")
        new_vote=model.Vote(post_id =vote.post_id,user_id=cuerrent_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404,detail="Vote doesnot exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}
    