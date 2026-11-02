## Our social media application
import curses
import sqlite3    # ---> Importing sqlite built-in Python library to store the information
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from fastapi.staticfiles import StaticFiles

DATABASE_NAME = "social_app.db"   # ---> creating a database name

app = FastAPI(title = "Social App API" )    # ---> Creating a variable and calling FastAPI


# Creating the database and table
def setup_database():
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(""" CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, message TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")


# Creating the function for likes
def add_likes_column():
    with sqlite3.connect(DATABASE_NAME) as connection:
        columns = connection.execute("PRAGMA table_info(posts)").fetchall()

        column_names = [column[1] for column in columns]

        if "likes" not in column_names:
            connection.execute("""ALTER TABLE posts ADD COLUMN likes INTEGER NOT NULL DEFAULT 0""")


# Defining the data a user must send to create a post
class PostRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=200)


setup_database()
add_likes_column()


# Home Endpoint


@app.post("/posts", status_code=201)
def create_post(post: PostRequest):
    username = post.username.strip()
    message = post.message.strip()

    if not username or not message:
        raise HTTPException(status_code=400, detail="Username or Message cannot be empty!")

    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute("""INSERT INTO posts (username, message) VALUES (?, ?)""", (username, message))

        post_id = cursor.lastrowid


        row = connection.execute("""SELECT id, username, message, created_at, likes FROM posts WHERE id = ?""", (post_id,)).fetchone()



    return {
        "id" : row[0],
        "username" : row[1],
        "message" : row[2],
        "created_at" : row[3],
        "likes" : row[4]
    }


# Get all posts
@app.get("/post")
def get_posts():
    with sqlite3.connect(DATABASE_NAME) as connection:
        rows = connection.execute("""SELECT id, username, message, created_at, likes FROM posts ORDER BY id DESC""").fetchall()

    return [
        {
            "id" : row[0],
            "username" : row[1],
            "message" : row[2],
            "created_at" : row[3],
            "likes" : row[4]
        }
        for row in rows
    ]

@app.post("/posts/{post_id}/like")
def like_post(post_id: int):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute("""UPDATE posts SET likes = likes + 1 WHERE id = ?""", (post_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Post not found!")

        row = connection.execute("SELECT likes FROM posts WHERE id = ? ", (post_id,)).fetchone()

        return {
            "post_id" : post_id,
            "likes" : row[0],
            "message" : "Post liked successfully!"
        }


app.mount(
    "/",
    StaticFiles(
        directory=Path(__file__).parent / "static",
        html=True
    ),
    name="frontend"
)