#!/usr/bin/python

import sys, getopt
import random

def main(argv):
    piece = ''
    position = ''
    piece_list = ['knight', 'queen', 'rook']
    position_index = None
    gameboard = {}
    tiles = {}
    chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)]
    chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]
    target = False
    len_r_keys = 8
    opposing_pieces = []

    for i, value in enumerate(range(1,9)[::-1]):
        for j, char in enumerate(range(97, 105)):
            gameboard[(i,j)] = "{0}{1}".format(chr(char), value)
            tiles[(i,j)] = '  '


    def random_position(target):
        keys = tiles.keys()
        r_keys = []
        while True:
            if len(r_keys) >= len_r_keys:
                break
            r_key = random.choice(keys)
            if r_key not in r_keys:
                tiles[r_key] = ' b'
                r_keys.append(r_key)
        #r_keys = [(7, 2), (2, 1), (1, 0), (4, 7), (6, 5), (0, 3), (3, 0), (1, 3)]
        for i in r_keys:
            tiles[i] = ' b'
        tiles[target] = ' s'
        return r_keys

    def printBoard():
        print(" |  a |  b |  c |  d |  e |  f |  g |  h |")
        for i in range(8):
            print("-"*42)
            print str(abs(8-i)) +'|',
            for j in range(8):
                item = tiles.get((i,j),"  ")
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
            tiles[target_position] = ' t'
        return target_position
    
    def get_most_nearest_tile(position, moves_list):
        target_position = None
        target_list = {}
        for i in moves_list:
            value = abs(i[0]-position[0])+abs(i[1]-position[1])
            target_list[i] = value
        if target_list:
            target_position = min(target_list, key=target_list.get)
        return target_position

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
                positions.append((xtemp,ytemp))
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return positions

    def knightmoves(x,y):
        possible_list = [(x+1, y+2), (x+2, y+1), (x-1, y-2), (x-2, y-1),
                         (x+1, y-2), (x+2, y-1), (x-1, y+2), (x-2, y+1)]
        return [i for i in possible_list if i in tiles and 'm' not in tiles.get(i)]

    def get_moves(piece, position_index):
        x, y = position_index
        if piece == 'knight':
            return knightmoves(x, y)
        elif piece == 'rook':
            return get_position(x, y, chessCardinals)
        elif piece == 'queen':
            return get_position(x, y, chessCardinals+chessDiagonals)
        else:
            pass

    def get_target_moves(piece, start, target):
        moves = []
        if start == target:
            tiles[start] = ' t'
            return moves
        else:
            moves_list = get_moves(piece, start)
            if piece == 'knight' and start in moves_list:
                moves_list.remove(start)
            start = get_most_nearest_tile(target, moves_list)
            moves.append(start)
            tiles[start] = ' m'
            moves.extend(get_target_moves(piece, start, target))
            return moves

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
                position_index = (8-int(arg[1]), ord(arg[0])-97)
            except:
                pass
            if gameboard.get(position_index) == arg:
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
        opposing_pieces=random_position(position_index)
        print "Below are the opposing pieces positions.\n"
        print [gameboard.get(i) for i in opposing_pieces if i in gameboard]
        print
        most_distant_tile = get_most_distant_tile(position_index)
        target = most_distant_tile
        printBoard()
        result = get_target_moves(piece,position_index, target)
        print "After all possible moves.\n"
        printBoard()
    else:
        result = get_moves(piece, position_index)

    print "output: ",[gameboard.get(i) for i in result if i in gameboard]
    
if __name__ == "__main__":
   main(sys.argv[1:])
