from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from random import randint
from email import encoders
import numpy as np
import getpass
import smtplib
import os

fromaddr = input("From : ")
password = getpass.getpass()
toaddr = input("To : ")
subject = input("Subject : ")
body = input("Body : \n")
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

s = input("Secret Message : \n")
words = [i for i in s.split(' ')]
possible = [((i+6)*(i+6)) for i in range(15)]

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

attachment = open(file_name, "rb")
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
msg.attach(p)
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(fromaddr, password)
text = msg.as_string()
s.sendmail(fromaddr, toaddr, text)
s.quit()
attachment.close()

print("\nFile successfully sent to receiver for decoding\n")
