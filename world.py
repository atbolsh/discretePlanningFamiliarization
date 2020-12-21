import numpy as np
from agent import *

# Elements can only be picked up at a location one at a time.
# Hopefully, I'll be able to make a framework that understands how to manipulate objects between 5 stacks.

class Element:
    def __init__(self, name, t = "inedible"):
        self.name = name
        self.t = t
    
    def __str__(self):
        return self.t + ':' + self.name


class Stack:
    def __init__(self, container=None):
        self.container = []
        if type(container) != type(None):
            for x in container:
                self.container.append(x)
    
    def add(self, x):
        self.container.append(x)
    
    def pop(self):
        try:
            return self.container.pop()
        except IndexError:
            return None
    
    def __str__(self):
        return ' :: '.join([str(x) for x in self.container[::-1]])


class Location:
    def __init__(self, name):
        self.name = name
        self.objs = Stack()
        self.agents = []

    def __str__(self):
        return self.name + ': Agents ' + ', '.join([str(x) for x in self.agents]) + '; Stack ' + str(self.objs)
    
    def place(self, x):
        self.objs.add(x)
    
    def pickup(self):
        return self.objs.pop()
    
    def enter(self, agent):
        self.agents.append(agent)
        agent.location = self # TEST / DEBUG THiS LINE!
    
    def remove(self, agent):
        self.agents.remove(agent)


class World:
    def __init__(self):
        self.places = []
        for letter in 'ABCDE':
            self.places.append(letter)
            self.__dict__[letter] = Location(letter) # 5 places

    def __str__(self):
        return 'World:\n\n' + '\n'.join([str(self.__dict__[place]) for place in self.places])


