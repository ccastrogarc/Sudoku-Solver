from math import *
from random import *
import time
nmbrs = [int(1),int(2),int(3),int(4),int(5),int(6),int(7),int(8),int(9)]

#Reading the document + transforming into lists
with open('sudoku.txt', 'r') as f:
    lines = f.read()
    newlines = lines.rstrip()

y =[]
for i in range(0,9):
    x =[]
    for j in range(0, 9):
        x.append(int(newlines[j +(10*i)]))
    y.append(x)

#Printing sudoku input
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print(
      )
print('The input is:')
print(
      )
print(*y, sep = '\n')
print(
      )
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print(
      )
#Sector generation (0 downto 8 from left to right, up to down):
sectors = []
h = []
v = []
for k in range(0, 9):
    v = []
    h = []
    for i in range(0,3):
    
        for j in range(0,3):
            if k <= 2:
                h.append(y[i][j + (3*k)])
                
            if (k == 3) or (k == 4) or (k == 5):
                h.append(y[i+3][j + (3*(k-3))])
                
            if (k == 6) or (k == 7) or (k == 8):
                h.append(y[i+6][j + (3*(k-6))])
    sectors.append(h)

#Column generation (col list, 0 downto 8 from left to right):
col = []
for i in range(0,9):
    n = []
    for j in range(0,9):
        n.append(y[j][i])
    col.append(n)

def colgen(z):                  #Column update using str:
    col = []
    for i in range(0,9):
        n = []
        for j in range(0,9):
            n.append(z[j*9 + i])
        col.append(n)
    return col

def rowgen(z):                  #Row update using str:
    y = []
    for i in range(0,9):
        n = []
        for j in range(0,9):
            n.append(z[j+9*i])
        y.append(n)
    return y

#Sudoku string-shaped (0 downto 80, left to right, up to down):
str = []
for i in range(0,9):
    for j in range(0,9):
        str.append(y[i][j])
        
#Validity indicator, to remember original sudoku numbers (0 = to change, 1 = fixed):
val = []
for i in range(0,81):
    if str[i] == 0:
        val.append(int(0))
    else:
        val.append(int(1))

#sector in string form (0 downto 80, ranging from 0 to 8):
sl = [0, 0, 0, 1, 1, 1, 2, 2, 2,
      0, 0, 0, 1, 1, 1, 2, 2, 2,
      0, 0, 0, 1, 1, 1, 2, 2, 2,
      3, 3, 3, 4, 4, 4, 5, 5, 5,
      3, 3, 3, 4, 4, 4, 5, 5, 5,
      3, 3, 3, 4, 4, 4, 5, 5, 5,
      6, 6, 6, 7, 7, 7, 8, 8, 8,
      6, 6, 6, 7, 7, 7, 8, 8, 8,
      6, 6, 6, 7, 7, 7, 8, 8, 8]

#correcting variable w (horizontal coordinate, from 0 to 8):
def wunder(w): 
    underflow = True
    while underflow:
        w = w + 9
        if w >=0:
            underflow = False  
    return w

def wover(w): 
    overflow = True
    while overflow:
        w = w - 9
        if w <=8:
            overflow = False  
    return w

#######################################LOGIC#############################################
#Current solving method used in the code, called "backtracking".
unsolved = True                 #Defining constants outside the while loop
u = 0
w = 0
output = [[],[],[],[],[],[],[],[],[]]
start = time.process_time()
while unsolved:                 #Start of the solving loop
    if w <= -1:
        w = wunder(w)
    if u >= 81:
        break
    if val[u] == 0:             #Check if number can be edited
        h = floor(u/9)
        si = w + 3*h - 3*sl[u]
        str[u] += 1
        sectors[sl[u]][si] = str[u]
        col = colgen(str)
        y = rowgen(str)
        if (sectors[sl[u]].count(str[u]) <= 1) and (col[w].count(str[u]) <= 1) and (y[h].count(str[u]) <= 1):#Check if old number + 1 is valid
            if str[u] >= 10:    #If the number is 10, reset number to 0 and backtrack
                str[u] = 0
                sectors[sl[u]][si] = str[u]
                col = colgen(str)
                y = rowgen(str)
                backtrack = True
                while backtrack:#Backtracking loop, until it finds a number it can change
                    u -= 1
                    w -= 1
                    if val[u] == 0:
                        backtrack = False
                    else:
                        continue
            else:               #If the number is within the 3 laws and is not bigger than 10, move on to the next cell    
                u += 1
                w += 1
                if w >= 9:      #Correcting for a w bigger than 8
                    w = wover(w)
                if w <= -1:     #Correcting for a w smaller than 0
                    w = wunder(w)
        else:                   #If old number + 1 doesn't abide by rules, go back to the beginning of while loop to add another + 1
            u += 0              
            w += 0
    else:                       #If cell value is not to be edited (val from list = 1) then skip and go to next cell
        if val[u] == 1:
            u += 1
            w += 1
            if w >= 9:          #Correcting for a w bigger than 8
                w = wover(w)
            if w <= -1:         #Correcting for a w smaller than 0
                w = wunder(w)
        if u == 81:             #If it reaches the end of the sudoku str string, end the while loop
            unsolved = False

