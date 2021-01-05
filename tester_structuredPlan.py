from tester import *
from structuredPlan import *

# w is world, q is agent, as described in tester.

q.perceive() # Create the STRIPSimage of the world
sw = q.STRIPSimage

# Reduce notation a tad
go = sw.actions['Go']
placeEmpty = sw.actions['PlaceEmpty']
pickupStack = sw.actions['PickupStack']

p = StructuredPlan('MoveStackEmpty', ('X', 'From', 'Z', 'To'), [(pickupStack, ('X', 'From', 'Z')), (go, ('From', 'To')), (placeEmpty, ('X', 'To'))])

# This small failed test really shows the limitations of just using predicates and such.
# What's really, really needed is a robust simulation protocol that can catch this sort of impossible precondition.
# Which I am building next.
try:
    p2 = StructuredPlan('BadMoveStackEmpty', ('X', 'From', 'Z', 'To'), [(pickupStack, ('X', 'From', 'Z')), (placeEmpty, ('X', 'To'))])
except Exception:
    print("It worked! Detects unexecutable plans!!")


