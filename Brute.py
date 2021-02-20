import random
def Brute(S,R):
    L=len(S)
    P=lambda f: random.random()<f
    if L==0:
        if P(0.5):
            return (3,0)
        return (3,1)
    if L < 4:
        if (R[-1][0]==3 and R[-1][1]<2):
            if (S[-1][1] + R[-1][1] %2 ==1):
                if S[-1][1] == 0:
                    return (3,0)
                else:
                    return (4,0)
            else:
                if P(0.5):
                    return (3,0)
                return (3,1)         
    if S[-1][0] + R[-1][0] == 7:
        return (R[-1]) 
    if P(0.5):           
        return (4, R[-1][0])
    return (7-R[-1][1],R[-1][0])
