import numpy as np
from sklearn.metrics import mean_squared_error
import concepts as concepts

# Explore large 2x2 matrix subset and calculate predictions from each stationary
# concept. 

#Check for negatives and fractions
def check_conditions(game):
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game
    if any(n < 0 for n in (a_l, a_r, b_u, b_d)):
       #Base payoffs must be non-negative
       return False
    if any(n <= 0 for n in (c_l, c_r, d_u, d_d)):
       #Payoff differences must be positive
       return False
    return True

def generate_games(number):
    '''
    Generate a list of all games up to some number. Games are represented as an eight-tuple. 
    '''
    games = []

    for i in range(number+1):
        for j in range(number+1):
            for k in range(number+1):
                for l in range(number+1):
                    for v in range(number+1):
                        for b in range(number+1):
                            for n in range(number+1):
                                for m in range(number+1):
                                    game = (i,j,k,l,v,b,n,m)
                                    if(check_conditions(game) == False):
                                        continue
                                    else:
                                        games.append(game)

    return games


def get_distance(pdxns_1, pdxns_2):
    '''
    Takes a list of predictions from two models as inputs. Returns a list of distances
    representing the difference between each of the games under the two
    different models. 
    '''
    dists = []

    for pdxn_1, pdxn_2 in zip(pdxns_1, pdxns_2):
        # For measuring distance between games, I decided to use mean squared
        # error (averaging the sum of the squared difference of each output
        # probability. 
        dists.append(np.mean((np.array(pdxn_1) - np.array(pdxn_2))**2))

    return np.array(dists)


def main(number):
    
    games = generate_games(number)

    #Get predictions for suitable games
    ibe_pdxns = [concepts.impulse_balance_equilibrium(game) for game in games]
    ne_pdxns = [concepts.nash_equilibrium(game) for game in games]
    qre_pdxns = [concepts.quantal_response_equilibrium(game) for game in games]
    
    distinguishability_values = []
    for i in range(len(games)):
        #Get distinguishability for each pdxn compared to each other
        distance_1 = (get_distance(ne_pdxns[i],qre_pdxns[i])[0],get_distance(ne_pdxns[i],qre_pdxns[i])[2])
        distance_2 = (get_distance(ne_pdxns[i],ibe_pdxns[i])[0],get_distance(ne_pdxns[i],ibe_pdxns[i])[2])
        distance_3 = (get_distance(ibe_pdxns[i],qre_pdxns[i])[0],get_distance(ibe_pdxns[i],qre_pdxns[i])[2])
        
        #Combine each difference
        total_distance_1 = np.sqrt(distance_1[0]**2 + distance_1[1]**2)
        total_distance_2 = np.sqrt(distance_2[0]**2 + distance_2[1]**2)
        total_distance_3 = np.sqrt(distance_3[0]**2 + distance_3[1]**2)
        
        #Combine all totals
        distinguishability = np.sqrt(total_distance_1**2 + total_distance_2**2 + total_distance_3**2)
        distinguishability_values.append(distinguishability)

    return distinguishability_values, games, (ibe_pdxns,ne_pdxns,qre_pdxns)