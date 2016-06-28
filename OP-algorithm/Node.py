class Action_Node(object):
    """description of class"""
    def __init__(self, action, parent_state_node, depth):
        self.state_node = parent_state_node
        self.depth = depth
        self.is_children_generated = False
        self.__children_nodes__ = [] #list of the children, their probability and the reward associated
        self.action = action

    def __str__(self):
        return str(self.action)

class State_Node(object):
    """description of class"""
    def __init__(self, state, depth, parent_action_node = None):
        """state has to be hashable"""
        self.parent_action_node = parent_action_node #in order to go upwards
        self.state = state
        
        
        
        self.depth = depth

        self.is_leaf_in_the_main_tree = True #please update!

        self.is_action_list_generated = False
        self.__possible_actions__ = [] #list of the possible actions

        self.optimistic_action = None

        self.probability = 0
        self.reward = 0
        self.ub = 0
        self.lb = 0

    def __str__(self):
        return str(self.state)


