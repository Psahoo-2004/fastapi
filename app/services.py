# from app.model import Post,User
# from sqlalchemy.orm import Session
# from app.schemas import PostCreate,UserCreate


# # POST

# def create_post(db:Session,post:PostCreate):
#     PO=Post(owner_id=1,**post.model_dump())
#     db.add(PO)
#     db.commit()
#     db.refresh(PO)
#     return PO

# def get_post(db:Session):
#     return db.query(Post).all()

# def get_post_by_id(db:Session,id:int):
#     return db.query(Post).filter(Post.id==id).first()

# def update_post(db:Session,post:PostCreate,id:int):
#     UP=db.query(Post).filter(Post.id==id).first()
#     if UP:
#         for key,value in post.model_dump().items():
#             setattr(UP,key,value)
#         db.commit()
#         db.refresh(UP)
#     return UP

# def delete_post(db:Session,id:int):
#     DP=db.query(Post).filter(Post.id==id).first()
#     if DP:
#         db.delete(DP)
#         db.commit()
#     return DP


# # User

# def get_user(db:Session):
#     return db.query(User).all()

# def create_user(user:UserCreate,db:Session):
#     CU=User(**user.model_dump())
#     db.add(CU)
#     db.commit()
#     db.refresh(CU)
#     return CU

# def update_user(user:UserCreate,db:Session,id:int):
#     UU=db.query(User).filter(User.id==id).first()
#     if UU:
#         for key,value in user.model_dump().items():
#             setattr(UU,key,value)
#         db.commit()
#         db.refresh(UU)
#     return UU

# def delete_user(db:Session,id:int):
#     DU=db.query(User).filter(User.id==id).first()
#     if DU:
#         db.delete(DU)
#         db.commit()
#     return DU