from datetime import datetime
import random
import math

#Tournament code is preliminary.
#Sum-first scoring

#import bots here
from AC34 import AC34
from AC33 import AC33
from AC43 import AC43
from Ran34 import Ran34
from Rando import Rando
from ExampleBot import ExampleBot
from Grudge import Grudge
from Piebot import Piebot
bot_list=[AC33, AC43, AC34, Ran34, Rando, ExampleBot, Grudge, Piebot]

#fill list with bots
def Setup(bot_list, init_copy, round_count):
    
    #format file I/O
    date=datetime.now().strftime('%Y-%m-%d')
    file=open(date+" Stats.txt" ,"a+")
    file.write(date)
    file.write("\n\n")
    file.close()
    
    #populate bot pool
    bot_counts=[]
    for i in range(len(bot_list)):
        bot_counts.append(init_copy)
        
    #run rounds
    pool_size = len(bot_list) * init_copy
    for Rnd in range(round_count):
        round_score = Round(bot_list, bot_counts)
        bot_counts = Judge(bot_list, round_score, pool_size)
        Write(Rnd, bot_list, round_score, bot_counts)
        #print(Rnd)
    print(bot_counts)             


def Write(round_num, bot_names, round_scores, bot_counts):
    date=datetime.now().strftime('%Y-%m-%d')

    #Human-readable file layed out per round
    file=open(date+" Stats.txt" ,"a+")
    if(round_num ==0):
        file.write(str(list(map(lambda x: x.__name__ , bot_list)))+"\n\n")
    file.write("Round: "+str(round_num+1)+"\n")
    file.write("Scores: "+str(round_scores)+"\n")
    file.write("Copies: "+str(bot_counts)+"\n")
    file.write("\n")
    file.close()

    #CSV file with round scores and copy numbers
    file=open(date+" Stats.csv" ,"a+")
    if(round_num ==0):
        file.write("Round #,Score,")
        for bot in bot_list:
            file.write(str(bot.__name__)+",")
        file.write(",Copies,")
        for bot in bot_list:
            file.write(str(bot.__name__)+",")
        file.write("\n")
    file.write(str(round_num)+","+str(sum(round_scores))+",")
    for score in round_scores:
        file.write(str(score)+",")
    file.write(","+str(sum(bot_counts))+",")
    for count in bot_counts:
        file.write(str(count)+",")
    file.write("\n")
    file.close()     
    
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
    
        #recover single int input
    elif (type(move) is int):
        return (move,0)

        #recover list into tuple
    elif (type(move) is list and type(move[0]) is int and type(move[1]) is int):
        return (move[0],move[1])
    
    else:
        #do not recover other non-tuples
        print(str(move) + "non-tuple")
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
        
        #score round
        if(A_move[0] + B_move[0] < 8):
            #Check vetos
            if(A_move[0] != B_move[1]):
                A_score += A_move[0]
              
            if(B_move[0] != A_move[1]):
                B_score += B_move[0]

        #Check sum   
        if(A_move[0] + B_move[0] < 8):
            
            #Check vetos 
            #score round
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
                
                                  
#Setup(bot_list,4,4)
Setup(bot_list,256,256)
                                  
