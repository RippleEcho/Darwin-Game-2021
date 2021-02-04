import random
def ExampleBot(own_moves,opp_moves):
    
    if(len(own_moves)>0):
    #len(moves) is the same as the number of turns completed this match
    
        #own previous move (last entry is [-1]).
        #Claim is [0], veto is [1]
        own_prev_claim = own_moves[-1][0]
        own_prev_veto = own_moves[-1][1]

        #opponent previous move(last entry is [-1]).
        #Claim is [0], veto is [1]
        opp_prev_claim = opp_moves[-1][0]
        opp_prev_veto = opp_moves[-1][1]
        
        #tit-for-tat 
        return(opp_prev_claim,opp_prev_veto)   
    return (3,0)
