# Comment this out, but these are really mind agents.

# The idea is that these agents can imagine a lot of actions that the 
# agent can't take directly (like using the 'place' method), and then
# learn to simulate the before and after effects of different actions, 
# try different plans, etc. 

# Ideally, they will be able to just "plan" exactly like the original planner,
# but using a mental representation of the space itself rather than only 
# the limited predicates, Might also avoid the "exponential growth of functions" 
# problem that keeps happening.

# This is really the crux of the 'imagination' portion; with continuous 2d agents,
# this will involve teleporting accross the map and imagining that the agent is absent,
# etc.

from agent import *
from simulator import *
from perceptor import *
