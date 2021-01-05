# May need to change the imports later.
from strips.strips import *
from world import *
from agent import *

# Reverse of perceptor; given STRIPSworld, creates a real world object, or raises an error (VITALLY IMPORTANT).

# I might need to declare a new class, SimWorld, with SimPlaces, where agents are just strings.

# Not as universal, I'm afraid, as the others. The special  predicates might need to be pulled out.

def simulate(sw): # For now, this is the easiest way to wrap it up. If I wanna store all the dicts later, I might, but it's honestly overkill.
    s = Simulator(sw)
    s.simulate()
    return s.simAgent

class Simulator: # THis is easy; the hard part is the stochastic stuff necessary when we move on to 2d continuous spaces.
    def __init__(self, sw):
        self.sw = sw

    def simulate(self):
        self.w = World()
        self.specialLiterals = set(['self'])
        for place in self.w.places:
            self.specialLiterals.add(place)
        self.processElements()
        self.processEdible() # Can later be replaced with a dict of attributes
        # Finished with basics, now creating the stacks with a poor man's version of linked lists
        self.onDict = dict(self.sw.state['On']) # Conveniently, a list of 2-item tuples in the right order for us
        self.placeItems()
        # Now, build some other dictionaries, only a couple of which are useful for now.
        self.buildAtDict() # Not really needed now, but might be useful later on.
        self.topDict = dict(self.sw.state['Top']) 
        # Finishing touches in making the actual 'embodied' agent, to be handed in.
        locName = self.atDict['self']
        self.simAgent = SimAgent('self', self.w, self.w.__dict__[locName]) 
    
    def processElements(self):
        self.elements = {}
        for kl in self.sw.known_literals:
            if kl not in self.specialLiterals:
                el = Element(kl)
                self.elements[kl] = el
    
    def processEdible(self):
        for monoTuple in self.sw.state['Edible']:
            self.elements[monoTuple[0]].t = 'edible'
    
    def placeItems(self):
        for base in self.w.places:
            fullPlace = self.w.__dict__[base]
            while base in self.onDict:
                base = self.onDict[base] # First one not placed; is the place itself!
                fullPlace.place(self.elements[base]) # Put them in the place, in the correct order.
                    
    def buildAtDict(self):
        reverseAtTuples = [(t[1], t[0]) for t in self.sw.state['At']]
        self.atDict = dict(reverseAtTuples)
 
