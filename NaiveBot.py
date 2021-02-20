#This is the NaiveBot submitted by Johnny, from the Bayesian Conspiracy
#Discord.

def NaiveBot (MyMoves,EnemyMoves):

    #begin establishing turn number
    EnemySize = len(EnemyMoves)
    MySize = len(MyMoves)
    #end establishing turn number


    #beginning of ball-taking-home protocol
    if (MySize > 49):
        MyTotal = 0
        for count in range(MySize):
            if ((MyMoves[count][0] + EnemyMoves[count][0]) < 8):
                if (MyMoves[count][0] != EnemyMoves[count][1]):
                    MyTotal += MyMoves[count][0]
        if (MyTotal < 150):
            return (7,0)
    #end of ball-taking-home protocol
    

    #beginning of opening move
    if MySize == 0:
        import random
        decider = random.randint(1,2)
        if decider == 1:
            return (1,3)
        if decider == 2:
            return (6,4)
    #end of opening moves


    #beginning of last-move-check
    lastmove = EnemyMoves[EnemySize - 1][0]
    MyLastMove = MyMoves[MySize - 1][0]
    #end of last-move check


    #beginning of cooperative moves
    if MyLastMove == 0 and lastmove == 7:
        return (7,3)
    if MyLastMove == 1 and lastmove == 6:
        return (6,4)
    if MyLastMove == 2 and lastmove == 5:
        return (5,3)
    if MyLastMove == 3 and lastmove == 4:
        return (4,6)
    if MyLastMove == 4 and lastmove == 3:
        return (3,1)
    if MyLastMove == 5 and lastmove == 2:
        return (2,3)
    if MyLastMove == 6 and lastmove == 1:
        return (1,4)
    if MyLastMove == 7 and lastmove == 0:
        return (0,3)
    #end of cooperative moves


    #beginning of random moves
    import random
    if MyLastMove == 1 and lastmove == 1:
        decider = random.randint(1,2)
        if decider == 1:
            return (1,3)
        if decider == 2:
            return (6,4)

    if MyLastMove == 2 and lastmove == 2:
        decider = random.randint(1,2)
        if decider == 1:
            return (2,4)
        if decider == 2:
            return (5,3)

    if MyLastMove == 3 and lastmove == 3:
        decider = random.randint(1,2)
        if decider == 1:
            return (4,6)
        if decider == 2:
            return (3,1)

    if MyLastMove == 4 and lastmove == 4:
        decider = random.randint(1,2)
        if decider == 1:
            return (4,6)
        if decider == 2:
            return (3,1)

    if MyLastMove == 5 and lastmove == 5:
        decider = random.randint(1,2)
        if decider == 1:
            return (5,3)
        if decider == 2:
            return (2,4)

    if MyLastMove == 6 and lastmove == 6:
        decider = random.randint(1,2)
        if decider == 1:
            return (6,3)
        if decider == 2:
            return (1,4)

    if MyLastMove == 7 and lastmove == 7:
        decider = random.randint(1,2)
        if decider == 1:
            return (7,3)
        if decider == 2:
            return (0,4)
    #end of random moves


    #beginning of confusion move
    return (random.randint(1,7),random.randint(1,7))
    #end of confusion move


    #end of program.
