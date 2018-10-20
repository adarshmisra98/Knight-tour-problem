import numpy as np
import os

prefixed = [filename for filename in os.listdir('.') if filename.startswith("Info")]
f = open(prefixed[0],"r")
str = ""
for w in f:
    str = str + w
f.close()

name = prefixed[0]
name = name[:-4]
vals = [x for x in name.split(" ")]
N = int(vals[1])
x = int(vals[2])
y = int(vals[3])

def safe(x,y,board,N):
	return (x < N and x >= 0 and y < N and y >= 0 and board[x][y] == 0)

def ifSolution(Board,N):
	for i in range(N):
		for j in range(N):
			if Board[i][j] == 0:
				return False
	return True

def degreecheck(posx,posy,moves,board,N):
	accessibility = 0
	for i in range(8):
		if safe(posx+moves[i][0],posy+moves[i][1],board,N):
			accessibility += 1
	return accessibility

def knightnextmoves(move,moves,board,N):
	positionx = move[0]
	positiony = move[1]
	accessibility = 8
	for i in range(8):
		Nextx = positionx + moves[i][0]
		Nexty = positiony + moves[i][1]
		NewAccessibility = degreecheck(Nextx,Nexty,moves,board,N)
		if safe(Nextx,Nexty,board,N) and NewAccessibility < accessibility:
			move[0] = Nextx
			move[1] = Nexty
			accessibility = NewAccessibility
	return

def method2(N,positionx,positiony):
    x = positionx
    y = positiony
    moveNumber = 2
    move = [positionx,positiony]
    moves = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
    Board = np.zeros([N,N])
    Board[positionx][positiony] = 1
    L = []
    for i in range(N*N):
        move[0] = positionx
        move[1] = positiony
        knightnextmoves(move,moves,Board,N)
        positionx = move[0]
        positiony = move[1]
        Board[positionx][positiony] = moveNumber
        moveNumber += 1
    Board[positionx][positiony] -= 1
    sol = ifSolution(Board,N)
    if sol:
        k = 1
        while k <= N*N:
            for i in range(N):
                for j in range(N):
                    if Board[i][j] == k:
                        L.append([i,j])
                        k += 1
    if(len(L)==0):
        print("Sorry decoding cannot be done with given information\n")
        exit()
    return Board , L

Board , L = method2(N,x,y)

k = 0
words = [i for i in str.split(" ")]
word_matrix = np.chararray((N,N), itemsize=100)
for i in range(N):
    for j in range(N):
        word_matrix[i][j] = words[k]
        k = k + 1

ans = ""
for i in range(len(L)):
    if(word_matrix[L[i][0]][L[i][1]].decode() == "-"):
        break
    ans = ans + word_matrix[L[i][0]][L[i][1]].decode() + " "

print(ans)
