from time import time
import numpy as np
import pygame
import sys
from pygame.locals import *
import tkinter
from tkinter import *
from tkinter import messagebox

# Function checks if point is not visited and lies inside the board(used for Warnsdorff)
def safe(x,y,board,N):
	return (x < N and x >= 0 and y < N and y >= 0 and board[x][y] == 0)

# Function checks if point is not visited and lies inside the board(used for backtracking)
# Different functions because board is intialised with -1 and 0 in backtracking and wanrsdorff respectively
def safebacktrack(x,y,board,N):
	return (x < N and x >= 0 and y < N and y >= 0 and board[x][y] == -1)

def backtrack(x,y,N,start_time):
	# Declare different directions in which Knight moves
	dx=[2, 1, -1, -2, -2, -1, 1, 2]
	dy=[1, 2, 2, 1, -1, -2, -2, -1]
	# Initialize solution matrix with 0
	sol=np.zeros([N,N])
	# Initialize solution matrix with -1
	for i in range(N):
		for j in range(N):
			sol[i][j]=-1
	# Initialize first point as visited
	sol[x][y]=0;
	foundsol=solvebacktrack(x,y,1,sol,N,dx,dy)
	for i in range(N):
		for j in range(N):
	 		if sol[i][j] == -1:
	 			foundsol=False
	# If no solution found foundsol is false
	if foundsol == False :
		# UI
		t.insert(tkinter.END,"Couldn't find a solution")
		t.tag_config("center",justify='center')
		t.tag_add("center", "1.0",tkinter.END)
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
		return
	# Else solution exists
	# Mark the end time for algorithm completion 
	end_time = time()
	r = "Time taken to execute backtracking Algorithm " + str(round((end_time-start_time)*1000,2)) + " ms"
	t.insert(tkinter.END,r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	k = 0
	# L will contain the Knight's path
	L=[]
	# Search for 0 1 2 3 and append to L 
	while k <= N*N-1:
		for i in range(N):
			for j in range(N):
				if sol[i][j] == k:
					L.append([i,j])
					k += 1
	# Take the final coordinates in finalx and finaly 
	final_x,final_y = L[len(L)-1][0] , L[len(L)-1][1]
	# Check if tour is open/closed tour
	initial_x,initial_y = x,y
	# If knight can move in one step from last position to first position : Tour is closed
	# Else tour is open
	f = 0
	for i in range(8):
		if(final_x+dx[i] == initial_x and final_y+dy[i] == initial_y):
			f = 1
			break
	if (f==1):
		show1.insert(tkinter.END,"Closed Tour observed\n")
	else:
		show1.insert(tkinter.END,"Open Tour observed\n")
	# UI
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
		values.insert(tkinter.END, j)
		values.tag_add("center", "1.0",tkinter.END)
	else:
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
	values.tag_config("center",justify='center')
	show1.tag_config("center",justify='center')
	show1.tag_add("center", "1.0",tkinter.END)
	# If possible draw 
	if N <= 32 :
		printboard(N,L)
	return

# Backtracking's utility function
def solvebacktrack(positionx,positiony,movei,sol,N,dx,dy):
	# Breaking condition ie when all vertices are visited retrun true to indicate solution is found
	if(movei==N*N):
		return True
	# Try all the 8 possible directions 
	for i in range(8):
		Nextx = positionx + dx[i]
		Nexty = positiony + dy[i]
		# If the next point is safe mark the path index (movei) in sol matrix
		if (safebacktrack(Nextx,Nexty,sol,N)):
			sol[Nextx][Nexty]=movei
			# If the chosen point gave a solution return true,add 1 to path index and continue with the new pts
			if(solvebacktrack(Nextx,Nexty,movei+1,sol,N,dx,dy)==True):
				return True
			# Else mark as unvisited (-1)
			sol[Nextx][Nexty]=-1
	# Return false if no solution found
	return False

# Degree function for Warnsdorff Algo to find the min degree node 
def degreecheck(posx,posy,moves,board,N):
	# No of points that are accessible to this point 
	accessibility = 0
	for i in range(8):
	# Check all 8 points for validity and  update if valid 
		if safe(posx+moves[i][0],posy+moves[i][1],board,N):
			accessibility += 1
	return accessibility

# Take x and y from the pair move and travel in 8 directions using moves array 
def knightnextmoves(move,moves,board,N):
	positionx = move[0]
	positiony = move[1]
	# Max accesibility for a point 	
	accessibility = 8
	for i in range(8):
		Nextx = positionx + moves[i][0]
		Nexty = positiony + moves[i][1]
		# Update  the point 	with min Accessibility using NewAccessibility  variable 
		NewAccessibility = degreecheck(Nextx,Nexty,moves,board,N)
		if safe(Nextx,Nexty,board,N) and NewAccessibility < accessibility:
			move[0] = Nextx
			move[1] = Nexty
			accessibility = NewAccessibility
	return

# UI
def printboard(N,LeftCoordinate):
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

# If solution found return true for Warnsdorff
# Check if all board points are zero if yes solution found 
def ifSolution(Board,N):
	for i in range(N):
		for j in range(N):
			if Board[i][j] == 0:
				return False
	return True

# UI
def basics():
	values.delete(1.0,tkinter.END)
	t.delete(1.0,tkinter.END)
	show1.delete(1.0,tkinter.END)
	show.delete(1.0,tkinter.END)
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

# Validation
def validity(a,b,c):
	r = ""
	if(b<0 or b>=a):
		r = "Value of positionx is out of bounds"
	elif(c<0 or c>=a):
		r = "Value of positiony is out of bounds"
	else:
		return True
	t.insert("1.0",r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	values.insert(tkinter.END,"")
	values.tag_add("center", "1.0",tkinter.END)
	return False

# Backtracking setup function and start timer
def method1():
	N , positionx , positiony = basics()
	if(N==-1 and positionx==-1 and positiony==-1):
		check(N,positionx,positiony)
		return
	if(validity(N,positionx,positiony)==False):
		return
	start_time = time()
	show.insert("1.0","Results \n Time analysis \n")
	show.tag_config("center",justify='center')
	show.tag_add("center", "1.0",tkinter.END)
	backtrack(positionx,positiony,N,start_time)
	return

# Warnsdorff setup function 
def method2():
	# Input from UI
	N , positionx , positiony = basics()
	if(N==-1 and positionx==-1 and positiony==-1):
		check(N,positionx,positiony)
		return
	if(validity(N,positionx,positiony)==False):
		return
	show.insert("1.0","Results \n Time analysisn \n")
	show.tag_config("center",justify='center')
	show.tag_add("center", "1.0",tkinter.END)
	# Mark starting time
	start_time = time()
	x = positionx
	y = positiony
	moveNumber = 2
	move = [positionx,positiony]
	moves = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
	Board = np.zeros([N,N])
	# Mark visited 1 
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
	#Check is solution exists
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
	# Checking whether the tour is opened or closed 
	final_x,final_y = L[len(L)-1]
	initial_x,initial_y = positionx,positiony
	f = 0
	for i in range(8):
		if(final_x+moves[i][0] == initial_x and final_y+moves[i][1] == initial_y):
			f = 1
			break
	if (f==1):
		show1.insert(tkinter.END,"Closed Tour observed\n")
	else:
		show1.insert(tkinter.END,"Open Tour observed\n")
	# UI
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
		values.insert(tkinter.END, j)
		values.tag_add("center", "1.0",tkinter.END)
		values.tag_config("center",justify='center')
	else:
		values.insert(tkinter.END,"")
		values.tag_add("center", "1.0",tkinter.END)
	show1.tag_config("center",justify='center')
	show1.tag_add("center", "1.0",tkinter.END)
	r = "Time taken to execute Warnsdorff\'s Algorithm " + str(round((end_time-start_time)*1000,2)) + " ms"
	t.insert(tkinter.END,r)
	t.tag_config("center",justify='center')
	t.tag_add("center", "1.0",tkinter.END)
	if N <= 32:
		printboard(N,L)
	return

# Information about group members
def group_info():
	h = "Adarsh Misra : 201601004\n"
	h = h + "Nishi Doshi     : 201601408\n"
	h = h + "Smit Shah       : 201601410\n"
	messagebox.showinfo("Group Members",h)
	return

# Definitions pertaining to open and closed tour
def about():
	values.delete(1.0,tkinter.END)
	t.delete(1.0,tkinter.END)
	show1.delete(1.0,tkinter.END)
	show.delete(1.0,tkinter.END)
	show1.insert(tkinter.END,"Basic Definitions")
	h = "Open Tour : When kinght at final poisition in the tour cannot reach the \ninitial position in one move; open tour is observed\n"
	h = h + "Closed Tour : When kinght at final poisition in the tour reaches the \ninitial position in one move; open tour is observed\n"
	values.insert(tkinter.END,h)
	return

# To close the app
def close():
	m.destroy()

# Warnsdorff
def method2_2():
	N , positionx , positiony = basics()
	if(N==-1 and positionx==-1 and positiony==-1):
		check(N,positionx,positiony)
		return -1 , -1
	if(validity(N,positionx,positiony)==False):
		return -1 , -1
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
	if len(L) == 0:
		return -1 , -1
	end_time = time()
	final_x,final_y = L[len(L)-1]
	initial_x,initial_y = positionx,positiony
	f = 0
	for i in range(8):
		if(final_x+moves[i][0] == initial_x and final_y+moves[i][1] == initial_y):
			f = 1
			break
	return end_time-start_time , f

# Backtracking
def method1_2():
	N , positionx , positiony = basics()
	if(N==-1 and positionx==-1 and positiony==-1):
		check(N,positionx,positiony)
		return -1 , -1
	if(validity(N,positionx,positiony)==False):
		return -1 , -1
	start_time = time()
	x = positionx
	y = positiony
	dx=[2, 1, -1, -2, -2, -1, 1, 2]
	dy=[1, 2, 2, 1, -1, -2, -2, -1]
	sol=np.zeros([N,N])
	for i in range(N):
		for j in range(N):
			sol[i][j]=-1
	sol[x][y]=0;
	foundSolution=solvebacktrack(x,y,1,sol,N,dx,dy)
	for i in range(N):
		for j in range(N):
	 		if sol[i][j] == -1:
	 			foundSolution=False
	if foundSolution == False :
		return -1 , -1
	end_time = time()
	k = 0
	L=[]
	while k <= N*N-1:
		for i in range(N):
			for j in range(N):
				if sol[i][j] == k:
					L.append([i,j])
					k += 1
	final_x,final_y = L[len(L)-1][0] , L[len(L)-1][1]
	initial_x,initial_y = x,y
	f = 0
	for i in range(8):
		if(final_x+dx[i] == initial_x and final_y+dy[i] == initial_y):
			f = 1
			break
	return end_time-start_time , f

# To analyze both the methods for a given position 
def analyze():
	times , f = method2_2()
	if (f==-1 or times==-1):
		values.insert("1.0","Some error in inputs or algorithm does not support this algorithm")
		values.tag_config("center",justify='center')
		values.tag_add("center", "1.0",tkinter.END)
		return
	s = "Warnsdorff\'s Algorithm analysis \n"
	s = s + "Time taken to find answer : " + str(round(times*1000,4)) + "ms \n"
	if(f==1):
		s = s + "Closed Tour observed\n\n"
	else:
		s = s + "Open Tour observed\n\n"
	times2 , f2 = method1_2()
	if (f2==-1 or times2==-1):
		values.insert("1.0","Some error in inputs or algorithm does not support this algorithm")
		values.tag_config("center",justify='center')
		values.tag_add("center", "1.0",tkinter.END)
		return
	s = s + "Backtracking Algorithm analysis \n"
	s = s + "Time taken to find answer : " + str(round(times2*1000,4)) + "ms \n"
	if(f2==1):
		s = s + "Closed Tour observed\n"
	else:
		s = s + "Open Tour observed\n"
	show.insert("1.0","\n Results")
	show.tag_config("center",justify='center')
	show.tag_add("center", "1.0",tkinter.END)
	show1.insert("1.0","Time Analysis")
	show1.tag_config("center",justify='center')
	show1.tag_add("center", "1.0",tkinter.END)
	values.insert("1.0",s)
	values.tag_config("center",justify='center')
	values.tag_add("center", "1.0",tkinter.END)
	return

# UI
m = tkinter.Tk()
m.geometry("650x650")
m.title('Knight\'s Tour')
heading = tkinter.Text(m,width=50,height=2)
a = tkinter.Label(m,width=40,height=3, text='Value of N \n (No. of squares in a row or column in chessboard)')
b = tkinter.Label(m,width=40, height = 3,text='Value of x \n (Initial x poisition of knight on chessboard)')
c = tkinter.Label(m,width=40, height = 3, text='Value of y \n (Initial y position of knight on chessboard)')
e1 = tkinter.Entry(m,width=25)
e2 = tkinter.Entry(m,width=25)
e3 = tkinter.Entry(m,width=25)
b1 = tkinter.Button(m, text='Backtracking Algorithm',width=25, command=method1)
b2 = tkinter.Button(m, text='Warnsdorff\'s Algorithm', width=25, command=method2)
b3 = tkinter.Button(m, text='Creater\'s Info', width=25,command=group_info)
b4 = tkinter.Button(m, text='Basic Definitions',width=25,command=about)
b5 = tkinter.Button(m, text='Close',width=25,command=close)
b6 = tkinter.Button(m, text='Show Analysis',width=25,command=analyze)
show = tkinter.Text(m,width=75,height=2)
t = tkinter.Text(m,width=75,height=1)
show1 = tkinter.Text(m,width=75,height=2)
values = tkinter.Text(m,width=75,height=12)
heading.insert("1.0","Knight\'s Tour Analysis \n Enter Values for running the algorithm")
heading.tag_config("center",justify='center')
heading.tag_add("center", "1.0",tkinter.END)
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
b6.grid(row=9,column=0)
b5.grid(row=10,column=2)
b4.grid(row=10,column=0)
m.mainloop()
