import random
def bluff_spot():
    player1_card = 0 #bluff, Q, HERO
    player2_card = 1 #bluff catcher, K, VILLIAN
    pot = 2 # 1 ante from each player
    bluff_size = 1
    breakeven_bluff_success_freq = bluff_size / (bluff_size + pot) #1/3
    bluffcatch_freq = 1 - breakeven_bluff_success_freq#0 ev bluff
    # bluffcatch_freq = 1 - .25 #underfolds
    # bluffcatch_freq = 1 - .40 #overfolds
    if random.random() < bluffcatch_freq:
        return -bluff_size # player2 calls and wins, player1 loses the bluff
    else:
        return pot # player2 folds and player1 wins the pot

def sim_bluff_spot():
    total = 0 #we're not including antes! just bluff spot in isolation
    iterations = 1000
    for i in range(iterations):
        total += bluff_spot()
        print('{0:0.2f}'.format(total/iterations))
        # print('{0:0.2f}'.format(total))
        # total = 0

def bluffcatch_spot():
    player1_card = 0 #bluff, Q, VILLIAN
    player2_card = 1 #bluff catcher, K, HERO
    pot = 2 # 1 ante from each player
    bet_size = 1
    bluff_freq = bet_size / (2*bet_size + pot)#.25
    # in AKQ game, if dealt 3 As and 3 Qs, bluff 1/3 of Q's
    # ie to find how often to bluff Q, x / (1 + x) = 1/4, x = 1/3
    # bluff_freq = .3 #overbluffing
    # bluff_freq = .2 #underbluffing
    if random.random() < bluff_freq:
        return pot+bet_size# player2 calls and wins pot + bluff
    else:
        return -bet_size # player2 calls and loses

def sim_bluffcatch_spot():
    total = 0 #we're not including antes! just bluff spot in isolation
    iterations = 1000
    for i in range(iterations):
        total += bluffcatch_spot()
        print('{0:0.2f}'.format(total/iterations))
        # print('{0:0.2f}'.format(total))
        # total = 0

def polarized_spot():
    player1_card = 2 if random.random() > 0.5 else 0
    player2_card = 1 #always a bluffcatcher
    ante = 1
    pot = 2*ante 
    bet_size = 1

    # equity is 50/50 split if always check down (or always bet/call)
    # bluff_freq = 0
    # bluffcatch_freq = 0
    # or always bet/call, note variance goes up
    # bluff_freq = 1
    # bluffcatch_freq = 1

    # best possible outcome is if we always bluff, they always fold
    # bluff_freq = 1
    # bluffcatch_freq = 0
    # # also good for us is if we never bluff, they always bluffcatch
    # bluff_freq = 0
    # bluffcatch_freq = 1

    #equilibrium
    #25% of overall range should be bluffs
    #half the time we have value
    bluff_freq = 1/3#3 times we have value, 1 time we bluff
    bluffcatch_freq = 1-1/3

    # bluff_freq = 1/2 #if one player deviates, other goes pure in other direction
    # bluffcatch_freq = 1#we bluff too much so villian pure calls

    # bluff_freq = 1/4 #if one player deviates, other goes pure in other direction
    # bluffcatch_freq = 0#we bluff too little so villian pure folds

    # at equilibrium, changing just one strategy has no affect on EV
    # bluff_freq = 1/3 #
    # bluffcatch_freq = 1#can pure fold, pure call, mix, doesn't matter

    if player1_card == 2: #we have value hand
        if random.random() < bluffcatch_freq: #they call and lose
            return pot+bet_size-ante
        else: #they fold, we win their ante
            return pot-ante
        # equivalent to EV calculation:
        # return pot + bet_size*bluffcatch_freq - ante
    else: #we are bluffing
        if random.random() < bluff_freq: #we choose to bluff
            if random.random() < bluffcatch_freq: #they call and we lose bet,ante
                return -bet_size-ante
            else: #they fold, we win their ante
                return pot-ante
        else: #we give up and always lose
            return -ante

def sim_polarized_spot():
    total = 0 #we're not including antes! just bluff spot in isolation
    iterations = 1000
    for i in range(iterations):
        total += polarized_spot()
        print('{0:.2f}'.format(total/iterations))
        # print('{0:.2f}'.format(total))
        # total = 0
if __name__ == "__main__":
    # sim_bluff_spot()
    # sim_bluffcatch_spot()
    sim_polarized_spot()