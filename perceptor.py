from strips.strips import *
from world import *

# Class that creates a STRIPSworld from a World.
# Assume exactly 1 agent for now.

class Perceptor:
    """Usage: perceive(world) or perceiveSelf(agent)"""
    def __init__(self, fname='strips/emptyAppleWorld.txt'): # Compiles from the POV of this agent.
        self.fname = fname
        self.reset()
        self.elementTypeToPredicateDict = {  # In the future, this could be a list of attributes or something.
                'edible': 'Edible',
            }
        self.walkerDict = { \
                Element: self.perceiveElement,
                Stack: self.perceiveStack,
                Location: self.perceiveLocation,
                World: self.perceiveWorld,
#                Agent: self.perceiveSelf
            }
    
    def reset(self):
        self.sw = create_world(self.fname)
    
    def perceive(self, obj): # Nasty tree walker.
        self.walkerDict[type(obj)](obj)
    
    def perceiveElement(self, el):
        self.sw.add_literal(el.name)
        if el.t != 'default':
            p = self.elementTypeToPredicateDict[el.t]
            self.sw.set_true(p, (el.name,))
    
    def perceiveStack(self, stack):
        # Has to be first, to get the literals in there
        for el in stack.container:
            self.perceive(el)
        # Can't do much else without location name; that happens in next walker
    
    def perceiveLocation(self, loc):
        self.sw.add_literal(loc.name) # Expand literals
        self.perceive(loc.objs) # Expand literals further.
        # Process objects
        if len(loc.objs.container) == 0:
            self.sw.set_true('Empty', (loc.name,))
        else:
            self.sw.set_false('Empty', (loc.name,))
            for el in loc.objs.container:
                self.sw.set_true('At', (loc.name, el.name))
            self.sw.set_true('On', (loc.name, loc.objs.container[0].name))
            self.sw.set_true('Top', (loc.name, loc.objs.container[-1].name))
            if len(loc.objs.container) > 1:
                for i in range(1, len(loc.objs.container)):
                    prev = loc.objs.container[i - 1].name
                    cur = loc.objs.container[i].name
                    self.sw.set_true('On', (prev, cur))
        #Process agents
        if len(loc.agents) > 0:
            self.sw.set_true('At', (loc.name, 'self')) ## IMPORTANT!! WE ASSUME FOR NOW THAT THERE IS ONLY ONE AGENT!! Also, don't process agents fully, ever; can't see inside minds.

    def perceiveWorld(self, w):
        for p in w.places:
            self.perceive(w.__dict__[p])         

    def perceiveSelf(self, agent): # Note, this is only run on the agent through whose eyes we are perceiving. This could change later.
        if agent.holding is None:
            self.sw.set_true('Emptyhanded', ('self',))
        else:
            self.perceive(agent.holding)
            self.sw.set_true('Holding', (agent.holding.name,))
        self.perceive(agent.world) # Most important line
                

 
