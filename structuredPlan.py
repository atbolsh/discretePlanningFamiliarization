from strips.strips import *

# This file will only deal with strips.
# Given a list of actions and variables they should be called with, creates an action with specific pre and post conditions (or crashes) which can be used in planning.
# Additionally, at moving time, it knows how to create a list of GroundedAction elements that can be used for instructions.

# Alternatively, this plan might be used to ground exactly one action at a time, so that excessive memory is not used and recursion is possible. 
# Basically, it has options.

class BoundAction:
    def __init__(self, action, binding): # Accepts Action obj, and a binding of new variables (same order as old params)
        self.action = action
        self.refs = dict(zip(action.params, binding))
        self.name = action.name
        self.pre = [p.change_basis(self.refs) for p in self.action.pre]
        self.post = [p.change_basis(self.refs) for p in self.action.post]
    
    def ground(self, args_map): # args_map from binding to literals
        literals = tuple([args_map[self.refs[p]] for p in self.action.params])
        return self.action.ground(literals) # A little wasteful to go back and forth like this, but dict lookups are fast, and this is better than messy code.
          

def update_unclosed_state(state, p):
    for i in range(len(state)):
        if weak_match(state[i], p):
            state[i] = p # Replace truth either way
            return
    state.append(p)


class StructuredPlan:
    def __init__(self, name, params, boundList): # List of (Action, (Binding)) pairs
        self.name = name
        self.params = params
        self.backend = [BoundAction(*bl) for bl in boundList]
        self.get_conditions()
        # self.post = 
    
    def ground(self, literals):
        args_map = dict(zip(self.params, literals))
        return [b.ground(args_map) for b in self.backend]

    def get_conditions(self):
        pre = []
        state = []
        for ba in self.backend:
            for p in ba.pre:
                t = weak_find(state, p)
                if t is None: # If it had ever been in the state, it would still weakly be here, because we are using an unclosed world.
                    pre.append(p)
                    state.append(p)
                elif t.truth != p.truth:
                    raise Exception("Contradictory Requirements for plan.")
                else:
                    continue
            # Then, step passes
            for p in ba.post:
                update_unclosed_state(state, p)
        self.pre = pre
        self.post = state # All have passed, this is what we have left

    def action(self): # Planning-level construct that can be added to the world.
        return Action(self.name, self.params, self.pre, self.post)
     
