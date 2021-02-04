from datetime import datetime
import random
import math

#Tournament code is preliminary.
#final version will contain code for exporting results

#import bots here
from AC33 import AC33
from AC34 import AC34
from AC43 import AC43
from Rando import Rando
from ExampleBot import ExampleBot
from Grudge import Grudge
bot_list=[AC33,AC34,AC43,Rando, ExampleBot, Grudge]

#fill list with bots
def Setup(bot_list, init_copy, round_count):
    #populate bot pool
    bot_counts=[]
    for i in range(len(bot_list)):
        bot_counts.append(init_copy)
        
    #run rounds
    pool_size = len(bot_list) * init_copy
    for Rnd in range(round_count):
        round_score = Round(bot_list, bot_counts)
        bot_counts = Judge(bot_list, round_score, pool_size)
        print(bot_counts)
    #print(bot_counts)             
    
def Limit(move):
    #type check for tuple of ints
    if (type(move) is tuple and type(move[0]) is int and type(move[1]) is int):
        for n in move:
            #recover out of range ints
            if n>7:
                n=7
            if n<0:
                n=0
        return move
    else:
        #do not recover non-tuples
        return (0,0)

def Match(A_bot, B_bot, turns_left):
    A_score=0
    B_score=0
    A_moves=[]
    B_moves=[]
    while (turns_left>0):
        turns_left -= 1
        
        A_move=Limit(A_bot(A_moves, B_moves))
        B_move=Limit(B_bot(B_moves, A_moves))
        #print(A_move)
        #print(B_move)
        #score round
        if(A_move[0] + B_move[0] < 8):
            #Check vetos
            if(A_move[0] != B_move[1]):
                A_score += A_move[0]
              
            if(B_move[0] != A_move[1]):
                B_score += B_move[0]
        #append move lists            
        A_moves.append(A_move)
        B_moves.append(B_move)
    return(A_score, B_score)
                 
def Round (bot_list, bot_counts): #
    #inputs: bots, botcounts
    #outputs: points for bots for that round
    bot_pool=[]
    bot_total_score=[]
    for i in range (len(bot_list)):
        bot_total_score.append(0)
        for j in range(bot_counts[i]):
            bot_pool.append(i)
            
    #shuffle bot pool      
    bot_pool=random.sample(bot_pool,len(bot_pool))
    for k in range(0, len(bot_pool),2):
        
        #setup matches
        A_bot = bot_list[bot_pool[k]]
        B_bot = bot_list[bot_pool[k+1]]
        turns=random.randint(112,144)
        
        #run matches
        match_score= Match(A_bot, B_bot, turns)
        
        #score matches
        bot_total_score[bot_pool[k]]+= match_score[0]
        bot_total_score[bot_pool[k+1]]+= match_score[1]
    return(bot_total_score)

def Judge (bot_list, bot_points, pool_size):
    #inputs: bots, bot points, total pool size
    #outputs: new bot counts
    bot_counts=[]
    
    #zero contingency
    if(sum(bot_points)==0):
        for i in range(len(bot_list)):
            bot_counts.append(int(pool_size/len(bot_list)))
            #even distribution
            return(bot_counts)
        
    for j in range(len(bot_list)):
        #first count as fraction of total points, rounded down
        first_count=int(math.floor(bot_points[j]/sum(bot_points)*pool_size))
        bot_counts.append(first_count)
        
    #determine bot with lowest ratio of copies:points
    #add one copy of that bot to the pool
    #repeat until pool is filled
    while(sum(bot_counts)<pool_size):
        bot_to_add=random.randint(0,len(bot_list))
        init_need=1.00
        for k in range(len(bot_list)):
            #do not account for zero-scoring bots
            if(bot_points[k]==0):
                case_need=1.00
            else:
                #ratio of copies:points
                case_need=float(bot_counts[k]/bot_points[k])
            if(case_need<init_need and bot_points[k]!=0):
                bot_to_add=k
                init_need=case_need
        bot_counts[bot_to_add]+=1
        
    return(bot_counts)
                
                                  

Setup(bot_list,256,256)
                                  
