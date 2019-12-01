#! python3

file = open("../1.txt","r")

total = 0

for line in file:
    total += int(int(line.strip())/3-2)

print(total)

