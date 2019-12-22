#!/bin/python

import numpy as np
import sys

def deal_to_new_stack(deck):
    return deck[::-1]

def cut(deck,n):
    #print("--- cutting ----")
    #print(deck,n)
    slice = deck[0:n]
    #print(slice)
    deck = deck[n:]
    #print(deck)
    deck = np.concatenate((deck,slice),axis=0)
    return deck

def deal_with_increment(deck,n):
    pos_old_deck = -1
    pos_new_deck = -n

    new_deck = np.zeros(cards,int)
    while pos_old_deck < cards -1:
        pos_old_deck += 1
        pos_new_deck += n 
        pos_new_deck %= cards
        new_deck[pos_new_deck] = deck[pos_old_deck]
        #print(pos_old_deck,pos_new_deck,new_deck)

    return new_deck

cards = 10007

deck = np.arange(cards)
#print(deck)

code = open(sys.argv[1]).read().strip().split('\n')

for instr in code:
    instr_arr = instr.split(' ')
    if instr_arr[0] == 'cut':
        deck = cut(deck,int(instr_arr[1]))
    elif instr_arr[0] == 'deal' and instr_arr[1] == 'with' :
        deck = deal_with_increment(deck,int(instr_arr[3]))
    else:
        deck = deal_to_new_stack(deck)

print(np.where(deck == 2019)[0])
