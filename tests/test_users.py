from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get('message') == 'Hello Tran Trung Truc'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "trungtruc21@gmail.com", "password": "truc123"})

    res_out = schemas.UserShow(**res.json())
    assert res_out.email == "trungtruc21@gmail.com"
    assert res.status_code == 201
