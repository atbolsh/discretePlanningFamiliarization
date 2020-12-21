import numpy as np

class SimAgent: # The sock-puppet used by both human characters and by the automatic agents, later.
    def __init__(self, name, location):
        self.name = name
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
        return (self.location.name, str(self.holding), self.lastAction, self.deltaR)
    # This can output the state, but not FULL state (no info on location info, for instance).
    # All more sophisticated info gathering / learning will come later.
    # For now, I will code up a straightforward STRIPS planner for this system.
    # THEN, I will try to do "STRIPS IN STRIPS" where the fundamental actions are sentence manipulations.
    # THEN, I will add "simulation." Should all work out.

