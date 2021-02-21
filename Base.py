from datetime import datetime
import random
import math

#Tournament code is preliminary.
#Sum-first scoring

#import bots here
from Brute import Brute
from NaiveBot import NaiveBot
from NiceBot import NiceBot
from WesBot import WesBot
from DarwinianEmptySeat import DarwinianEmptySeat
from Kind_Bot import Kind_Bot
from bayes import bayes
from bot import bot
from Goblin import Goblin
from Grudge import Grudge

bot_list=[Brute, Kind_Bot, bot, bayes, NaiveBot, NiceBot, WesBot, DarwinianEmptySeat, Goblin, Grudge]

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
    round_score=[]
    for i in range(len(bot_list)):
        bot_counts.append(init_copy)
        round_score.append(0)
    Write(0, bot_list, round_score, bot_counts)
    print(str(list(map(lambda x: x.__name__ , bot_list))))
        
    #run rounds
    pool_size = len(bot_list) * init_copy    
    for Rnd in range(round_count):
        if Rnd%4 == 0:
            print(bot_counts)
        print(str(Rnd)+" / "+str(round_count))
        round_score = Round(bot_list, bot_counts)
        bot_counts = Judge(bot_list, round_score, pool_size)
        Write(Rnd+1, bot_list, round_score, bot_counts)
        if(max(bot_counts)>(pool_size*3/4)):
            print("break") 
            break;
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
    
    #correct out of range ints
    lim = lambda m: min(max(m,0),7)
    
    #type check for tuple or list of ints
    if (type(move) is tuple or list):
        if(type(move[0]) is int and type(move[1]) is int):
            for n in move:
                n=lim(n)
            return (move[0], move[1])
        
    #recover single int input    
    elif (type(move) is int):
        return (lim(move),0)

    #do not recover other non-tuples
    return (0,0)

def Match(A_bot, B_bot, turns_left):
    A_score=0
    B_score=0
    A_moves=[]
    B_moves=[]
    while (turns_left>0):
        turns_left -= 1

        #get bot moves based on existing move lists
        A_move=Limit(A_bot(A_moves, B_moves))
        B_move=Limit(B_bot(B_moves, A_moves))
        
        #check sums (Sum-first scoring)
        if(A_move[0] + B_move[0] < 8):
            #Check vetos
            if(A_move[0] != B_move[1]):
                A_score += A_move[0]
              
            if(B_move[0] != A_move[1]):
                B_score += B_move[0]
        
        #append move lists            
        A_moves.append(A_move)
        B_moves.append(B_move)
        
    return(A_score, B_score, A_moves, B_moves)
                 
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

def Compare(bot_list, matches):
    print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    for i in bot_list:
        for j in bot_list:
            bot_score=0
            bot_claims=[]
            bot_vetoes=[]
            for n in range (144):
                bot_claims.append([0,0,0,0,0,0,0,0])
                bot_vetoes.append([0,0,0,0,0,0,0,0])
            for k in range (matches):
                turns=random.randint(112,144)
                score=Match(i,j,turns)
                bot_score+=score[0]
                for m in range(len(score[2])):
                    bot_claims[m][score[2][m][0]]+=1
                    bot_vetoes[m][score[2][m][1]]+=1
                print_score=round(bot_score/matches,4)
            WriteMoves((str(i.__name__),str(j.__name__)),bot_claims,bot_vetoes,print_score)
            print(str(i.__name__)+" vs. " + str(j.__name__)+ " score: " + str(print_score))
    print(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
def WriteMoves(botnames, claims, vetoes, score):
    date=datetime.now().strftime('%Y-%m-%d')
    file=open(date+" Details.csv" ,"a+") 
    file.write(str(botnames[0])+",vs,"+str(botnames[1]))
    file.write("\n")
    file.write("Avg,Score:,"+str(score)+"\n\n")
    file.write("Claims,,Turn:,")
    for t in range(144):
        file.write(str(t+1)+",")
    file.write("\n")
    for r in range(8):
        file.write(","+str(r)+",,")
        for c in claims:
            file.write(str(c[r])+",")
        file.write("\n")
    file.write("\n")    
    file.write("Vetoes,Turn:,")
    for t in range(144):
        file.write(str(t+1)+",")
    file.write("\n")
    for r in range(8):
        file.write(","+str(r)+",,")
        for v in vetoes:
            file.write(str(v[r])+",")
        file.write("\n")
    file.write("\n")
    file.close()   
            
Compare(bot_list, 4096)
#Setup(bot_list,4096,256)
                                  
