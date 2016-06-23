from Generator import *
from Algo import *

print("Welcome.")
print("This is an example of usage of OP-Algorithm for Dynamic Pricing, with a product following a Bernoulli sales distribution")

"""WIP"""




initial_state = (5,0,0,0,0,1)

gen = Generator()

gen.set_generate_actions_function(generate_actions_values)
gen.set_generate_children_function(generate_children_values)

gen.set_paramaters(5,8,)
gen.set_normalization(-100, 1000)
                  
alg = Algo()
alg.set_parameters(gen, 10, initial_state, 0, 0.8, False)