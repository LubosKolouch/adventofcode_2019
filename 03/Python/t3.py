#! python3_

from pprint import pprint
import re

grid={}

dX = {'R':1,'L':-1,'U':0,'D':0}
dY = {'R':0,'L':0,'U':1,'D':-1}

file = open("../input","r")

for line in file:
        arr = line.strip().split(',')
        posx=0
        posy=0
        seen={}
        
        for item in arr:
            direction,count = item[0],int(item[1:])
   
            for i in range(count):
                posx += dX[direction]
                posy += dY[direction]
                
                if (posx,posy) not in seen:
                    if (posx,posy) not in grid:
                        grid[(posx,posy)] = 1
                    else:
                        grid[(posx,posy)] += 1
                        distance = abs(posx) + abs(posy)
                        print("intersection "+str(posx)+" "+str(posy)+" distance "+str(distance))

                seen[(posx,posy)]=1

