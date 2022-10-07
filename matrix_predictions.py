from numpy import np
from sklearn.metrics import mean_squared_error

# Explore large 2x2 matrix subset and calculate predictions from each stationary
# concept. 

# For now, we will check only zero-sum games. Need to think of a good way to
# exhaustively check. Perhaps we can set a maximum payoff and just use a brute
# force approach. 

def generate_zero_sum_games(min_payoff, max_payoff):
    '''
    Generating zero-sum games limits the number of free parameters to four,
    instead of eight. 

    Generate a list of all zero-sum games limited by the given max_payoff and
    min_payoff. Games are represented as an eight-tuple. 
    '''
    games = []

    for i in range(min_payoff, max_payoff + 1):
        for j in range(min_payoff, max_payoff + 1):
            for k in range(min_payoff, max_payoff + 1):
                for l in range(min_payoff, max_payoff + 1):
                    games.append((i, 0 - i, j, 0 - j, k, 0 - k, l, 0 - l))

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


def main(min_payoff, max_payoff):
    
    games = generate_zero_sum_games(min_payoff, max_payoff)

    ibe_pdxns = [impulse_balance_equilibrium(game) for game in games]
    ne_pdxns = [nash_equilibrium(game) for game in games]

    # What should our strategy be for finding matrices which are very different
    # across all games? Some kind of exhaustive search? Maybe sort the games
    # from highest-lowest difference, and find the first one present in all the
    # lists?
