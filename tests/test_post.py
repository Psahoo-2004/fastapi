from typing import List
from app import schemas
import pytest

def test_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map=map(validate,res.json())
    posts_list=list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client,test_posts):
    res=client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client,test_posts):
    res=client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 404 # change this one from 401

def test_get_one_post_not_exits(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_posts(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/{test_posts[0].id}")
    post =schemas.PostOut(**res.json())
    print(post)
    # assert res.status_code == 200
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content
    assert post.post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published",[
    ("awesom new title 1","awesom new content 1",True),
    ("awesom new title 2","awesom new content 2",True),
    ("awesom new title 3","awesom new content 3",False),
    ("awesom new title 4","awesom new content 4",False)
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res=authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    create_post=schemas.Posts(**res.json())
    assert res.status_code == 200
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published

def test_create_post_default_published_true(authorized_client,test_user,test_posts):
    res=authorized_client.post("/posts/",json={"title":"arbritary title","content":"arbritary content"})
    create_post=schemas.Posts(**res.json())
    assert res.status_code == 200
    assert create_post.title == "arbritary title"
    assert create_post.content == "arbritary content"
    assert create_post.published == True

def test_unauthorized_user_create_posts(client,test_user,test_posts):
    res=client.post("/posts/",json={"title":"arbritary title","content":"arbritary content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_posts(client,test_user,test_posts):
    res=client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_user,test_posts):
    res=authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

def test_delete_post_non_exist(authorized_client,test_user,test_posts):
    res=authorized_client.delete(f"/posts/8888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts,test_user):
    res=authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client,test_user,test_posts):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res=authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post=schemas.Posts(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client,test_user,test_user2,test_posts):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res=authorized_client.put(f"/posts/{test_posts[3].id}",json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_posts,test_user):
    res=client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client,test_user,test_posts):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res=authorized_client.put(f"/posts/8888",json=data)
    assert res.status_code == 404