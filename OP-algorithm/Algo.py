from Node import *

class Algo(object):
    """description of class"""


    def set_parameters(self, generator, initial_state_value, n_iterations, gamma, optimized = False):
        self.gamma = gamma
        self.generator = generator
        self.initial_state = State_Node(initial_state_value, 0)
        self.depth = n_iterations
        return self
        

    def run(self, verbose):
        self.verbose = verbose

        self.initial_state.ub = 1/(1-self.gamma)
        self.initial_state.lb = 0
        self.initial_state.probability = 1
        self.initial_state.reward = 0
        self.initial_state.is_leaf_in_the_main_tree = True
        self.update_bounds_and_policy(self.initial_state)

        for i in range(0, self.depth):
            if verbose:print("Iteration " + str(i) + "...")
            

            
            
            self.optimistic_tree_leaves = []
            self.build_optimistic_subtree(self.initial_state) 
            if self.optimistic_tree_leaves == []:
                raise Exception("Leaves list is empty !")
            leaf_to_expand = self.select_leaf_to_expand(self.optimistic_tree_leaves)
            self.expand_main_tree(leaf_to_expand)
            self.update_b_value_upwards(leaf_to_expand)
        return [self.initial_state.optimistic_action, self.initial_state.lb, self.initial_state.ub]



    def build_optimistic_subtree(self, root): #p is the probabilty, r is the reward
        if root.is_leaf_in_the_main_tree:
            self.optimistic_tree_leaves.append(root)
            return

        #self.update_bounds_and_policy(root)  
        for state in self.generator.get_next_states(root.optimistic_action):
            #to double check: what does the next line ?
            self.build_optimistic_subtree(state[0])

        
    #this function can be applied to a leaf, it will return None
    def update_bounds_and_policy(self, root):
        if root.is_leaf_in_the_main_tree:
            return 
        if self.verbose:
            print("Arbre update: " + str(root))
            print("Optimistic action: " + str(root.optimistic_action))

        for action in self.generator.get_actions(root):
            root.ub = 1/(1-self.gamma)
            root.lb = 0
            ub = 0
            lb = 0
            for child in self.generator.get_next_states(action):
                ub += child[0].ub*child[1]
                if(ub <0):
                    print(root)
                    print(child[1])
                lb += child[0].lb*child[1]
            if ub <= root.ub:
                
                root.ub = ub
                root.lb = lb
                root.optimistic_action = action
                if self.verbose:print("New optimistic action: " + str(action) + ", new upperbound: " + str(ub))



    def select_leaf_to_expand(self, leaves_list):
        max = 0
        for leaf in leaves_list:
            if leaf.probability*(self.gamma**leaf.depth)/(1-self.gamma) > max:
                res = leaf
                max = leaf.probability*(self.gamma**leaf.depth)/(1-self.gamma)
        return res

    #cette fonctio a l'air a peu pres juste
    def expand_main_tree(self, leaf):
        leaf.is_leaf_in_the_main_tree = False
        for action in self.generator.get_actions(leaf):
            for state in self.generator.get_next_states(action):
                state[0].reward  = leaf.reward + (self.gamma**state[0].depth)*state[2]
                state[0].ub = state[0].reward + (self.gamma**state[0].depth)/(1-self.gamma)
                state[0].probability = leaf.probability*state[1]
                state[0].lb = state[0].reward

    def update_b_value_upwards(self, starting_point):
        self.update_bounds_and_policy(starting_point)
        if starting_point.parent_action_node is not None:
            self.update_b_value_upwards(starting_point.parent_action_node.state_node)