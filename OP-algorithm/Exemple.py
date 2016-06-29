from Generator import *
from Algo import *

print("Welcome.")
print("This is an example of usage of OP-Algorithm for Dynamic Pricing, with a product following a Bernoulli sales distribution")

"""WIP"""

MIN_PRICE = 200
MAX_PRICE = 1000
OBSERVED_SALES = 0.5
OBSERVED_PRICE = 500
MAX_SALES = 1
GAMMA = 0.95
STEP = 50
PRICE_LIST = range(MIN_PRICE, MAX_PRICE, STEP)




initial_state = (2, 0, 0, 1, 0, 1, 0)

gen = Generator()
gen.set_normalization(0, MAX_PRICE)


def demand_rate(price):
    return max(min(MAX_SALES - (price/OBSERVED_PRICE)*(1-OBSERVED_SALES),1),0) 



def generate_actions_values(state_value):
    if(state_value[0] == 0):
        return [MAX_PRICE]
    else:
        return PRICE_LIST
        

def generate_children_values(state_value, action_value):
    if state_value[0] == 0 :
        return [[state_value[1:] + (0,), 1, 0]]
    else:
        return [[(state_value[0]+state_value[1],) + state_value[2:] + (0,), 1-demand_rate(action_value),0],[(state_value[0]+state_value[1]-1,) + state_value[2:] + (1,), demand_rate(action_value), action_value]]

gen.set_generate_actions_function(generate_actions_values)
gen.set_generate_children_function(generate_children_values)



                  
alg = Algo()
if False:
    for i in range(1,100,10):
        alg.set_parameters(gen, initial_state, i, GAMMA, False)
        res = alg.run(True)

        print("Resultats: ")
        print("Action: "+ str(gen.denormalize(res[0].action)))
        print("Lower Bound: " + str(gen.denormalize(res[1])))
        print("Upper Bound: " + str(gen.denormalize(res[2])))

alg.set_parameters(gen, initial_state, 50, GAMMA, False)
res = alg.run(False, False)

print("Resultats: ")
print("Action: "+ str(gen.denormalize(res[0].action)))
print("Lower Bound: " + str(gen.denormalize(res[1])))
print("Upper Bound: " + str(gen.denormalize(res[2])))
