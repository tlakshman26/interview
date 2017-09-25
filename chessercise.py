#!/usr/bin/python

import sys, getopt
import random

def main(argv):
    piece = ''
    position = ''
    piece_list = ['knight', 'queen', 'rook']
    position_index = None
    gameboard = {}
    chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)]
    chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]
    target = False
    len_r_keys = 8
    opposing_pieces = []

    for i in range(8):
        for j, char in enumerate(range(97, 105)):
            gameboard[(i,j)] = '  ' #"{0}{1}".format(chr(char), i+1)

    def random_position():
        keys = gameboard.keys()
        r_keys = []
        while True:
            if len(r_keys) > len_r_keys:
                break
            r_key = random.choice(keys)
            if r_key not in r_keys:
                gameboard[r_key] = ' b'
                r_keys.append(r_key)
        print "r_key", r_keys
        return r_keys

    def printBoard():
        print(" |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |")
        for i in range(8):
            print("-"*42)
            print chr(i+97)+'|',
            for j in range(8):
                item = gameboard.get((i,j),"  ")
                print str(item)+' |',
            print
        print("-"*42)

    def get_most_distant_tile(position):
        target_position = None
        target_list = {}
        if opposing_pieces:
            for i in opposing_pieces:
                value = abs(i[0]-position[0])+abs(i[1]-position[1])
                target_list[i] = value
        if target_list:
            target_position = max(target_list, key=target_list.get)
        return target_position
    
    try:
        opts, args = getopt.getopt(argv, "hp:n:",["target", "piece=","position="])
    except getopt.GetoptError as e:
        print 'chessercise.py -piece <KNIGHT> -position <d2>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'chessercise.py -piece <KNIGHT> -position <d2>'
            sys.exit()
        elif opt in ("-p", "--piece"):
            print 
            if arg.lower() in piece_list:
                piece = arg.lower()
            else:
                print '-piece value should be in this <KNIGHT, QUEEN, ROOK> '
                sys.exit(3)
        elif opt in ("-n", "--position"):
            try:
                position_index = (ord(arg[0])-97, int(arg[1])-1)[::-1]
            except:
                pass
            if arg: #gameboard.get(position_index) == arg:
                position = arg
            else:
                print 'Make sure position value is correct.'
                sys.exit(3)
        elif opt in ("--target"):
            target = True

    if not (piece and  position):
        print 'chessercise.py -piece <KNIGHT> -position <d2>'
        sys.exit()
    if target:
        opposing_pieces=random_position()
        printBoard()
        most_distant_tile = get_most_distant_tile(position_index)
    
    x, y = position_index
    
    def isInBounds(x,y):
        "checks if a position is on the board"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def get_position(x, y, intervals):
        positions = []
        for xint,yint in intervals:
            xtemp,ytemp = x+xint,y+yint
            while isInBounds(xtemp,ytemp):
                target = gameboard.get((xtemp,ytemp),None)
                positions.append(gameboard.get((xtemp,ytemp)))
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return positions

    if piece == 'knight':
        possible_list = [(x+1, y+2), (x+2, y+1), (x-1, y-2), (x-2, y-1),
                         (x+1, y-2), (x+2, y-1), (x-1, y+2), (x-2, y+1)]
        print [gameboard.get(i) for i in possible_list if i in gameboard]
    elif piece == 'rook':
        print get_position(x, y, chessCardinals)
    elif piece == 'queen':
        print get_position(x, y, chessCardinals+chessDiagonals)
    else:
        pass
    
if __name__ == "__main__":
   main(sys.argv[1:])
