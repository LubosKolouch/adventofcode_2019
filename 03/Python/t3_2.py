#! python3_

from pprint import pprint
import re

grid={}
steps={}

steps_count=0
i = 0
min_count = 0

def process_step(posx,posy) :
                global steps_count
                global steps
                global min_count

                steps_count += 1

                if (i,posx,posy) not in steps:
                    steps[(i,posx,posy)] = steps_count
#                    print("posx "+str(posx)+" posy "+str(posy)+"grid value "+str(grid[(posx,posy)])+" i "+str(i))

                if (grid[(posx,posy)] > 1) :
                    total_steps = steps[(1,posx,posy)] + steps[(2,posx,posy)]
                    distance = abs(posx) + abs(posy)
                    print("intersection "+str(posx)+" "+str(posy)+" distance "+str(distance)+" steps "+str(total_steps))

                    if (min_count == 0) :
                        min_count = total_steps

                    if (min_count > total_steps) :
                        min_count = total_steps

                    print("min count "+str(min_count))

file = open("../input","r")

for line in file:
        i += 1
        arr = line.strip().split(',')
        posx=0
        posy=0
        steps_count = 0
        seen={}
       
        for item in arr:
            match=re.match(r"(.)(.*)", item)
            direction=match.group(1)
            count=match.group(2)
   
            if (direction == 'R') :
                for j in range(1,int(count)+1):
                    posx += 1

                    if (posx,posy) not in seen:
                        if (posx,posy) not in grid:
                            grid[(posx,posy)] = 1
                        else:
                            grid[(posx,posy)] += 1
                    seen[(posx,posy)]=1
                    process_step(posx,posy)
            
            if (direction == 'L') :
                for j in range(1,int(count)+1):
                    posx -= 1

                    if (posx,posy) not in seen:
                        if (posx,posy) not in grid:
                            grid[(posx,posy)] = 1
                        else:
                            grid[(posx,posy)] += 1
                    seen[(posx,posy)]=1
                    process_step(posx,posy)
 
            if (direction == 'U') :
                for j in range(1,int(count)+1):
                    posy += 1

                    if (posx,posy) not in seen:
                        if (posx,posy) not in grid:
                            grid[(posx,posy)] = 1
                        else:
                            grid[(posx,posy)] += 1
                    seen[(posx,posy)]=1
                    process_step(posx,posy)


            if (direction == 'D') :
                for j in range(1,int(count)+1):
                    posy -= 1

                    if (posx,posy) not in seen:
                        if (posx,posy) not in grid:
                            grid[(posx,posy)] = 1
                        else:
                            grid[(posx,posy)] += 1
                    seen[(posx,posy)]=1
                    process_step(posx,posy)


