import csv
import sys
import re

if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")

# Read DNA sequence
with open(sys.argv[2], "r") as txt:
    dna = txt.read(-1)

# Open CSV file
with open(sys.argv[1], "r") as data:
    # Open CSV to get the key
    read = csv.DictReader(data)
    for row in read:
        i = list(row)
        break
    i = i[1:]
    s = {}
    for STR in i:
        result = re.findall(f"(?:{STR})+", dna)
        if result:
            s[STR] = str(int(len(max(result)) / len(STR)))

# Searching to find and result
with open(sys.argv[1], "r") as data:
    read = csv.DictReader(data)
    for row in read:
        a = dict(row)
        del a["name"]
        if a == s:
            print(row["name"])
            break
    # End :)
    else:
        print("No match")
    sys.exit(0)