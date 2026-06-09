import subprocess

user_input = input("Enter server IP: ")
subprocess.call("ping " + user_input, shell=True)

items = [1, 2, 3]
print(items[3])

def get_user():
    return None

user = get_user()
print(user["name"])
