from app import oauth2
from .. import schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends,HTTPException,APIRouter
from .. database import get_db
from .. model import Post,Vote

router=APIRouter(
    prefix="/posts",
    tags=['Post']
)

@router.get("/",response_model=list[schemas.PostOut])
def get_post(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # posts=db.query(Post).filter(Post.owner_id==current_user.id)
    results=db.query(Post,func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == Post.id,isouter=True).group_by(Post.id).all()
    print(results)
    if not results:
        raise HTTPException(status_code=404,detail="Post not found")
    return [
    {"post": post, "votes": votes} 
    for post, votes in results
    ]

@router.post("/",response_model=schemas.Posts)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    CP=Post(owner_id=current_user.id,**post.model_dump())
    print(CP)
    db.add(CP)
    db.commit()
    db.refresh(CP)
    return CP

@router.get("/{id}",response_model=schemas.PostOut)
def get_post_by_id(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # QP=db.query(Post).filter(Post.id==id).first()
    QP=db.query(Post,func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == Post.id,isouter=True).group_by(Post.id).filter(Post.id==id).first()
    if not QP:
        raise HTTPException(status_code=404,detail="Post not found")
    post, votes =QP
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    return {"post": post, "votes": votes} 
    


@router.put("/{id}",response_model=schemas.Posts)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    UP=db.query(Post).filter(Post.id==id).first()
    if not UP:
        raise HTTPException(status_code=404,detail="Post Not found")
    if UP.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    
    for key,value in post.model_dump().items():
        setattr(UP,key,value)
    db.commit()
    db.refresh(UP)
    return UP

@router.delete("/{id}",response_model=schemas.Posts)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    DP=db.query(Post).filter(Post.id==id).first()
    if not DP:
        raise HTTPException(status_code=404,detail="Post not found")
    if DP.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    db.delete(DP)
    db.commit()
    return DP
    # raise HTTPException(status_code=404,detail="Invalid Index")