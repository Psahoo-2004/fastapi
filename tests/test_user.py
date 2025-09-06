import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_create_user(client):
    res=client.post("/users",json={"email":"pratyush@gmail.com","password":"p123"})
    new_user=schemas.UserOut(**res.json())
    assert new_user.email == "pratyush@gmail.com"
    assert res.status_code == 200

def test_login_user(client,test_user):
    res=client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    login_response=schemas.Token(**res.json())
    payload=jwt.decode(login_response.access_token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    id=payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type =="bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@gmail.com','password@1234',401),
    ('hasheduser1@gmail.com','wrongpassword',401),
    ('wrongemail@gamil.com','wrongpassword',401),
    (None,'password@1234',422),
    ('hasheduser1@gamil.com',None,422)
])
def test_incorrect_login(client,test_user,email,password,status_code):
    data = {}
    if email is not None:
        data["username"] = email
    if password is not None:
        data["password"] = password
    res=client.post("/login",data=data)
    assert res.status_code == status_code


