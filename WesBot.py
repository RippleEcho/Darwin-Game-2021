from random import getrandbits


def WesBot(ownMoves, oppMoves):
   roundNumber = len(ownMoves) + 1

   if roundNumber == 1:
      return (3, 4)

   previousRound = (ownMoves[-1], oppMoves[-1])
   TPR = previousRound[0][0] + previousRound[1][0]

   previousScore = 0

   if(previousRound[0][0] + previousRound[1][0] < 8):
      #veto check
      if(previousRound[0][0] != previousRound[1][1]):
         previousScore += previousRound[0][0]




   if roundNumber > 3:
      lastThreeOppMoves = oppMoves[-3:]

      lastThreeOppClaims = []
      for oppMove in lastThreeOppMoves:
         lastThreeOppClaims.append(oppMove[0])

      if lastThreeOppClaims == [0,0,0]:
         return (7,0)

      if lastThreeOppClaims == [1,1,1]:
         return (6,0)

      if [claim for claim in lastThreeOppClaims if claim <= 2]:
         return (5, 0)

   if 2<=roundNumber<=10:
      if (previousScore == 0) and (TPR != 8):
         return (4, 3)

      if TPR == 7:
         return (oppMoves[-1][0], 0)

      if TPR == 6:
         if getrandbits(1):
            return (oppMoves[-1][0] + 1, 0)
         else:
            return (oppMoves[-1][0], 0)

      if TPR == 8:
         if getrandbits(1):
            return (oppMoves[-1][0] - 1, 0)
         else:
            return (oppMoves[-1][0], 0)

      if TPR > 8:
         return (4, 3)

      if TPR < 6:
         return (4, 3)

   if roundNumber >= 11:
      if (previousScore == 0):
         return (4, 3)

      if TPR == 7:
         if oppMoves[-1][0] == 3:
            return (3, 3)

         return (oppMoves[-1][0], 0)

      return (3, 4)
