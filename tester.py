from world import *
from agent import *


w = World()

q = Agent('bobby', w, w.B)

a = Element('apple', 'edible')
b = Element('buldozer')
#c = Element('carrot', 'edible')


w.A.place(a)
w.A.place(b)
#w.E.place(c)

# Challenge after this setup is to remove the buldozer in order to get to the apple.

