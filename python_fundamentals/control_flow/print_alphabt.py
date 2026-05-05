#!/usr/bin/env python3
result = ''
for i in range(ord('a'), ord('z') + 1):
    if chr(i) != 'q' and chr(i) != 'e':
        result += chr(i)
print('{}'.format(result), end='')
