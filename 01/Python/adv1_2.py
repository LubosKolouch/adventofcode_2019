#! python3

def get_fuel_req(input):
    total = 0

    while (input > 0):
     input = int(input/3)-2
     if (input > 0):
         total += input

    return total

file = open("../1.txt","r")

total = 0

for line in file:
    total += get_fuel_req(int(line.strip()))

print(total)

