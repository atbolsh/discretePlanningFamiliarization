from simulator import *

sw = create_world('strips/oldFormatFiles/eat_apple_v8.txt')
q = simulate(sw)
w = q.world

print(w)

