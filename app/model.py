from app.database import Base
from sqlalchemy import Integer,String,Column,Boolean,TIMESTAMP,ForeignKey, text,func
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__="post"
    id=Column(Integer,primary_key=True)
    title=Column(String,index=True,nullable=False)
    content=Column(String,index=True,nullable=False)
    published=Column(Boolean,server_default="True",index=True,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')) 
    owner_id=Column(Integer,ForeignKey("user.id",ondelete="cascade"),nullable=False)
    owner=relationship("User")

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,index=True,nullable=False,unique=True)
    password=Column(String,index=True,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default='now()',index=True,nullable=False)
    phone_number=Column(String) 

class Vote(Base):
    __tablename__="vote"
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key=True)