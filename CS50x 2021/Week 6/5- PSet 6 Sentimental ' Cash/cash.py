from cs50 import get_float

c = 0
# Get owe...
print("Write down the amount you owe to calculate the number of coins like ($.¢)... ")
o = 0
while True:
    o = get_float("Owed: ")
    if o > 0:
        break
# rounding number.
ce = round(o * 100)
# Quarter.
while 25 <= ce:
    ce -= 25
    c += 1
# Dime.
while 10 <= ce:
    ce -= 10
    c += 1
# Nickel.
while 5 <= ce:
    ce -= 5
    c += 1
# Penny.
while 1 <= ce:
    ce -= 1
    c += 1
# End!
print(c)