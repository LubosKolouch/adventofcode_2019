#! python3_

from pprint import pprint
import re

grid={}

def process_step(posx,posy) :
                if (posx,posy) not in seen:
                    if (posx,posy) not in grid:
                        grid[(posx,posy)] = 1
                    else:
                        grid[(posx,posy)] += 1
                        distance = abs(posx) + abs(posy)
                        print("intersection "+str(posx)+" "+str(posy)+" distance "+str(distance))

                seen[(posx,posy)]=1

file = open("../input","r")

for line in file:
        arr = line.strip().split(',')
        posx=0
        posy=0
        seen={}
        
        for item in arr:
            match=re.match(r"(.)(.*)", item)
            direction=match.group(1)
            count=match.group(2)
   
            if (direction == 'R') :
                for i in range(1,int(count)+1):
                    posx += 1
                    process_step(posx,posy)
            
            if (direction == 'L') :
                for i in range(1,int(count)+1):
                    posx -= 1
                    process_step(posx,posy)
 
            if (direction == 'U') :
                for i in range(1,int(count)+1):
                    posy += 1
                    process_step(posx,posy)


            if (direction == 'D') :
                for i in range(1,int(count)+1):
                    posy -= 1
                    process_step(posx,posy)


