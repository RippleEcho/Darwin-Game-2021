import random as r
from functools import reduce

def bayes(our_plays,their_plays):
    """A bot in the darwin game

    Args:
        our_plays ([(Int,Int)]): A history of our moves
        their_plays ([(Int,Int)]): A history of their moves
    Returns:
        move (Int,Int): Our moves
    """
    #Strategies I model each bot as one of these four strartegies
    bottom_feeder = tuple([20,20,20,1.3,1.3,1.3,0.5,0.5])
    cooperator = tuple([1,1,1,48,48,3,3,2])
    aggressor = tuple([1,1,1,4,4,24,24,24])
    random = tuple([1/8 for i in range(8)])
    
    def counter_bottom_feeder(our_plays,their_plays,p,n):
        yes = 1
        count = 2
        for move in their_plays:
            if  move[0] < 3:
                count+=1
                if move[0] < 2:
                    yes+=1
        rate = yes/count
        cond = 0.5
        if p/(p+n)>0.6:
            cond = r.random()
        if 0.5 < rate:
            return (6,4)
        else:
            return (5,4)
    
    def counter_cooperator(our_plays,their_plays,p,n):
        if len(our_plays) == 0:
            hardball = r.randint(0,1)
            if hardball == 0:
                return (3,r.randint(6,7))
            else:
                return (4,r.randint(6,7))
        yes = 1
        count = 2
        for move in their_plays:
            if  2 < move[0] < 5:
                count+=1
                if move[0] == 4:
                    yes+=1
        rate = yes/count
        cond = r.random()
        if p/(n+p)>0.6:
            if cond < rate:
                return (4,r.randint(6,7))
            else:
                return (3,r.randint(6,7))
        last = len(our_plays)-1
        score = (our_plays[last][0]+their_plays[last][0]) < 8
        maxim = our_plays[last][0]+their_plays[last][0] == 7
        if score and maxim:
            return their_plays[last]
        if score:
            if cond < rate:
                return (4,r.randint(6,7))
            else:
                return (3,r.randint(6,7))
        if not(score):
            return (3,r.randint(6,7))

    def counter_aggressor(our_plays,their_plays,p,n):
        return (2,5)

    def counter_random(our_plays,their_plays,p,n):
        if p/(p+n) > 0.5:
            cond = r.randint(0,1)
            if cond > 0:
                return (3,7)
            else:
                return (4,7)
        return (3,7)

    counter_strats = {bottom_feeder:counter_bottom_feeder, cooperator: counter_cooperator, aggressor: counter_aggressor, random: counter_random}
    close_veto = {bottom_feeder:[5,6,7],cooperator:[3,4] ,aggressor:[1,2], random:[3,4]}

  
    strats = [bottom_feeder,cooperator,aggressor,random]

    post_strat = {bottom_feeder:0.05, cooperator: 0.7, aggressor: 0.1, random: 0.05}
    post_close_veto = {bottom_feeder:(3,1), cooperator: (1,2), aggressor: (1,2), random: (1,1)}
    #Update priors
    for move in their_plays:
        for strat in strats:
            #Updating posterior on strategy model
            post_strat[strat] *= strat[move[0]]
            #Updating posterior on shady vetoing model
            (p,n) = post_close_veto[strat] 
            if close_veto[strat].count(move[1]) > 0:
                p+=1
            else:
                n+=1
            post_close_veto[strat] = (p,n)
        s = sum(post_strat.values())
        post_strat = {k:(p/s) for (k,p) in post_strat.items()}
    
    max_ap_strat = reduce(lambda x,y: x if x[1] > y[1] else y,post_strat.items())[0]
    cond_close_veto = post_close_veto[max_ap_strat]
    return counter_strats[max_ap_strat](our_plays,their_plays,*cond_close_veto)

    
