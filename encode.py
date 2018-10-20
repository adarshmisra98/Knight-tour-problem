from random import randint
import numpy as np
import os

s = input()
words = [i for i in s.split(' ')]
possible = [i*i for i in range(20)]

N = len(words)
i = 0
while(N>possible[i]):
    i = i +1
N = i+1
x = randint(0,N-1)
y = randint(0,N-1)

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
        print("Sorry encoding cannot be done with given information\n")
        exit()
    return Board , L

Board , L = method2(N,x,y)

j = 0
word_matrix = np.chararray((N,N) , itemsize = 100)

for i in range(len(L)):
    if(j<len(words)):
        word_matrix[L[i][0]][L[i][1]] = words[j]
    else:
        word_matrix[L[i][0]][L[i][1]] = '-'
    j = j +1

st = ""
for i in range(N):
    for j in range(N):
        st = st + word_matrix[i][j].decode() + " "

prefixed = [filename for filename in os.listdir('.') if filename.startswith("Info")]
for i in range(len(prefixed)):
    os.remove(prefixed[i])

file_name = "Info " + str(N) + " " + str(x) + " " + str(y) + ".txt"
f = open(file_name,"w+")
f.write(st)
f.close()
