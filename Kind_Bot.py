"""Darwin Game Bot
Plays nicely with itself maximizing expected score in self play
"""
import random
import numpy as np
#import matplotlib.pyplot as plt
def Kind_Bot(own_moves,opp_moves):
    """
    The bot, takes in earlier moves
    """
    roundn=len(own_moves)
    def uncertain():
        """Plays the opening until asymmetry is obtained and non deterministic algorithms can be used
        """
        idenlist=[0,1,2,5,6,7]
        veto=random.choice(idenlist)
        prob=random.uniform(0,1)
        if prob<0.14005:
            move=4
        else:
            move=3
        return ( move, veto )
    def is_me(own,opp):
        """
        Returns if it is possible the opponent is running this code
        """
        roundm=len(opp)
        for i in range(0,roundm-2):
            if opp[i]!=own[i]:
                return False
        if opp[roundm-1][0] in [3,4]:
            if opp[roundm-1][1] in [0,1,2,5,6,7]:
                return True
        return False
    if roundn<1:
        """the starting moves"""
        return uncertain()
    if is_me(own_moves,opp_moves):
        #If the opponent is me i act this way
        if own_moves[roundn-1]==opp_moves[roundn-1]:
            #If i can be playing myself and our moves have been the same thus far
            return uncertain()
        if own_moves[roundn-1][0]!=opp_moves[roundn-1][0]:
            """if our ask was different"""
            return ( opp_moves[roundn-1][0],1 )
        if own_moves[roundn-1][1]<opp_moves[roundn-1][1]:
            """if our veto was different"""
            return ( 4,1 )
        else:
            return ( 3,1 )
    #Find the first place where the asks sum to 7
    def first7(own, opp):
        """
        finds the first round that sums to 7
        """
        for i in range(len(opp)):
            if own[i][0]+opp[i][0]==7:
                return i
        return 200
    f7=first7(own_moves,opp_moves)
    #eat pibot
    def Is_Pi(opp):
        """is the opponent pibot"""
        e ="255760521305053551246527734254200471723636166134705407470551551265170233101050620637674622347347044466373713722774330661414353543664033100253542141365517370755272577262541110317650765740633550205306625"
        pi=     "311037552421026430215142306305056006701632112201116021051476307200202737246166116331045051202074616150023357371243154746472206154601260515574457424156477411526655524341105711026653546113637543364230413"
        for i in range(len(opp)):
            if opp[i][0]!=int(pi[i]):
                return False
            if opp[i][1]!=int(e[i]):
                return False
        return True
    def Play_Pi(opp):
        e ="255760521305053551246527734254200471723636166134705407470551551265170233101050620637674622347347044466373713722774330661414353543664033100253542141365517370755272577262541110317650765740633550205306625"
        pi=     "311037552421026430215142306305056006701632112201116021051476307200202737246166116331045051202074616150023357371243154746472206154601260515574457424156477411526655524341105711026653546113637543364230413"
        if int(pi[len(opp)])+int(e[len(opp)])!=7:
            return (7-int(pi[len(opp)]),0)
        else:
            return (6-int(pi[len(opp)]),0)
    if Is_Pi(opp_moves):
        return Play_Pi(opp_moves)
    #Figure out if playing myself or a nice bot
    Is_Good=True
    Is_Ok=True
    Is_Evil=False
    if f7==200:
        #Playing myself above code will deal with it, if we havent added to 7 and more than 5 moves have gone i assume you arent nice
        Is_Good=False
        if roundn>5:
            Is_Ok=False
    else:
        #If we have achieved a 7 i expect us to keep looping 7 if it is me or titfortat like so failing that it is neither
        for i in range(f7+1,len(opp_moves)):
            if own_moves[i][0]+opp_moves[i][0]!=7:
                Is_Good=False
                Is_Ok=False
            if opp_moves[i][1]!=1:
                Is_Good=False
            if opp_moves[i][1]==own_moves[i][0]:
                Is_Ok=False
                Is_Evil=True
    if Is_Good:
        return opp_moves[-1]
    if Is_Ok:
        return opp_moves[-1]
    else:
        if Is_Evil:
            #if the opponent tries to veto my move act randomly but block them from doing well
            return (random.choice([4,5,6,7]),3)
        return (4,5)
n=10000
result=[]
moves1=[]
moves2=[]
# def Opponent_Bot(own_moves, opp_moves):
'''
perf=np.ones(20)*7
result2=[]
for j in range(n):
    moves1=[]
    moves2=[]
    for i in range(20):
        tempmove=Kind_Bot(moves1,moves2)
        moves2.append(Opponent_Bot(moves2,moves1))
        moves1.append(tempmove)
    cal1=np.array(moves1)
    cal2=np.array(moves2)
    sum1=cal1[:,0]+cal2[:,0]
    lessthan7= sum1<=perf
    res=cal1[:,0]*lessthan7
    res2=cal2[:,0]*lessthan7
    result.append(sum(res))
    result2.append(sum(res2))
'''
# for i in range(128):
#     tempmove=Opponent_Bot(moves1,moves2)
#     moves2.append(Opponent_Bot(moves2,moves1))
#     moves1.append(tempmove)
# cal1=np.array(moves1)
# cal2=np.array(moves2)
# sum1=cal1[:,0]+cal2[:,0]
# lessthan7= sum1<=perf
# res=cal1[:,0]*lessthan7
# res2=cal2[:,0]*lessthan7
# result.append(sum(res))
# result2.append(sum(res2))

# print(np.mean(result)/128)
# print(np.mean(result2)/128)
