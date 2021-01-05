import numpy as np
from world import *
from perceptor import *

class SimAgent: # The sock-puppet used by both human characters and by the automatic agents, later.
    def __init__(self, name, world, location):
        self.name = name
        self.world = world
        location.enter(self) # Debug to make sure this works.
        self.holding = None
        self.reward = 0 # Accumulates over time; we'll ignore the other stuff for now.
        self.deltaR = 0
        self.lastAction = ''
   
    def __str__(self):
        return self.name

    def pickup(self):
        if type(self.holding) == type(None):
            self.holding = self.location.pickup()
        self.deltaR = 0 # This action does not affect reward at all.
        self.lastAction = 'pickup'
    
    def place(self):
        if type(self.holding) != type(None):
            self.location.place(self.holding)
            self.holding = None
        self.deltaR = 0 # This action does not affect reward at all.
        self.lastAction = 'place'
    
    def eat(self):
        if type(self.holding) != type(None) and self.holding.t == 'edible':
            self.holding = None
            self.reward += 1
            self.deltaR = 1
        else: # Nothing happens
            self.deltaR = 0
        self.lastAction = 'eat'
    
    def goTo(self, location):
        self.location.remove(self)
        location.enter(self) # Again, needs debugging.
        self.deltaR = 0
        self.lastAction = 'goTo(' + location.name + ')'
    
    def receive(self, R): # Hook to receive custom rewards in human-interaction mode, or with specialized tasks.
        self.reward += R
        self.deltaR = R
        # NOT recorded as an action. Just a manipulator. Should be associated with the previous action.
    
    def state(self):
        return { \
                    'name': self.name, \
                    'location': self.location.name, \
                    'holding': str(self.holding), \
                    'lastAction': self.lastAction, \
                    'deltaR': self.deltaR \
               }
    # This can output the state, but not FULL state (no info on location info, for instance).
    # All more sophisticated info gathering / learning will come later.

    def full_state(self):
        s = self.state()
        s['world'] = self.world.state()
        return s

# Shell for now; will include ability to read off predicates from world.
class Agent(SimAgent):
    def __init__(self, name, world, location):
        super(Agent, self).__init__(name, world, location)
        # see eat_apple_v7.txt
        self.perceptor = Perceptor()
        self.STRIPSimage = deepcopy(self.perceptor.sw)
        self.stripsActions = {\
            'Go': self.goTo,
            'PickupEmpty': self.pickup,
            'PickupStack': self.pickup,
            'PlaceEmpty': self.place,
            'PlaceStack': self.place,
            'Eat': self.eat
        }
        # Don't need to include all of them, just the ones that matter to low-level actions. In the future, could be compiled from world using names.
        self.stripsLiterals = {\
            'A': self.world.A,
            'B': self.world.B,
            'C': self.world.C,
            'D': self.world.D,
            'E': self.world.E
        }
        #Simple for now, but can be written longer. Consume list of literals, spit out dict of relevant args.
        self.literalPostProcessors = {\
            'Go': lambda literals: {'location': self.stripsLiterals[literals[1]]}, # Only need destination
            'PickupEmpty': lambda literals: {},
            'PickupStack': lambda literals: {},
            'PlaceEmpty': lambda literals: {},
            'PlaceStack': lambda literals: {},
            'Eat': lambda literals: {}
        }
    
    def perceive(self):
        self.perceptor.perceiveSelf(self)
        self.STRIPSimage = deepcopy(self.perceptor.sw)
        self.perceptor.reset() # The compiler shouldn't keep track of all that's been perceived; that's the agent's job.
  
    def executeGroundedAction(self, ga):
        name = ga.action.name
        args = self.literalPostProcessors[name](ga.literals)
        return self.stripsActions[name](**args)

    def executePlan(self, plan):
        for groundedAction in plan:
            self.executeGroundedAction(groundedAction)
    


