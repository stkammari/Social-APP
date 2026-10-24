## Our social media application

import sqlite3    # ---> Importing sqlite built-in Python library to store the information

DATABASE_NAME = "social_app.db"   # ---> creating a database name


# Creating the database and table
def setup_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()        # ---> It will execute and retrieve the sql queries

    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, message TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    connection.commit()
    connection.close()


# Creating a post
def create_post(username, message):        # ---> Defining a function for post creation by user
    username = username.lower().strip()                   # ---> Converting username to lower and Unwanted spaces free
    message = message.strip()                             # ---> Converting message to unwanted spaces free

    ## Conditions to show error ---> no name, only spaces instead of text, not more than 200 characters

    if username == "" :
        return "Error: Please enter a valid username"

    if message == "" :
        return "Error: Post cannot be empty"

    if len(message) > 200:
        return "Error: Post is too long"

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO posts (username, message) VALUES (?, ?)",(username, message))

    connection.commit()
    connection.close()

    return "Post saved successfully"



# Display the feed
def show_feed():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()


    cursor.execute("""SELECT username, message, created_at FROM posts ORDER BY id DESC""")

    all_posts = cursor.fetchall()

    connection.close()

    print("\n--- THE FEED ---")


    if len(all_posts) == 0:
        print("No posts created!")
        return


    for username, message, created_at in all_posts:
        print(f"@{username}: {message}")
        print(f"Posted at: {created_at}")
        print("-"* 30)



# Starting the application

setup_database()

while True:
    print("Social App")
    print("1. Create a new post")
    print("2. View all posts")
    print("3. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        username = input("Enter your username: ")
        message = input("Write your post: ")

        result = create_post(username, message)
        print(result)


    elif choice == "2":
        show_feed()


    elif choice == "3":
        print ("Thank you for visiting Social App!")
        break

    else:
        print("Choose a correct option! \n 1, 2, or 3.")