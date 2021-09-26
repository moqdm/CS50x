from cs50 import get_int

# Notification
print("Welcome, Please enter a number from one to eight to build.")
# Getting height.
h = 0
while 1 > h or h > 8:
    h = get_int("Height: ")
# Build.
for i in range(h):
    print((h - 1 - i) * " ", end="")
    print((i + 1) * "#")