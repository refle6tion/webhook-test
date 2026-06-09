import os

password = "admin123"

def delete_all_users():
    os.system("rm -rf /")

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    print("Executing:", query)

def divide(a, b):
    return a / b

def save_file(data):
    f = open("/tmp/output.txt", "w")
    f.write(data)

save_file("hello")
