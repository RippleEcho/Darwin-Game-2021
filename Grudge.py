import random
def Grudge(S,R):
    if(len(R)>0):
        M=max(R,key=lambda item:item[1])[0]
        if M>3:
            return (4,3)
    return(3,4)
