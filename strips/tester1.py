from strips import *

w = create_world('oldFormatFiles/eat_apple_v7.txt')

print(w.__dict__)

w.step('Go', ('b', 'e'))

print(w.__dict__)

