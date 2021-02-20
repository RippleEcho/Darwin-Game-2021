#This is NiceBot. It attempts to always end the round with 69 points, and
#ideally force the opponent to have 69 points as well.
import random
def NiceBot (MyMoves,EnemyMoves):

    #begin establishing turn number
    EnemySize = len(EnemyMoves)
    MySize = len(MyMoves)
    #end establishing turn number


    #Opponent is an asshole check
    AssFlag = 0
    AssList = [p[1] for p in EnemyMoves if p[1] == 3]
    if (len(AssList) >= 4):
            AssFlag = 1
    #End of opponent is an asshole check


    #Beginning of MyTotal Calculator
    MyTotal = 0
    for count in range(MySize):
        if ((MyMoves[count][0] + EnemyMoves[count][0]) < 8):
            if (MyMoves[count][0] != EnemyMoves[count][1]):
                MyTotal = MyMoves[count][0] + MyTotal
    #End of MyTotal Calculator
             

    #Opponent is an Asshole Behavior
    if AssFlag == 1: #(if the opponent is trying to scum you out with vetos)
             if (MyTotal <= 62):
                 return [random.randint(1,7),random.randint(1,7)]
             if (MyTotal > 62):
                 MultipleCheck = (MyTotal % 3)
                 if (MultipleCheck == 1):
                     return [1,random.randint(1,7)]
                 if (MultipleCheck == 2):
                     return [2,random.randint(1,7)]
                 if (MultipleCheck == 3):
                     return [3,random.randint(1,7)]
    #End of Opponent is an asshole behavior

    
    #Beginning of ball-taking-home
    if (MyTotal == 69):
        return [0,7]
    #End of Ball-taking home


    #Beginning of usual move
    return [3,7]
    #End of usual move
