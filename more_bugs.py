balance = 100

def withdraw(amount):
    global balance
    balance = balance - amount
    print(f"New balance: {balance}")

def greet(names):
    for i in range(len(names) + 1):
        print("Hello", names[i])

withdraw(200)
greet(["Alice", "Bob"])
