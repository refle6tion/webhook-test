import shutil

shutil.copy("/etc/passwd", "./passwd_backup")

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(-5))

def get_data():
    pass

data = get_data()
data.append(1)

x = 10
y = 0
print(x / y)
