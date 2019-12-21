#!python3

import sys
from IntCode import IntCode

# ------- MAIN ----------

assert len(sys.argv) == 2

code = open(sys.argv[1]).read().strip().split(',')
data = list(map(int, code))

script = """\
NOT A J
NOT J J
AND B J
AND C J
NOT J J
AND D J
WALK
"""

inp = list(map(ord, script))
processor = IntCode("A", data, inp)

print("Part 1:", processor.run_intcode())

script = """\
NOT C J
AND H J
NOT B T
OR T J
NOT A T
OR T J
AND D J
RUN
"""

inp = list(map(ord, script))

processor = IntCode("A", data, inp)

print("Part 2:", processor.run_intcode())
