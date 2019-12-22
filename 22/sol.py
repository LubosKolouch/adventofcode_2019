# solution from Reddit... too mathematical for me to bother...

import re
import sympy
from collections import deque

# Stolen from https://www.geeksforgeeks.org/modular-exponentiation-python/
def modInverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        # q is quotient
        q = a // m
        t = m
        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y
        # Update x and y
        y = x - q * y
        x = t
    # Make x positive
    if x < 0:
        x = x + m0
    return x


read = open("input").read().strip()
lines = read.strip().split("\n")
deck = deque(range(10007))
for i, line in enumerate(lines):
    if line == "deal into new stack":
        deck = deque(reversed(deck))
    else:
        num, = map(int, re.findall(r"-?\d+", line))
        if line.startswith("deal with increment "):
            arr = [-1] * len(deck)
            dealt = 0
            for j in range(0, 10 ** 9, num):
                arr[j % len(arr)] = deck.popleft()
                dealt += 1
                if dealt == len(arr):
                    break
            deck = deque(arr)
        elif line.startswith("cut "):
            deck.rotate(-num)
        else:
            assert False
print("Part1", deck.index(2019))


def getEquation(deckSize):
    curr = sympy.Symbol("x", integer=True)
    for line in reversed(lines):
        if line == "deal into new stack":
            curr = deckSize - 1 - curr
        else:
            num, = map(int, re.findall(r"-?\d+", line))
            if line.startswith("deal with increment "):
                # curr maps to curr * num % deckSize
                # So to undo the step need to find num^-1 % deckSize
                # Sympy can't handle simplifying the mods so we do it all at once in the end
                num_inv = modInverse(num, deckSize)
                curr = curr * num_inv
            elif line.startswith("cut "):
                curr += num
            else:
                assert False
    return sympy.simplify(curr % deckSize)


# Double check that this equation indeeds map my part 1 answer back to 2019
print(getEquation(10007))
x = 3939
assert (
    2019
    == (
        1315392026111080230451006564378314839352784895845592294250786878653195721500650716576276684844395334211426149137983383398423195398120918156699848671232000000000
        * x
        + 3517
    )
    % 10007
)

# Actual part 2
m = 119315717514047
print("Part2")
print(getEquation(m))
# So the above maps a*x + b, which we copy down here:
a = 64701337022060343820226393583070349434634307926694491961597553874086667241858882805974964927526696341879184859440299872225838381081016011205767500567133993486371913753517642027543653238974053108178007527810720946448672170703287188397881081098463537817926311407053629833397998496748246747377408422900706248412225246788376129398970815623890514469506475268175585405666624882104420028439898015321116879607429441244694150213491370243179289017439287966745941270399968386095768818703624996367576619856050403303885870024957315735095874708801656287179783817532077624936961664426785781467129097523999172632191696896000000000
b = 89398771567475
N = 101741582076661
# Each a * x + b will undo one shuffle. Need to iterate N times
#
#   a * x +       b
# a^2 * x + a   * b +       b
# a^3 * x + a^2 * b + a   * b  +     b
# a^4 * x + a^3 * b + a^2 * b  + a * b + b
# ...
# a^N * x + (a^(N-1) + a^(N-2) + ... + 1) * b
#
# The geometric sum can also be simplified to (a^N - 1) / (a - 1). Thus:
print(
    "Part2", (pow(a, N, m) * 2020 + b * (pow(a, N, m) - 1) * modInverse(a - 1, m)) % m
)
