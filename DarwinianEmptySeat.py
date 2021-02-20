import random
def DarwinianEmptySeat(own_moves,opp_moves):
    
    if(len(own_moves)>1):
    #len(moves) is the same as the number of turns completed this match
    
        #own previous move (last entry is [-1]).
        #Claim is [0], veto is [1]
        own_prev_claim = own_moves[-1][0]
        own_prev_veto = own_moves[-1][1]

        #opponent previous move(last entry is [-1]).
        #Claim is [0], veto is [1]
        opp_prev_claim = opp_moves[-1][0]
        opp_prev_veto = opp_moves[-1][1]
        
        if(len(own_moves)>2):
            if own_moves[-2][0] == opp_moves[-1][0] and own_moves[-2][1] == opp_moves[-1][1]:
                # Opponent appears to be TFTing, so make the move that would have best countered our previous move… so, veto our previous claim:
                new_veto = own_moves[-1][0]
                # and maximize our score
                new_claim = 7-own_moves[-1][0]
            else:
                new_claim = 3
                new_veto = 4
            return(new_claim,new_veto)
    # First move:
    return (3,7)
