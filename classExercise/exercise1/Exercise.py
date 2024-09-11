## my teammate: guan hong lin

from random import randint
from collections import Counter


num_lines = randint(100,300)  # randomize the length of the file

with open('random_numbers.txt', 'w') as f:
    for i in range(num_lines):
        nums_per_line = randint(2, 80) # Randomize how many distinct numbers we put on this line
        s = '' # initialize a blank string
        for j in range(nums_per_line):
            # Generate a new random number between 1 & 1000, inclusive:
            n = randint(1, 1000)
            s += str(n) + ' '  # convert integer to string and concatenate with a space
        print(s, file=f)

result = []

with open('random_numbers.txt', 'r') as f:

    counter = Counter()
    # We don't necessarily know how long the file is, but we can still use a for loop:
    for line in f:   # reads ONLY ONE line from the file, and stops when hits end of file.
        line = line.replace('\n','')
        values_on_line = line.split()  # Split string at spaces into list of "words" which are number strings.
        line_total = 0  # initialize to zero
        count  = 0
        counter.update(values_on_line)
        for value in values_on_line:
            # check if it's convertible to an integer as expected:
            try:
                n = int(value)
            except ValueError:
                print('WARNING: ignoring invalid non-integer value found:', value)
                n = 0
            count+=1
            line_total += n  # accumulate the line total

        result.append(f'Line Total: {line_total}  ,Original data: {line} , and the mean of this line is {line_total/count}')
    top_5_most_common = counter.most_common(5)
    result.append(f'top 5 most common numbers are {top_5_most_common}')

    with open('output.txt', 'w') as file:
        for item in result:
            file.write(item + '\n')
