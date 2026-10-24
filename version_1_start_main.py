## Our social media application




posts = []       # Creating and storing an empty list of posts



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

    post = {
        "username": username,
        "message": message
    }

    posts.append(post)

    return "Post created successfully"


def show_feed():
    print("\n--- Feed ---")


    if len(posts) == 0:
        print("No posts created!")
        return


    for post in posts:
        print(f"@{post['username']}: {post['message']}")\


## phase 1 : Making the feed interactive

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
        result = show_feed()
        print(result)

    elif choice == "3":
        print ("Thank you for visiting!")
        break

    else:
        print("Choose a correct option! \n 1, 2, or 3.")












