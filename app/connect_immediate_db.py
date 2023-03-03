from fastapi import FastAPI, HTTPException, status, Response
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# my_post = [{"title": "title 1", "context": "context 1", "id": 1},
#            {"title": "title 2", "context": "context 2", "id": 2},
#            {"title": "title 3", "context": "context 3", "id": 3}]


# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p
#
#
# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p["id"] == id:
#             return i


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="firstapi", user="postgres", password="1",
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Connect successful!")
        break
    except Exception as err:
        print(" Error connect to database!")
        print(f"Error: {err}")
        time.sleep(3)


class Post(BaseModel):
    title: str
    context: str
    published: bool = True
    # rating: Optional[int] = 4


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_post():
    cur.execute(""" SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"message": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # new_post = post.dict()
    # id = randrange(0, 10000000)
    # new_post["id"] = id
    # my_post.append(new_post)
    """
    To avoid SQl ejection : use (%s, %s, %s), (arg.a, arg.b, arg.c)
    :param post:
    :return:
    """
    cur.execute(""" INSERT INTO posts (title, context, published) VALUES (%s, %s, %s) RETURNING *""",
                (post.title, post.context, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"message": new_post}


# @app.get("/posts/latest")
# def get_post_latest():
#     post_latest = my_post[len(my_post) - 1]
#     return {"message": post_latest}


@app.get("/posts/{id}")
def get_one_post(id: int):
    # find post that my_post["id"] = id
    # post = find_post(id)
    cur.execute(""" SElECT * FROM posts WHERE id = %s """, (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} not found.")
    return {"message": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    # find index that my_post["id"] = id
    # index = find_index_post(id)
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    del_post = cur.fetchone()
    conn.commit()
    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cur.execute(""" UPDATE posts SET title = %s, context = %s, published = %s WHERE id = %s RETURNING *""",
                (post.title, post.context, post.published, str(id)))
    up_post = cur.fetchone()
    conn.commit()
    print(up_post)
    if up_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} not found.")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_post[index] = post_dict
    return {"message": up_post}
