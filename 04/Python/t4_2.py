#! python3

count = 0

for i in range(172851, 675870):
    prev_num = 0
    ok = 1
    for char in str(i):
        if int(char) < prev_num:
            ok = 0
        prev_num = int(char)

    if ok == 1:
        found = 1
        prev_char =0

        for char in str(i):
            if (char != prev_char):
                if found ==2 : break
                found = 1
            else:
                found += 1

            prev_char = char

        if found ==2: count += 1

print(count)
