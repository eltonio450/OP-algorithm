from Node import *
from Memory import Memory

class Algo(object):
    """description of class"""


    def set_parameters(self, generator, initial_state_value, n_iterations, gamma, optimized = False):
        self.gamma = gamma
        self.generator = generator
        self.initial_state = State_Node(initial_state_value, 0)
        self.depth = n_iterations
        return self
        

    def run(self, verbose, verbose_more):
        self.verbose = verbose
        self.verbose_more = verbose_more
        self.optimistic_nodes = {}
        self.initial_state.ub = 1/(1-self.gamma)
        self.initial_state.lb = 0
        self.initial_state.probability = 1
        self.initial_state.reward = 0
        self.initial_state.is_leaf_in_the_main_tree = True

        for i in range(0, self.depth):
            if verbose:print("Iteration " + str(i) + "...")
   
            self.optimistic_tree_leaves = []
            self.build_optimistic_subtree(self.initial_state, 1) 
            if self.optimistic_tree_leaves == []:
                raise Exception("Leaves list is empty !")
            leaf_to_expand = self.select_leaf_to_expand(self.optimistic_tree_leaves)
            
            if self.verbose:
                for item in self.optimistic_tree_leaves:
                    print("Leaf :" + str(item[0].state)  +", LB: " + str(item[0].lb)+ ", UB: " + str(item[0].ub)+ ", Depth " + str(item[0].depth))
                print("Selected leaf for expansion: "+ str(leaf_to_expand.state))
            self.expand_main_tree(leaf_to_expand)
            self.update_b_value_upwards(leaf_to_expand)

            #reset of the optimistic tree
            for key in self.optimistic_nodes:
                self.optimistic_nodes[key].optimistic_probability = 0
            self.optimistic_nodes = {}
        return [self.initial_state.optimistic_action, self.initial_state.lb, self.initial_state.ub]



    def build_optimistic_subtree(self, root, probability): #p is the probabilty, r is the reward
        
        if root.get_key() not in self.optimistic_nodes.keys():
            self.optimistic_nodes[root.get_key()] = root

        self.optimistic_nodes[root.get_key()].optimistic_probability += probability

        if root.is_leaf_in_the_main_tree:            
            self.optimistic_tree_leaves.append((root, self.optimistic_nodes[root.get_key()].optimistic_probability*(self.gamma**root.depth)/(1-self.gamma)))
            return

        
        for state in self.generator.get_next_states(root.optimistic_action):
            new_probability = self.optimistic_nodes[root.get_key()].optimistic_probability*state[1]
            self.build_optimistic_subtree(state[0], new_probability)

        
    #this function can be applied to a leaf, it will return None
    #if nothing change, could be great not tu continue the upgrading upward.
    def update_bounds_and_policy(self, root):
        if root.is_leaf_in_the_main_tree:
            return 
        if self.verbose_more:
            print("Root update: " + str(root) + ", Optimistic action: " + str(root.optimistic_action))
            
        root.ub = 0
        root.lb = 0

        for action in self.generator.get_actions(root):
            
            ub = 0
            lb = 0
            for child in self.generator.get_next_states(action):
                #ub += child[0].ub*child[1]
                #lb += child[0].lb*child[1]
                ub += ((self.gamma**root.depth)*child[2] + child[0].ub)*child[1]
                lb += ((self.gamma**root.depth)*child[2] + child[0].lb)*child[1]
                if(ub <0):
                    print(root)
                    print(child[1])
                    raise Exception("Upper bound below 0.")
                
            if ub >= root.ub:
                root.ub = ub
                root.lb = lb
                root.optimistic_action = action
        if self.verbose_more:print("=> New optimistic action: " + str(root.optimistic_action) + ", UB: " + str(root.ub)+ ", LB: " + str(root.lb))



    def select_leaf_to_expand(self, leaves_list):
        max = 0
        for leaf in leaves_list:
            if leaf[1] > max:
                res = leaf[0]
                max = leaf[1]
        return res

    #cette fonction a l'air a peu pres juste
    def expand_main_tree(self, leaf):
        leaf.is_leaf_in_the_main_tree = False
        for action in self.generator.get_actions(leaf):
            for state in self.generator.get_next_states(action):                
                #state[0].ub = reward + (self.gamma**leaf.depth)*state[2] + (self.gamma**(state[0].depth))/(1-self.gamma)
                #state[0].lb = reward + (self.gamma**leaf.depth)*state[2] + 0
                state[0].ub = (self.gamma**(state[0].depth))/(1-self.gamma)
                state[0].lb =  0



    #this function can be applied to a leaf.
    def update_b_value_upwards(self, starting_point):
        self.update_bounds_and_policy(starting_point)
        for key in starting_point.parent_nodes:
            self.update_b_value_upwards(starting_point.parent_nodes[key])