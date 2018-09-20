from time import time
import numpy as np
import pygame
import sys
from pygame.locals import *
import tkinter
from tkinter import *
from tkinter import messagebox

def IsSafe(x,y,board,N):
	return (x < N and x >= 0 and y < N and y >= 0 and board[x][y] == 0)

def IsSafeBacktrack(x,y,board,N):
	return (x < N and x >= 0 and y < N and y >= 0 and board[x][y] == -1)

def backtrack(x,y,N,start_time):
	dx=[2, 1, -1, -2, -2, -1, 1, 2]
	dy=[1, 2, 2, 1, -1, -2, -2, -1]
	sol=np.zeros([N,N])
	for i in range(N):
		for j in range(N):
			sol[i][j]=-1
	sol[x][y]=0;
	foundSolution=solveUtil(x,y,1,sol,N,dx,dy)
	for i in range(N):
		for j in range(N):
	 		if sol[i][j] == -1:
	 			foundSolution=False
	if foundSolution == False :
		t.insert(tkinter.END,"Couldn't find a solution")
		t.tag_config("center",justify='center')
		t.tag_add("center", "1.0",tkinter.END)
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
		return
	end_time = time()
	r = "Time taken to execute the algorithm " + str(round((end_time-start_time)*1000,2)) + " ms"
	t.insert(tkinter.END,r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	k = 0
	L=[]
	while k <= N*N-1:
		for i in range(N):
			for j in range(N):
				if sol[i][j] == k:
					L.append([i,j])
					k += 1
	if(N<=10):
		board = np.zeros((N,N))
		k = 0
		for i in range(len(L)):
			board[L[i][0]][L[i][1]] = k
			k = k+1
		j = ""
		for i in range(N):
			for k in range(N):
				j = j + str(round(int(board[i][k] + 1),0))+ "\t"
			j = j + "\n"
		show1.insert(tkinter.END,"Tracing path in NxN matrix \n")
		show1.tag_config("center",justify='center')
		show1.tag_add("center", "1.0",tkinter.END)
		values.insert(tkinter.END, j)
		values.tag_add("center", "1.0",tkinter.END)
	else:
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
	if N <= 32 :
		graphicTour(N,L)
	return

def solveUtil(positionx,positiony,movei,sol,N,dx,dy):
	if(movei==N*N):
		return True
	for i in range(8):
		Nextx = positionx + dx[i]
		Nexty = positiony + dy[i]
		if (IsSafeBacktrack(Nextx,Nexty,sol,N)):
			sol[Nextx][Nexty]=movei
			if(solveUtil(Nextx,Nexty,movei+1,sol,N,dx,dy)==True):
				return True
			sol[Nextx][Nexty]=-1
	return False

def checkAccessibility(posx,posy,moves,board,N):
	accessibility = 0
	for i in range(8):
		if IsSafe(posx+moves[i][0],posy+moves[i][1],board,N):
			accessibility += 1
	return accessibility

def getNextMoves(move,moves,board,N):
	positionx = move[0]
	positiony = move[1]
	accessibility = 8
	for i in range(8):
		Nextx = positionx + moves[i][0]
		Nexty = positiony + moves[i][1]
		NewAccessibility = checkAccessibility(Nextx,Nexty,moves,board,N)
		if IsSafe(Nextx,Nexty,board,N) and NewAccessibility < accessibility:
			move[0] = Nextx
			move[1] = Nexty
			accessibility = NewAccessibility
	return

def graphicTour(N,LeftCoordinate):
	Knight = pygame.image.load("knight.png")
	pygame.init()
	screen = pygame.display.set_mode((32*N,32*N))
	pygame.display.set_caption("Knight's Tour")
	background = pygame.image.load("chess.png")
	index = 0
	font = pygame.font.SysFont("comicsansms", 22)
	text = []
	Floor = []
	while True:
		screen.blit(background,(0,0))
		if index < N*N:
			screen.blit(Knight,(LeftCoordinate[index][0]*32,LeftCoordinate[index][1]*32))
			text.append(font.render(str(index+1),True,(255,255,255)))
			Floor.append(text[index].get_rect())
			Floor[index].center = (LeftCoordinate[index][0]*32+16,LeftCoordinate[index][1]*32+16)
			index += 1
		else:
			screen.blit(Knight,(LeftCoordinate[index-1][0]*32,LeftCoordinate[index-1][1]*32))
			pygame.display.quit()
			pygame.quit()
			return
		for x in range(8000000):
			pass
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
		for i in range(index):
			screen.blit(text[i],Floor[i])
		pygame.display.update()

def ifSolution(Board,N):
	for i in range(N):
		for j in range(N):
			if Board[i][j] == 0:
				return False
	return True

def basics():
	values.delete(1.0,tkinter.END)
	t.delete(1.0,tkinter.END)
	show1.delete(1.0,tkinter.END)
	i = e1.get()
	j = e2.get()
	k = e3.get()
	if(i.isdigit() and j.isdigit() and k.isdigit()):
		N = int(float(i))
		positionx = int(float(j))
		positiony= int(float(k))
		return N , positionx , positiony
	else:
		return -1 , -1 , -1

def check(a,b,c):
	r = ""
	if(e1.get().isdigit()==False):
		r = "Enter positive integral value in first field"
	elif(e2.get().isdigit()==False):
		r = "Enter positive integral value in second field"
	else:
		r = "Enter positive integral value in third field"
	t.insert(tkinter.END,r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	values.insert(tkinter.END,"")
	values.tag_add("center", "1.0",tkinter.END)
	return

def validity(a,b,c):
	r = ""
	if(b<0 and b>=N):
		r = "Value of positionx is out of bounds"
	elif(c<0 and c>=N):
		r = "Value of positiony is out of bounds"
	else:
		return True
	t.insert(tkinter.END,r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	values.insert(tkinter.END,"")
	values.tag_add("center", "1.0",tkinter.END)
	return False

def method1():
	N , positionx , positiony = basics()
	if(N==-1 and positionx==-1 and positiony==-1):
		check(N,positionx,positiony)
		return
	if(validity(N,positionx,positiony)==False):
		return
	start_time = time()
	backtrack(positionx,positiony,N,start_time)
	return

def method2():
	N , positionx , positiony = basics()
	if(N==-1 and positionx==-1 and positiony==-1):
		check(N,positionx,positiony)
		return
	if(validity(N,positionx,positiony)==False):
		return
	start_time = time()
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
		getNextMoves(move,moves,Board,N)
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
	else:
		moves = [[2,1],[-2,1],[2,-1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]
		Board = np.zeros([N,N])
		positionx = x
		positiony = y
		Board[positionx][positiony] = 1
		L = []
		moveNumber = 2
		move = [positionx,positiony]
		for i in range(N*N):
			move[0] = positionx
			move[1] = positiony
			getNextMoves(move,moves,Board,N)
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
	if len(L) == 0:
		r = "Couldn't find a solution"
		t.insert(tkinter.END,r)
		t.tag_config("center",justify='center')
		t.tag_add("center", "1.0",tkinter.END)
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
		return
	end_time = time()
	if(N<=10):
		board = np.zeros((N,N))
		k = 0
		for i in range(len(L)):
			board[L[i][0]][L[i][1]] = k
			k = k + 1
		j = ""
		for i in range(N):
			for k in range(N):
				j = j + str(round(int(board[i][k] + 1),0))+ "\t"
			j = j + "\n"
		show1.insert(tkinter.END,"Tracing path in NxN matrix \n")
		show1.tag_config("center",justify='center')
		show1.tag_add("center", "1.0",tkinter.END)
		values.insert(tkinter.END, j)
		values.tag_add("center", "1.0",tkinter.END)
	else:
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
	r = "Time taken to execute the algorithm " + str(round((end_time-start_time)*1000,2)) + " ms"
	t.insert(tkinter.END,r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	if N <= 32:
		graphicTour(N,L)
	return

def group_info():
	t = "Adarsh Misra : 201601004\n"
	t = t + "Nishi Doshi     : 201601408\n"
	t = t + "Smit Shah       : 201601410\n"
	messagebox.showinfo("Group Members",t)
	return

m = tkinter.Tk()
m.geometry("550x650")
m.title('Knight\'s Tour')
heading = tkinter.Text(m,width=50,height=2)
a = tkinter.Label(m,width=25, text='Value of N')
b = tkinter.Label(m,width=25, text='Value of x')
c = tkinter.Label(m,width=25, text='Value of y')
e1 = tkinter.Entry(m,width=25)
e2 = tkinter.Entry(m,width=25)
e3 = tkinter.Entry(m,width=25)
b1 = tkinter.Button(m, text='Backtracking Algorithm',width=25, command=method1)
b2 = tkinter.Button(m, text='Warnsdorff\'s Algorithm', width=25, command=method2)
b3 = tkinter.Button(m, text='Creater\'s Info', width=25,command=group_info)
show = tkinter.Text(m,width=75,height=2)
t = tkinter.Text(m,width=75,height=1)
show1 = tkinter.Text(m,width=75,height=1)
values = tkinter.Text(m,width=75)
heading.insert("1.0","Knight\'s Tour Analysis \n Enter Values for running the algorithm")
heading.tag_config("center",justify='center')
heading.tag_add("center", "1.0",tkinter.END)
show.insert("1.0","Results \n Time analysis \n")
show.tag_config("center",justify='center')
show.tag_add("center", "1.0",tkinter.END)
e1.insert(tkinter.END,'4')
e2.insert(tkinter.END,'0')
e3.insert(tkinter.END,'0')
heading.grid(row=0,column=0,columnspan=3)
a.grid(row=1,column=0)
b.grid(row=2,column=0)
c.grid(row=3,column=0)
e1.grid(row=1, column=2)
e2.grid(row=2, column=2)
e3.grid(row=3, column=2)
b1.grid(row=4,column=0)
b2.grid(row=4,column=2)
show.grid(row=5,column=0,columnspan=3)
t.grid(row=6,column=0,columnspan=3)
show1.grid(row=7,column=0,columnspan=3)
values.grid(row=8,column=0,columnspan=3)
b3.grid(row=9,column=2)
m.mainloop()
