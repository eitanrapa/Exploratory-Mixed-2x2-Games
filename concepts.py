#U is up, D is down, L is left, R is right
#Player 1 is the row player, having up and down choices
#Player 2 is the col player, having left and right choices
#c_l and c_r are Player 1's payoff differences
#d_u and d_d are Player 2's payoff differences
#p_u and p_d are Player 1's choice probability for Up and Down
#q_l and q_r are Player 2's choice probability for Left and Right

def display_matrix(game):
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game
    top_left = a_l + c_l
    top_right = b_u + d_u
    bottom_left = b_d + d_d
    bottom_right = a_r + c_r
    print("(" + str(top_left) + "," + str(b_u) + ")     (" + str(a_r) + "," + str(top_right) + ")\n")
    print("(" + str(a_l) + "," + str(bottom_left) + ")     (" + str(bottom_right) + "," + str(b_d) + ")")

def nash_equilibrium(game):
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game
    check_conditions(game)
    p_u = d_d / (d_u + d_d)
    p_d = d_u / (d_u + d_d)
    q_l = c_r / (c_l + c_r)
    q_r = c_l / (c_l + c_r)
    return p_u,p_d,q_l,q_r

def impulse_balance_equilibrium(game):
    return

def quantal_response_equilibrium(game):
    return

def sample_n_equilibrium(game):
    return

def poisson_ch_equilibrium(game):
    return

#Check for negatives and fractions
def check_conditions(game):
    a_l, a_r, b_u, b_d, c_l, c_r, d_u, d_d = game
    if any(n < 0 for n in (a_l, a_r, b_u, b_d)):
        raise Exception("Base payoffs must be non-negative")
    if any(n <= 0 for n in (a_l, a_r, b_u, b_d)):
        raise Exception("Payoff differences must be positive")
    return None
