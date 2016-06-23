from Node import *

class Algo(object):
    """description of class"""


    def set_parameters(self, generator, initial_state_vale, n_iterations, fixed_value_lb, gamma, optimized = False):
        self.gamma = gamma
        self.generator = generator
        self.initial_state = State_Node(initial_state_value, 0)
        return self
        

    def run(self, verbose):
        for i in range(0, self.depth):
            self.initial_state.is_leaf_in_the_optimistic_tree = True
            self.optimistic_tree_leaves = []
            self.buid_optimistic_subtree(self.initial_state, 1, 0) 
            leaf_to_expand = self.select_leaf_to_expand(self.optimistic_tree_leaves)
            self.expand_main_tree(leaf_to_expand)
            self.update_b_value_upwards(leaf_to_expand)
        return [self.initial_state.secure_action, self.generator.denormalize(self.initial_state.lb), self.generator.denormalize(self.initial_state.ub)]

    def build_optimistic_subtree(self, root, p, r): #p is the probabilty, r is the reward
        if root.is_leaf_in_the_main_tree:
            self.optimistic_tree_leaves.append([root, p*(self.gamma**root.depth)/(1-self.gamma), r])
            return
        else: 
            self.update_bounds_and_policy(root)  
            for state in self.generator.get_next_states(root.optimistic_action):
                self.build_optimistic_subtree(self, state[0], state[1]*p, r + state[2]*self.gamma**state.depth)

        

    def update_bounds_and_policy(self, root):
        for action in self.generator.get_actions(root):
            ub = 0
            lb = 0
            for child in self.generator.get_next_states(action):
                ub += child[0].ub*child[1]
                lb += child[0].lb*child[1]
            if ub > root.ub:
                root.ub = ub
                root.optimistic_action = action
            if lb > root.lb:
                root.b = val
                root.secure_action = action

    def select_leaf_to_expand(self, leaves_list):
        leaf = leaves_list[0][0]
        max = leaves_list[0][1]
        for i in range(0, len(leaves_list)):
            if leaves_list[i][1] > max:
                res = leaves_list[i][0]
                max = leaves_list[i][1]
        return leaf

    def expand_main_tree(self, leaf):
        leaf.is_leaf_in_the_main_tree = False
        for action in self.generator.get_actions(leaf):
            for state in self.generator.get_next_states(action):
                state.ub = leaf.ub + self.gamma**state[0].depth*state[2]

    def update_b_value_upwards(self, starting_point):
        self.update_bounds_and_policy(starting_point)
        if starting_point.parent_action_node is not None:
            self.update_b_value_upwards(starting_point.parent_action_node.state_node)