#! python3
import re
import sys

count = 0

for i in range (172851,675870) : 

    if not re.match(r".*(\d)\1", str(i)): continue

    prev = 0
    exit = 0

    for x in str(i):
        if (int(x) < int(prev)) :
            exit = 1
            break

        prev = x

    if exit == 0: count +=1

print(count)
