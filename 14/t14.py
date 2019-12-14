#! python3

import sys
from collections import defaultdict
import math

bom = {}

def produce(what,quantity):

	inventory = defaultdict(int)
	production_q = defaultdict(int)
	with open(sys.argv[1], "r") as f:
		bom_lines = map(str.strip, f.readlines())

		for r in bom_lines:
			arr1 = r.split(" => ")
  
			out_arr = arr1[1].split(" ")

			bom[ out_arr[1] ] = {}
			bom[ out_arr[1] ]['prod_qty'] = out_arr[0]

#			inventory[ out_arr[1] ] = 0
#			production_q[ out_arr[1] ] = 0
			bom[ out_arr[1] ]['need_qty'] = {}
			for ing in arr1[0].split(", ") :
				arr2 = ing.split(" ")
				bom[ out_arr[1] ]['need_qty'][ arr2[1] ] = arr2[0]


    
	production_q[what] = quantity
	
	while production_q:
		elem = list(production_q.keys())[0]
        
		if inventory[elem] >= production_q[elem] :
			inventory[elem] -= production_q[elem]
			del production_q[elem]
			continue

		still_needed = production_q[elem] - inventory[elem]
		inventory[elem] = 0

		prod_rounds = math.ceil( int(still_needed) / int(bom[elem]['prod_qty'])  )

        #say "need $prod_rounds prod rounds, producing...";
		inventory[elem] += ( prod_rounds * int(bom[elem]['prod_qty']) ) - still_needed

        #warn Dumper \%inventory;
		del production_q[elem];

		for elem2 in bom[elem]['need_qty'].keys():
			if elem2 == 'ORE' :
				inventory['ORE'] += int(bom[elem]['need_qty']['ORE']) * prod_rounds
			else :
				production_q[elem2] += int(bom[elem]['need_qty'][elem2]) * prod_rounds

	return inventory['ORE']



print("Part 1",produce('FUEL',1))
# got this by manually testing different numbers
print("Part 2",produce('FUEL',4436981))
print("Part 2",produce('FUEL',4436982))

