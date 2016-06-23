from Node import *

class Generator(object):

    def generate_actions_values(self, state_value):
        raise Exception("Function generate_children_values(self, state_value, action_value) has not been specified. Please use 'Generator::set_generate_actions_function(f)' to specify.")

    """Must return a list of all the children, their probability and the reward associated"""
    def generate_children_values(self, state_value, action_value):
        raise Exception("Function generate_children_values(self, state_value, action_value) has not been specified. Please use 'Generator::set_generate_children_function(f)' to specify.")

    def set_generate_actions_function(self, f):
        self.generate_actions_values = f

    def set_generate_children_function(self, f):
        self.generate_actions_values = f

    def set_normalization(self, mini = 0, maxi = 1):
        self.min = mini
        self.max = maxi

    def normalize(self, value):
        return (value + self.mini)/(self.mini+self.maxi)

    def denormalize(self, value):
        return value*(self.mini+self.maxi) - self.mini
    

    def generate_actions(self, state_node):
        for value in self.generate_actions_values(state_node.state):
            value = self.normalize(value)
            state_node.__possible_actions__.append(Action_Node(value, state_node, depth))

    def generate_children_values(self, action_node):
        for child in self.generate_children_values(action_node.action, action_node.state_node):
            action_node.__children_nodes__.append([State_Node(child[0], action_node.depth+1, action_node), child[1],child[2]])


    def get_actions(self, state_node):
        if not state_node.is_action_list_generated:
            state_node.is_action_list_generated = True
            self.generate_actions(state_node)
        return state_node.possible_actions

    def get_next_states(self, action_node):
        if not action_node.is_children_generated:
            action_node.is_children_generated = True
            self.generate_children(action_node)
        return action_node.children_nodes