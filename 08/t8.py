#! python3

# I could not come with anything better than np solution in Reddit, so took it as
# a learning material...

from pprint import pprint
import numpy as np

# remember - best to read, strip and reshape in one line
with open('input', 'r') as data:
    data = np.array(list(data.read().strip())).reshape((-1, 6, 25))

# get the minimal layer for sum of zeros
zeros_layer = min(data, key=lambda func:np.sum(func == '0'))

# it's not summing the numbers itself, but number of times the condition is true
print(np.sum(zeros_layer == '1') * np.sum(zeros_layer == '2'))

# initial result is the first layout
result = data[0]

for next_layer in data:
    # if item is not 2, keep what is there, otherwise put what found in the new layer
    result = np.where(result != '2', result, next_layer)

# replace for better readability
result = np.where(result == '1', '█', ' ') 
for row in result: # Part 2
    print(*row, sep='')

