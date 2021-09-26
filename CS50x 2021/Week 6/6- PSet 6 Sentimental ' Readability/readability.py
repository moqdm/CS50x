from sys import exit

# Get Text...
text = input("Text: ")

# Variables...
h = 0
s = 0
l = 0
c = 0
k = 1
sat = 0

# Check and count...
for i in range(len(text)):
    if text[i] >= 'A' and text[i] <= 'z':
        h += 1
    if text[i] == ' ':
        k += 1
    if text[i] == '.' or text[i] == '!' or text[i] == '?':
        sat += 1

# Calculate...
l = (h / k) * 100.0
s = (sat / k) * 100.0
c = 0.0588 * l - 0.296 * s - 15.8

# Results...
if c < 1:
    print("Before Grade 1")
    exit(0)
if c > 16:
    print("Grade 16+")
    exit(0)
c = round(c)
# End :)
print(f"Grade {int(c)}")
exit(0)