end = time.process_time()       #Recording time of end
for i in range(0,9):            #Generation of the output list to be displayed
    for j in range(0,9):
        output[i].append(str[j + 9*i])
timetaken = float('%.4g' % (end-start))
################################################################################################################################################################

#Presenting output list + time taken
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print(
      )
print('The final answer is:')
print(
      )
print(*output, sep = '\n')
print(
      )
print(f"with a runtime of {timetaken} seconds.")
print(
      )
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print(
      )
input("Press Enter to continue...")


'''
#############################################################################################################################################################
#Guessing Logic, slow at best, inaccurate at worst.
unsolved = True
output = [[],[],[],[],[],[],[],[],[]]
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
si = 0
i = 0
c = 0
errors = [0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0]
while unsolved:
    randomize = True
    while randomize:
        
        if i >= 81:
            randomize = False
            correcting = True
            i = 0
            break
        a = int(choice(numbers))
        if val[i] == 0:
            str[i] = a
            sectors[sl[i]][si] = str[i]
            col = colgen(str)
            y = rowgen(str)
            if (sectors[sl[i]].count(str[i]) <= 1) and (col[si].count(str[i]) <= 1) and (y[c].count(str[i]) <= 1):
                
                print("number assigned")
                i += 1   
            else:
                str[i] = 0
                print("error")
                i += 1
                
                print("repeat")
                
                continue
        else:
            i += 1
            print("skipped")
            #error.append(int(0))
            continue
        if i >= 81:
            randomize = False
            correcting = True
            i = 0
            break
        c = floor(i/9)
        q = i - 9*c
        si = q + 3*c - 3*sl[i]
    print(str)    
    while correcting:
        if i >= 81:
            randomize = True
            correcting = False
            i = 0
            break
        elif val[i] == 1:
            i += 1
        elif val[i] == 0:
            if str[i] != 0 and((sectors[sl[i]].count(str[i]) <= 0) and (col[si].count(str[i]) <= 0) and (y[c].count(str[i])) <= 0):
                errors[i] = int(0)
                i += 1
            else:
                print("correcting")
                str[i] = 0
                sectors[sl[i]][si] = str[i]
                col = colgen(str)
                y = rowgen(str)
                errors[i] = int(1)
                i += 1
    
        c = floor(k/9)
        q = k - 9*c
        si = q + 3*c - 3*sl[k]
    if sum(errors) <= 0:
        unsolved = False
    print(str)
    


for i in range(0,9):
    for j in range(0,9):
        output[i].append(str[j + 9*i])
#############################################################################################################################################################
'''
'''
#############################################################################################################################################################
#constants and related: KINDA WORKS, BUT GETS STUCK TOO EARLY
unsolved = True
output = [[],[],[],[],[],[],[],[],[]]
u = 0 #index of str, from 0 to 80 inclusive.
q = 0 #horizontal position, from 0 to 8 inclusive
c = 0 #vertical position, from 0 to 8 inclusive
si = 0 # position within a sector, from 0 to 8 inclusive
while unsolved:
    if val[u] == 0:                 #updating and adding +1 to a changeable number
        str[u] += 1
        print("added +1")
        sectors[sl[u]][si] = str[u]
        col = colgen(str)
        y = rowgen(str)
        if (sectors[sl[u]].count(str[u]) <= 1) and (col[si].count(str[u]) <= 1) and (y[c].count(str[u]) <= 1): #checking if it abides laws
            if str[u] >= 10: 
                str[u] = 0
                sectors[sl[u]][si] = str[u]
                u -= 1
                print("going back one")
            else:
                u += 1
                print("going forward one")
                
    if val[u] == 1:
        if (sectors[sl[u]].count(str[u]) <= 1) and (col[si].count(str[u]) <= 1) and (y[c].count(str[u]) <= 1): #checking if it abides laws
            u += 1
            print("ignoring cell and going forward one")
            
        else:
            backtrack = True
            while backtrack:
                print("going back")
                u -= 1
                c = floor(u/9)
                q = u - (9*c)
                si = q + 3*c - 3*sl[u]
                if val[u] == 0 and ((sectors[sl[u]].count(str[u]) >= 2) or (col[si].count(str[u]) >= 2) or (y[c].count(str[u]) >= 2)):
                    backtrack = False
                    print("correcting")
                    str[u] += 1
                    sectors[sl[u]][si] = str[u]
                    col = colgen(str)
                    y = rowgen(str)
                    if (sectors[sl[u]].count(str[u]) <= 1) and (col[si].count(str[u]) <= 1) and (y[c].count(str[u]) <= 1): #checking if it abides laws
                        if str[u] >= 10: 
                            str[u] = 0
                            sectors[sl[u]][si] = str[u]
                            u -= 1
                            print("going back one")
                        else:
                            u += 1
                            print("going forward one")
                    
                    
            
            
    c = floor(u/9)
    q = u - (9*c)
    si = q + 3*c - 3*sl[u]
    if u >= 81:
        unsolved = False
    
    
for i in range(0,9):
    for j in range(0,9):
        output[i].append(str[j + 9*i])
################################################################################################################################################################
'''        

