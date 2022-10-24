import numpy as np
from scipy.optimize import fsolve, least_squares

# U is up, D is down, L is left, R is right
# Player 1 is the row player, having up and down choices
# Player 2 is the col player, having left and right choices
# c_l and c_r are Player 1's payoff differences
# d_u and d_d are Player 2's payoff differences
# p_u and p_d are Player 1's choice probability for Up and Down
# q_l and q_r are Player 2's choice probability for Left and Right

def game_to_matrix(game):
    '''
    Convert values of a game back into a matrix.
    Matrix values are given in order LU_1, LU_2, RU_1, RU_2, 
    LD_1, LD_2, RD_1, RD_2.
    '''
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game
    
    RU_1, LU_2, LD_1, RD_2 = a_r, b_u, a_l, b_d
    LU_1 = a_l + c_l
    RU_2 = b_u + d_u
    LD_2 = b_d + d_d
    RD_1 = a_r + c_r

    return LU_1, LU_2, RU_1, RU_2, LD_1, LD_2, RD_1, RD_2


def matrix_to_game(matrix):
    '''
    Convert values of a matrix to values which are understood by the different
    models (a_l, a_r, etc.).

    a_l, a_r, b_u, and b_d need to be greater than or equal to zero.
    c_l, c_r, d_u, d_d need to be greater than zero. 
    '''
    LU_1, LU_2, RU_1, RU_2, LD_1, LD_2, RD_1, RD_2 = matrix
    
    a_r, b_u, a_l, b_d = RU_1, LU_2, LD_1, RD_2
    c_l = LU_1 - a_l
    d_u = RU_2 - b_u
    d_d = LD_2 - b_d
    c_r = RD_1 - a_r
    return a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d 

def display_matrix(matrix, cell_width=8):
    '''
    Print out a nice lil visual of the game in matrix form. 
    '''
    LU_1, LU_2, RU_1, RU_2, LD_1, LD_2, RD_1, RD_2 = matrix
    
    def spacer(n): # Adjust spacer size based on string length. 
        return ' ' * (cell_width - len(str(n)))
    
    row_1 = f'| {LU_1} ' + spacer(LU_1) + f'| {RU_1} ' + spacer(RU_1) + '|'
    row_2 = f'|' + spacer(LU_2) + f' {LU_2} |' +  spacer(RU_2)  + f' {RU_2} |'
    row_3 = f'| {LD_1} ' + spacer(LD_1) + f'| {RD_1} ' + spacer(RD_1) + '|'
    row_4 = f'|' + spacer(LD_2) + f' {LD_2} |' +  spacer(RD_2)  + f' {RD_2} |'
    
    divider ='-' * len(row_1)
    
    print(divider)
    print(row_1)
    print(row_2)
    print(divider)
    print(row_3)
    print(row_4)
    print(divider)

def display_game(game, cell_width=8):
    '''
    Print out a nice lil visual of the game in the more complicated form.
    '''
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game # transform_coords(game)
    
    def spacer(x=None, y=None): # Adjust spacer size based on string length. 
        if y is not None: # Accomodate the plus sign. 
            return ' ' * (cell_width - len(str(x)) - len(str(y)) - 3)
        else:
            return ' ' * (cell_width - len(str(x)))
    
    row_1 = f'| {a_l} + {c_l} ' + spacer(x=a_l, y=c_l) + f'| {a_r} ' + spacer(x=a_r) + '|'
    row_2 = f'|' + spacer(x=b_u) + f' {b_u} |' +  spacer(x=b_u, y=d_u)  + f' {b_u} + {d_u} |'
    row_3 = f'| {a_l} ' + spacer(x=a_l) + f'| {a_r} + {c_r} ' + spacer(x=a_r, y=c_r) + '|'
    row_4 = f'|' + spacer(x=b_d, y=d_d) + f' {b_d} + {d_d} |' +  spacer(x=b_d) + f' {b_d} |'
    
    divider ='-' * len(row_1)
    
    print(divider)
    print(row_1)
    print(row_2)
    print(divider)
    print(row_3)
    print(row_4)
    print(divider)


def nash_equilibrium(game):
    '''
    Just do the thing for a simple Nash equilibrium. 
    '''
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game
    p_u = d_d / (d_u + d_d)
    p_d = d_u / (d_u + d_d)
    q_l = c_r / (c_l + c_r)
    q_r = c_l / (c_l + c_r)
    return p_u, p_d, q_l, q_r

# We want this function to output a set of probabilities, just like the Nash
# Equilibrium, based on the 

def transform(s_i, payoff):
    '''
    Transforms a payoff based on the security level. 
    '''
    if payoff > s_i:
        payoff = payoff - (payoff - s_i)/2
    return payoff

def impulse_balance_equilibrium(game):
    '''
    Returns the predicted probability of each strategy choice according to the
    Impulse Balance Equilibrium model. 
    '''
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game # transform_coords(game)
    
    # Security levels for players 1 and 2.
    s_1 = max(min(a_l + c_l, a_r), min(a_l, a_r + c_r))
    s_2 = max(min(b_u, b_d + d_d), min(b_u + d_u, b_d))

    # Now need to transform the game.
    LU_1 = transform(s_1, a_l + c_l)
    LU_2 = transform(s_2, b_u)
    RU_1 = transform(s_1, a_r)
    RU_2 = transform(s_2, b_u + d_u)
    LD_1 = transform(s_1, a_l)
    LD_2 = transform(s_2, b_d + d_d)
    RD_1 = transform(s_1, a_r + c_r)
    RD_2 = transform(s_2, b_d)
    
    # Now calculate the magnitude of the impulses, which is the magnitude of the
    # forgone payoff in the transformed game. 
    c_l_star = max(LU_1 - s_1, LD_1 - s_1) # One of these two values should be 0
    c_r_star = max(RU_1 - s_1, RD_1 - s_1)
    d_u_star = max(LU_2 - s_2, RU_2 - s_2)
    d_d_star = max(LD_2 - s_2, RD_2 - s_2)
    
    c = c_l_star / c_r_star
    d = d_u_star / d_d_star
    
    p_u = np.sqrt(c) / (np.sqrt(c) + np.sqrt(d))
    q_l = 1 / (1 + np.sqrt(c * d))

    return p_u, 1 - p_u, q_l, 1 - q_l

# FIXME: adjust equations to include payoffs
def qre_eqs(x, l = 0, payoffs = []):
    # A = 3
    eq1 = x[0] - 1/(1 + np.exp(l * (1 - (1 + 3) * x[1])))
    eq2 = x[1] - 1/(1 + np.exp(l * (2 * x[0] - 1)))
    return [eq1, eq2]

def quantal_response_equilibrium(game, param=10):
    '''
    Quantal response equilibrium as function of chosen free parameter
    '''
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = transform_coords(game)
    # use Nash eq as initial guess
    p_u, p_d, q_l, q_r = nash_equilibrium(game)
    soln = fsolve(qre_eqs, [p_u, q_l], (param))
    qre_p_u = soln[0]
    qre_q_l = soln[1]
    return qre_p_u, 1 - qre_p_u, qre_q_l, 1 - qre_q_l

def sample_n_equilibrium(game):
    return

def poisson_ch_equilibrium(game):
    return
