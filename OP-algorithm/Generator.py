from Node import *

class Generator(object):

    def __init__(self):
        self.generated_states = {}

    def generate_actions_values(self, state_value):
        raise Exception("Function generate_children_values(self, state_value, action_value) has not been specified. Please use 'Generator::set_generate_actions_function(f)' to specify.")

    """Must return a list of all the children, their probability and the reward associated"""
    def generate_children_values(self, state_value, action_value):
        raise Exception("Function generate_children_values(self, state_value, action_value) has not been specified. Please use 'Generator::set_generate_children_function(f)' to specify.")

    def set_generate_actions_function(self, f):
        self.generate_actions_values = f

    def set_generate_children_function(self, f):
        self.generate_children_values = f

    def set_normalization(self, mini = 0, maxi = 1):
        self.min = mini
        self.max = maxi

    def normalize(self, value):
        res = (value - self.min)/(self.max - self.min)
        if res > 1 or res < 0:
            print("Value: " + str(value) + ", Res: " + str(res))
            raise Exception("Bad normalization: reward value must be between 0 and 1.")
        return res

    def denormalize(self, value):
        return value*(self.max - self.min) + self.min
    

    def generate_actions(self, state_node):
        for action in self.generate_actions_values(state_node.state):
            action_value = self.normalize(action)
            state_node.__possible_actions__.append(Action_Node(action_value, state_node, state_node.depth))

    def generate_children(self, action_node):
        for child in self.generate_children_values(action_node.parent_node.state, self.denormalize(action_node.action)):
            ns = State_Node(child[0], action_node.depth+1)
            if ns.get_key() in self.generated_states.keys():
                ns = self.generated_states[ns.get_key()]
            else:
                self.generated_states[ns.get_key()] = ns
            if action_node.parent_node.get_key() not in ns.parent_nodes.keys():
                ns.parent_nodes[action_node.parent_node.get_key()] = action_node.parent_node
            action_node.__children_nodes__.append([ns, child[1], self.normalize(child[2])])


    def get_actions(self, state_node):
        if not state_node.is_action_list_generated:
            state_node.is_action_list_generated = True
            self.generate_actions(state_node)
        return state_node.__possible_actions__

    def get_next_states(self, action_node):
        if not action_node.is_children_generated:
            action_node.is_children_generated = True
            self.generate_children(action_node)
        return action_node.__children_nodes__