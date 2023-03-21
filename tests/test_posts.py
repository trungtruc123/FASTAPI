import pytest
from app import schemas
from app import models


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # print(res.json())
    # print(posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.context == test_posts[0].context
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, context, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, context, published):
    res = authorized_client.post(
        "/posts/createpost", json={"title": title, "context": context, "published": published})
    # print(res.json().get("message"))
    # created_post = schemas.PostCreate(**res.json().get("message"))
    created_post = models.Post(**res.json().get("message"))
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.context == context
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/createpost", json={"title": "arbitrary title", "context": "aasdfjasdf"})

    created_post = models.Post(**res.json().get("message"))
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.context == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/createpost", json={"title": "arbitrary title", "context": "aasdfjasdf"})
    assert res.status_code == 401
