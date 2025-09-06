import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app import model

SQLALCHAMY_DATABASE_URL=f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine=create_engine(SQLALCHAMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
# Base=declarative_base()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db 
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data={"email":"pratyush@gmail.com",
               "password":"p123"
    }
    res=client.post("/users/",json=user_data)
    assert res.status_code ==  200
    new_user=res.json()
    new_user['password'] = user_data['password']
    print(new_user)
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id':test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    post_data=[{
        "title":"first title",
        "content":"first content",
        "owner_id":test_user['id']
    },{
        "title":"second title",
        "content":"second content",
        "owner_id":test_user['id']
    },{
        "title":"3rd title",
        "content":"3rd content",
        "owner_id":test_user['id']
    },{
        "title":"4th title",
        "content":"4rth content",
        "owner_id":test_user2['id']
    }
    ]
    
    def create_post_model(post):
        return model.Post(**post)
    
    post_map= map(create_post_model,post_data)
    posts=list(post_map)

    session.add_all(posts)
    session.commit()  
    # post=session.query(model.Post).all()
    return posts

@pytest.fixture
def test_user2(client):
    user_data={"email":"pratyush123@gmail.com",
               "password":"p123"
    }
    res=client.post("/users/",json=user_data)
    assert res.status_code ==  200
    new_user=res.json()
    new_user['password'] = user_data['password']
    print(new_user)
    return new_user