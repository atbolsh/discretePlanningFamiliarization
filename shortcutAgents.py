# The idea is that these agents can imagine a lot of actions that the 
# agent can't take directly (like using the 'place' method), and then
# learn to simulate the before and after effects of different actions, 
# try different plans, etc. 

# Ideally, they will be able to just "plan" exactly like the original planner,
# but using a mental representation of the space itself rather than only 
# the limited predicates, Might also avoid the "exponential growth of functions" 
# problem that keeps happening.

# This is really the crux of the 'simulation' portion; with continuous 2d agents,
# this will involve teleporting accross the map and simulating that the agent is absent,
# etc.

from agent import *
from simulator import *
from perceptor import *

# For apples, the some actual methods needed:

# 1) Take(X) (from anywhere)
# 2) Remove(X) (disappears; goes to a 'limbo' dict.) Limbo will be useful.
# 3) Fuse(X, Y): If On(Y, X), then these two will become a single object.
# 4) Unfuse(Y): splits it into just two parts.
# 5) Move(X, From, To): X teleports

# All of this will correspond to actions defined in a new STRIPS file.
# There also need to be simple ways to turn off one or more of these actions.
# This can be added in the STRIPS file (eg, one of the consequences is RemoveActionUsed, and you can't undo that predicate).

# I really need to start thinking about how to define subproblems and solve them in a submethod, 
# OR 
# Make limiting the specific set of literals under consideration part of executing a plan.

