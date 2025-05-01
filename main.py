import time
import random

# Future possible board positions - list of Nodes
futures = []

# Store user's move
user_movefrom = 0
user_moveto = 0

# Default parameters for evaluation of a piece given its board square
square_eval = [[0.0] * 64] * 12

# Trained parameters for evaluation of a piece given its board square



# Area for pasting previously saved parameter data
'''

square_eval =






'''

class Node:
    # method for creating a new position node
    def __init__(self, board, pieces, turn, miscs, movefrom, moveto):
        self.board = board
        self.pieces = pieces
        self.turn = turn
        self.miscs = miscs

        self.movefrom = movefrom
        self.moveto = moveto

        self.best_movefrom = -1
        self.best_moveto = -1
        self.eval = 0.0
        self.children = []

    # set a position node to the position of the current board, used to generate the tree root
    def copy_from_current(self):
        global current
        self.board = [] * 64
        for i in range(64):
            self.board[i] = current.board[i]
        self.pieces = [[]] * 12
        for i in range(12):
            for j in current.pieces[i]:
                self.pieces[i].append(j)
        self.turn = current.turn
        self.miscs = [] * 6
        for i in range(6):
            self.miscs[i] = current.miscs[i]

        self.movefrom = current.movefrom
        self.moveto = current.moveto

        self.best_movefrom = current.best_movefrom
        self.best_moveto = current.best_moveto
        self.eval = 0.0
        self.children = []


    # reset the board to its starting position
    def setup_board(self):
        self.board = [3,1,2,4,5,2,1,3,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,6,6,6,6,6,6,6,9,7,8,10,11,8,7,9]
        self.pieces = [[8,9,10,11,12,13,14,15],[1,6],[2,5],[0,7],[3],[4],[48,49,50,51,52,53,54,55],[57,62],[58,61],[56,63],[59],[60]]
        self.turn = 0
        for i in range(4):
            self.miscs[i] = 1
        self.miscs[4] = -1
        self.miscs[5] = 0
        
    # determine if white is not in check in a position
    def white_out_of_check(self):
        pos = self.pieces[5][0]
        b = self.board
        rank = int(pos / 8)
        file = pos % 8

        # look for rook and queen checks
        i = file + 1
        while i < 8:
            p = b[rank * 8 + i]
            if p > -1: break
            if p == 24 or p == 27 or p == 31: return False
            i += 1
        i = rank + 1
        while i < 8:
            p = b[i * 8 + file]
            if p > -1: break
            if p == 24 or p == 27 or p == 31: return False
            i += 1
        i = file - 1
        while i > -1:
            p = b[rank * 8 + i]
            if p > -1: break
            if p == 24 or p == 27 or p == 31: return False
            i -= 1
        i = rank - 1
        while i > -1:
            p = b[i * 8 + file]
            if p > -1: break
            if p == 24 or p == 27 or p == 31: return False
            i -= 1

        # look for bishop and queen checks
        i = rank + 1
        j = file + 1
        while i < 8 and j < 8:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 26 or p == 27 or p == 29: return False
            i += 1
            j += 1
        i = rank + 1
        j = file - 1
        while i < 8 and j > -1:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 26 or p == 27 or p == 29: return False
            i += 1
            j -= 1
        i = rank - 1
        j = file - 1
        while i > -1 and j > -1:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 26 or p == 27 or p == 29: return False
            i -= 1
            j -= 1
        i = rank - 1
        j = file + 1
        while i > -1 and j < 8:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 26 or p == 27 or p == 29: return False
            i -= 1
            j += 1

        # look for knight checks
        if rank < 7 and file < 6:
            p = b[(i + 1) * 8 + j + 2]
            if(p == 25 or p == 30): return False
        if rank < 6 and file < 7:
            p = b[(i + 2) * 8 + j + 1]
            if(p == 25 or p == 30): return False
        if rank < 6 and file > 0:
            p = b[(i + 2) * 8 + j - 1]
            if(p == 25 or p == 30): return False
        if rank < 7 and file > 1:
            p = b[(i + 1) * 8 + j - 2]
            if(p == 25 or p == 30): return False
        if rank > 0 and file > 1:
            p = b[(i - 1) * 8 + j - 2]
            if(p == 25 or p == 30): return False
        if rank > 1 and file > 0:
            p = b[(i - 2) * 8 + j - 1]
            if p == 25 or p == 30: return False
        if rank > 1 and file < 7:
            p = b[(i - 2) * 8 + j + 1]
            if p == 25 or p == 30: return False
        if rank > 0 and file < 6:
            p = b[(i - 1) * 8 + j + 2]
            if p == 25 or p == 30: return False

        # look for pawn checks
        if rank < 7:
            if file < 7:
                if b[pos + 9] > 15 and b[pos + 9] < 24: return False
            if file > 0:
                if b[pos + 7] > 15 and b[pos + 7] < 24: return False

        # look for king checks
        if rank < 7:
            if b[pos + 8] == 28: return False
            if file < 7:
                if b[pos + 9] == 28: return False
            if file > 0:
                if b[pos + 7] == 28: return False
        if rank > 0:
            if b[pos - 8] == 28: return False
            if file < 7:
                if b[pos - 7] == 28: return False
            if file > 0:
                if b[pos - 9] == 28: return False
        if file < 7:
            if b[pos + 1] == 28: return False
        if file > 0:
            if b[pos - 1] == 28: return False

        return True

    # determine if black is not in check in a position
    def black_out_of_check(self):
        print(self.pieces)
        pos = self.pieces[11][0]
        b = self.board
        rank = int(pos / 8)
        file = pos % 8

        # look for rook and queen checks
        i = file + 1
        while i < 8:
            p = b[rank * 8 + i]
            if p > -1: break
            if p == 0 or p == 3 or p == 7: return False
            i += 1
        i = rank + 1
        while i < 8:
            p = b[i * 8 + file]
            if p > -1: break
            if p == 0 or p == 3 or p == 7: return False
            i += 1
        i = file - 1
        while i > -1:
            p = b[rank * 8 + i]
            if p > -1: break
            if p == 0 or p == 3 or p == 7: return False
            i -= 1
        i = rank - 1
        while i > -1:
            p = b[i * 8 + file]
            if p > -1: break
            if p == 0 or p == 3 or p == 7: return False
            i -= 1

        # look for bishop and queen checks
        i = rank + 1
        j = file + 1
        while i < 8 and j < 8:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 2 or p == 3 or p == 5: return False
            i += 1
            j += 1
        i = rank + 1
        j = file - 1
        while i < 8 and j > -1:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 2 or p == 3 or p == 5: return False
            i += 1
            j -= 1
        i = rank - 1
        j = file - 1
        while i > -1 and j > -1:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 2 or p == 3 or p == 5: return False
            i -= 1
            j -= 1
        i = rank - 1
        j = file + 1
        while i > -1 and j < 8:
            p = b[i * 8 + j]
            if p > -1: break
            if p == 2 or p == 3 or p == 5: return False
            i -= 1
            j += 1

        # look for knight checks
        if rank < 7 and file < 6:
            p = b[(i + 1) * 8 + j + 2]
            if(p == 1 or p == 6): return False
        if rank < 6 and file < 7:
            p = b[(i + 2) * 8 + j + 1]
            if(p == 1 or p == 6): return False
        if rank < 6 and file > 0:
            p = b[(i + 2) * 8 + j - 1]
            if(p == 1 or p == 6): return False
        if rank < 7 and file > 1:
            p = b[(i + 1) * 8 + j - 2]
            if(p == 1 or p == 6): return False
        if rank > 0 and file > 1:
            p = b[(i - 1) * 8 + j - 2]
            if(p == 1 or p == 6): return False
        if rank > 1 and file > 0:
            p = b[(i - 2) * 8 + j - 1]
            if(p == 1 or p == 6): return False
        if rank > 1 and file < 7:
            p = b[(i - 2) * 8 + j + 1]
            if(p == 1 or p == 6): return False
        if rank > 0 and file < 6:
            p = b[(i - 1) * 8 + j + 2]
            if p == 1 or p == 6: return False

        # look for pawn checks
        if rank > 0:
            if file < 7:
                if b[pos - 7] > 7 and b[pos - 7] < 16: return False
            if file > 0:
                if b[pos - 9] > 7 and b[pos - 9] < 16: return False

        # look for king checks
        if rank < 7:
            if b[pos + 8] == 4: return False
            if file < 7:
                if b[pos + 9] == 4: return False
            if file > 0:
                if b[pos + 7] == 4: return False
        if rank > 0:
            if b[pos - 8] == 4: return False
            if file < 7:
                if b[pos - 7] == 4 : return False
            if file > 0:
                if b[pos - 9] == 4: return False
        if file < 7:
            if b[pos + 1] == 4: return False
        if file > 0:
            if b[pos - 1] == 4: return False

        return True
    
    def is_semilegal_move(self, movefrom, moveto):
        if movefrom < 0 or movefrom > 63 or moveto < 0 or moveto > 63 or moveto == movefrom: return False

        # get the moving piece's type
        movertype = self.board[movefrom]
        desttype = self.board[moveto]

        # check if piece of the player whose turn it is's color is on the source square
        if movertype < 0 or movertype > 11: return False
        if self.turn % 2 == 1 and movertype < 6: return False
        if self.turn % 2 == 0 and movertype > 5: return False

        # get the moving piece's specific number, return false if not found
        movernum = 0
        found = False
        for i in range(len(self.pieces[movertype])):
            if self.pieces[movertype][i] == movefrom:
                movernum = i
                found = True
                break
        if not found: return False

        capturing = False
        if movertype > 5:
            if desttype > 5: return False
            if desttype > -1 and desttype < 6: capturing = True
        else:
            if desttype > -1 and desttype < 6: return False
            if desttype > 5: capturing = True

        srcfile = movefrom % 8
        srcrank = int(movefrom / 8)
        difffile = moveto % 8
        diffrank = int(moveto / 8)
        diff = moveto - movefrom

        # depending on the piece, check if this move is legal
        match movertype:
            case 0:
                if diff == 8 and desttype == -1: return True
                if diff == 16 and srcrank == 1 and desttype == -1:
                    if self.board[movefrom + 8] == -1: return True
                if diff == 7 and srcfile > 0 and desttype > 5 : return True
                if diff == 9 and srcfile < 7 and desttype > 5 : return True
                if diff == 7 and srcfile > 0 and desttype == -1 and self.board[movefrom - 1] == 6 and self.miscs[4] == srcfile - 1 : return True # en passant left
                if diff == 9 and srcfile < 7 and desttype == -1 and self.board[movefrom + 1] == 6 and self.miscs[4] == srcfile + 1 : return True # en passant right
                    # promotion
            case 6:
                if diff == -8 and desttype == -1 : return True
                if diff == -16 and srcrank == 6 and desttype == -1:
                    if self.board[movefrom - 8] == -1: return True
                if diff == -9 and srcfile > 0 and desttype > -1 and desttype < 6 : return True
                if diff == -7 and srcfile < 7 and desttype > -1 and desttype < 6 : return True
                if diff == -9 and srcfile > 0 and desttype == -1 and self.board[movefrom - 1] == 0 and self.miscs[4] == srcfile - 1 : return True # en passant left
                if diff == -7 and srcfile < 7 and desttype == -1 and self.board[movefrom + 1] == 0 and self.miscs[4] == srcfile + 1 : return True # en passant right
                    # promotion
            case 1 | 7:
                if diff == 17 and srcfile < 7 and srcrank < 6: return True
                if diff == 15 and srcfile > 0 and srcrank < 6: return True
                if diff == 6 and srcfile > 1 and srcrank < 7: return True
                if diff == -10 and srcfile > 1 and srcrank > 0: return True
                if diff == -17 and srcfile > 0 and srcrank > 1: return True
                if diff == -15 and srcfile < 7 and srcrank > 1: return True
                if diff == -6 and srcfile < 6 and srcrank > 0: return True
                if diff == 10 and srcfile < 6 and srcrank < 7: return True
            case 2 | 4:
                dist = abs(difffile)
                if movertype == 2 or abs(diffrank) == dist:
                    inc = 9
                    if difffile == diffrank:
                        if difffile < 0: inc = -9
                    elif difffile == 0 - diffrank:
                        if difffile > 0: inc = -7
                        if difffile < 0: inc = 7
                    else: return False
                    
                    curr = movefrom
                    for i in range(dist):
                        curr += inc
                        if(self.board[curr] > -1 and self.board[curr] < 6): return False
                        if(self.board[curr] > 5):
                            if(i != dist - 1): return False
                    return True
            case 8 | 10:
                dist = abs(difffile)
                if(movertype == 8 or abs(diffrank) == dist):
                    inc = 9
                    if(difffile == diffrank):
                        if(difffile < 0): inc = -9
                    if(difffile == 0 - diffrank):
                        if(difffile > 0): inc = -7
                        if(difffile < 0): inc = 7
                    else: return False
                    
                    curr = movefrom
                    for i in range(dist):
                        curr += inc
                        if(self.board[curr] > 5): return False
                        if(self.board[curr] > -1 and self.board[curr] < 6):
                            if(i != dist - 1): return False
                    return True
            case 3 | 4:
                dist = abs(difffile) + abs(diffrank)
                inc = 1
                if(diffrank == 0):
                    if(difffile < 0): inc = -1
                elif(difffile == 0):
                    if(diffrank > 0): inc = 8
                    if(diffrank < 0): inc = -8
                else: return False
                
                curr = movefrom
                for i in range(dist):
                    curr += inc
                    if(self.board[curr] > -1 and self.board[curr] < 6): return False
                    if(self.board[curr] > 5):
                        if(i != dist - 1): return False
                return True
            case 9 | 10:
                dist = abs(difffile) + abs(diffrank)
                inc = 1
                if(diffrank == 0):
                    if(difffile < 0): inc = -1
                elif(difffile == 0):
                    if(diffrank > 0): inc = 8
                    if(diffrank < 0): inc = -8
                else: return False
                
                curr = movefrom
                for i in range(dist):
                    curr += inc
                    if(self.board[curr] > 5): return False
                    if(self.board[curr] > -1 and self.board[curr] < 6):
                        if(i != dist - 1): return False
                return True
            case 5 | 11:
                match diff:
                    case 1: return srcfile < 7
                    case 9: return srcfile < 7 and srcrank < 7
                    case 8: return srcrank < 7
                    case 7: return srcfile > 0 and srcrank < 7
                    case -1: return srcfile > 0
                    case -9: return srcfile > 0 and srcrank > 0
                    case -8: return srcrank > 0
                    case -7: return srcfile < 7 and srcrank > 0
        
        return False

    # Determine if a move is legal: semilegal and not putting the player who moves in check
    def is_legal_move(self, movefrom, moveto):
        if self.is_semilegal_move(movefrom, moveto):
            new = self.execute_move(movefrom, moveto)
            if new == None: return False
            if new.turn % 2 == 1: return new.white_out_of_check()
            return new.black_out_of_check()
        return False
    
    # method for generating position after move, or for adding a new position child node to a current leaf, given the node and the piece movement
    def execute_move(self, movefrom, moveto):
        b = self.board[:]
        p = self.pieces[:]
        m = self.miscs[:]
        print(p)
        movertype = b[movefrom]
        if movertype < 0 or movertype > 11: return self
        
        capturing = (movertype == 0 or movertype == 6) # pawn move or capture for resetting 50-move rule
        movernum = 0
        pm = p[movertype]
        for i in range(len(pm)):
            if pm[i] == movefrom:
                movernum = i
                # changing the piece's location on the new board array
                b[movefrom] = -1
                if b[moveto] > -1:
                    capturing = True
                    # capture and remove the piece on the destination square
                    for i in range(len(p[b[moveto]])):
                        if p[b[moveto]][i] == moveto:
                            p[b[moveto]].pop(i)
                            break
                    self.pieces[b[moveto]] = p[b[moveto]]
                b[moveto] = movertype
                # change the piece's location on pieces
                pm[i] = moveto
                break

        print(p)
        # white pawn promotion
        if movertype == 0 and moveto > 55:
            # remove the pawn
            pm.pop(movernum)
            # add the promoted piece depending on its type
            p[int(moveto / 8) - 6].append(56 + (moveto % 8))
            # since captures have been covered above, we are done

        # black pawn promotion
        if movertype == 6 and moveto < 8:
            # remove the pawn
            pm.pop(movernum)
            # add the promoted piece depending on its type
            p[10 - int(moveto / 8)].append(56 + (moveto % 8))
            # since captures have been covered above, we are done


        # to castle, only move the rook, since the king has already moved to the right spot

        # WQ castling
        if movertype == 5 and moveto == 2:
            b[0] = -1
            for i in range(len(p[3])):
                if p[3][i] == 0:
                    p[3][i] = 3
                    break
        # WK castling
        if movertype == 5 and moveto == 6:
            b[7] = -1
            for i in range(len(p[3])):
                if p[3][i] == 7:
                    p[3][i] = 5
                    break
        # BQ castling
        if movertype == 11 and moveto == 58:
            b[56] = -1
            for i in range(len(p[9])):
                if p[9][i] == 56:
                    p[9][i] = 59
                    break
        # BK castling
        if movertype == 11 and moveto == 62:
            b[63] = -1
            for i in range(len(p[9])):
                if p[9][i] == 63:
                    p[9][i] = 61
                    break

        # en passant is already done

        # set the miscellaneous descriptors: disable castling if moving kings or rooks
        if b[0] != 3:
            m[0] = 0
        if b[4] != 5:
            m[0] = 0
            m[1] = 0
        if b[7] != 3:
            m[1] = 0
        if b[56] != 3:
            m[2] = 0
        if b[60] != 5:
            m[2] = 0
            m[3] = 0
        if b[63] != 3:
            m[3] = 0
        
        # change en passant if moving pawn two squares
        m[4] = -1
        if (movertype == 0 or movertype == 6) and (moveto - movefrom == 16 or moveto - movefrom == -16):
            m[4] = moveto % 8
        
        # handle 50-move rule
        m[5] += 1
        if(capturing):
            m[5] = 0
        print(p)

        # creating the new position child node
        new = Node(b, p, self.turn + 1, m, movefrom, moveto)

        # add the move to the new position
        new.movefrom = movefrom
        new.moveto = moveto

        # add the new position to the tree (leaf's children)
        self.children.append(new)

        if new.eval == None: return None

        # if both kings are on the board, add the new position to the queue for future branching
        futures.append(new)
        return new
    
    # evaluate an entirely new position
    def base_evaluate(self, sq_eval, time_limit):
        
        # destroy the futures queue and tree of nodes (except for the root)
        futures.clear()
        for i in self.children:
            i.destroy_tree()

        # set the tree root as a copy of current
        self.copy_from_current()

        # add the current position to the queue of positions to evaluate
        futures.append(Node(self.board, self.pieces, self.turn, self.miscs, "", ""))

        # get the time at the start of the evaluation
        start_time = time.time_ns()

        # keep evaluating positions until you need to make a move
        while((time.time_ns() - start_time) / 1000 < time_limit):

            # get the next position in the futures queue to evaluate
            node = futures.pop(0)

            b = node.board
            p = node.pieces

            # if there are fewer than two kings on the board, quit evaluating
            if len(p[5]) == 0 or len(p[11]) == 0: return None

            e = 0.0

            # get the total eval of all the pieces
            e += 1.0 * len(p[0])
            e += 3.0 * len(p[1])
            e += 3.3 * len(p[2])
            e += 5.0 * len(p[3])
            e += 9.0 * len(p[4])
            e -= 1.0 * len(p[6])
            e -= 3.0 * len(p[7])
            e -= 3.3 * len(p[8])
            e -= 5.0 * len(p[9])
            e -= 9.0 * len(p[10])

            # use trained parameters to add up eval for each piece given its square
            for i in range(12):
                for j in range(len(p[i])):
                    e += sq_eval[i][p[i][j]]

            # set the node's eval
            node.eval = e

            # get all choices for moves branching off this position and add them to both the tree of position nodes and the futures queue
            global_add_moves = True
            if(node.turn % 2 == 0):
                node.get_choices_white()
            else:
                node.get_choices_black()

        # once the time is up, traverse the tree and find all the best moves
        self.tree_evaluate()

    # recursively traverse the tree and find every position's best move back to the head, record them all
    def tree_evaluate(self):
        white = self.turn % 2 == 0
        for i in self.children:
            i.tree_evaluate()
            if((white and i.eval > self.eval) or (not white and i.eval < self.eval)):
                self.eval = i.eval
                self.best_movefrom = i.movefrom
                self.best_moveto = i.moveto

    # add a possible choice defined by moving from movefrom to moveto using first position in queue
    def add_choice(self, movefrom, moveto):
        
        new_position = futures[0].execute_move(movefrom, moveto)
        if new_position != None:
            futures.append(new_position)

    # checks whether a piece can move to a square and returns True when cannot move farther (MAYBE MAKE SURE NOT MOVING INTO CHECK)
    def check_square_move(self, movefrom, moveto):
        
        target = self.board[moveto]
        if target > -1:
            if target > 5 and self.turn % 2 == 1:
                self.add_choice(movefrom, moveto)
            if target < 6 and self.turn % 2 == 0:
                self.add_choice(movefrom, moveto)
            return True
        self.add_choice(movefrom, moveto)
        return False

    # get all the possible choices that a piece can make
    def get_choices(self, movefrom):
        if movefrom < 0 or movefrom > 63: return

        b = self.board
        mover = b[movefrom]
        rank = int(movefrom / 8)
        file = movefrom % 8

        # if moving the wrong color piece, exit immediately
        if self.turn % 2 == 1 and mover < 6: return
        if self.turn % 2 == 0 and mover > 5: return
        
        match mover:
            case 3 | 9: # rook
                i = file + 1
                while i < 8:
                    if self.check_square_move(movefrom, rank * 8 + i): break
                    i += 1
                i = rank + 1
                while i < 8:
                    if self.check_square_move(movefrom, i * 8 + file): break
                    i += 1
                i = file - 1
                while i > -1:
                    if self.check_square_move(movefrom, rank * 8 + i): break
                    i -= 1
                i = rank - 1
                while i > -1:
                    if self.check_square_move(movefrom, i * 8 + file): break
                    i -= 1
            case 1 | 7: # knight
                if rank < 7 and file < 6: self.check_square_move(movefrom, (i + 1) * 8 + j + 2)
                if rank < 6 and file < 7: self.check_square_move(movefrom, (i + 2) * 8 + j + 1)
                if rank < 6 and file > 0: self.check_square_move(movefrom, (i + 2) * 8 + j - 1)
                if rank < 7 and file > 1: self.check_square_move(movefrom, (i + 1) * 8 + j - 2)
                if rank > 0 and file > 1: self.check_square_move(movefrom, (i - 1) * 8 + j - 2)
                if rank > 1 and file > 0: self.check_square_move(movefrom, (i - 2) * 8 + j - 1)
                if rank > 1 and file < 7: self.check_square_move(movefrom, (i - 2) * 8 + j + 1)
                if rank > 0 and file < 6: self.check_square_move(movefrom, (i - 1) * 8 + j + 2)
            case 2 | 6: # bishop
                i = rank + 1
                j = file + 1
                while i < 8 and j < 8:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i += 1
                    j += 1
                i = rank + 1
                j = file - 1
                while i < 8 and j > -1:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i += 1
                    j -= 1
                i = rank - 1
                j = file - 1
                while i > -1 and j > -1:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i -= 1
                    j -= 1
                i = rank - 1
                j = file + 1
                while i > -1 and j < 8:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i -= 1
                    j += 1
            case 4 | 10: # queen
                i = file + 1
                while i < 8:
                    if self.check_square_move(movefrom, rank * 8 + i): break
                    i += 1
                i = rank + 1
                while i < 8:
                    if self.check_square_move(movefrom, i * 8 + file): break
                    i += 1
                i = file - 1
                while i > -1:
                    if self.check_square_move(movefrom, rank * 8 + i): break
                    i -= 1
                i = rank - 1
                while i > -1:
                    if self.check_square_move(movefrom, i * 8 + file): break
                    i -= 1
                i = rank + 1
                j = file + 1
                while i < 8 and j < 8:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i += 1
                    j += 1
                i = rank + 1
                j = file - 1
                while i < 8 and j > -1:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i += 1
                    j -= 1
                i = rank - 1
                j = file - 1
                while i > -1 and j > -1:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i -= 1
                    j -= 1
                i = rank - 1
                j = file + 1
                while i > -1 and j < 8:
                    if self.check_square_move(movefrom, i * 8 + j): break
                    i -= 1
                    j += 1
            case 0: # white pawns
                if rank < 7:
                    moveto = (rank + 1) * 8 + file
                    if b[moveto] == ' ': # move upward
                        self.add_choice(movefrom, moveto)
                        if rank == 1 and b[moveto + 8] == ' ': # move upward two spaces
                            self.add_choice(movefrom, moveto + 8)
                    moveto = (rank + 1) * 8 + file + 1
                    if file < 7:
                        if b[moveto] > 5: # capture up-right
                            self.add_choice(movefrom, moveto)
                        if b[moveto] == ' ' and self.miscs[4] == file + 1: # en passant up-right
                            self.add_choice(movefrom, moveto)

                    moveto = (rank + 1) * 8 + file - 1
                    if file > 0:
                        if b[moveto] > 5: # capture up-left
                            self.add_choice(movefrom, moveto)
                        if b[moveto] == ' ' and self.miscs[4] == file - 1: # en passant up-left
                            self.add_choice(movefrom, moveto)
            case 6: # black pawns
                if rank > 0:
                    moveto = (rank - 1) * 8 + file
                    if b[moveto] == ' ': # move downward
                        self.add_choice(movefrom, moveto)
                        if rank == 6 and b[moveto - 8] == ' ': # move upward two spaces
                            self.add_choice(movefrom, moveto - 8)
                    moveto = (rank - 1) * 8 + file + 1
                    if file < 7:
                        if b[moveto] > -1 and b[moveto] < 6: # capture down-right
                            self.add_choice(movefrom, moveto)
                        if b[moveto] == ' ' and self.miscs[4] == file + 1: # en passant down-right
                            self.add_choice(movefrom, moveto)

                    moveto = (rank - 1) * 8 + file - 1
                    if file > 0:
                        if b[moveto] > -1 and b[moveto] < 6: # capture down-left
                            self.add_choice(movefrom, moveto)
                        if b[moveto] == ' ' and self.miscs[4] == file - 1: # en passant down-left
                            self.add_choice(movefrom, moveto)
            case 5 | 11: # white/black king
                if rank < 7:
                    self.check_square_move((rank + 1) * 8 + file)
                    if file < 7: self.check_square_move((rank + 1) * 8 + file + 1)
                    if file > 0: self.check_square_move((rank + 1) * 8 + file - 1)
                if rank > 0:
                    self.check_square_move((rank - 1) * 8 + file)
                    if file < 7: self.check_square_move((rank - 1) * 8 + file + 1)
                    if file > 0: self.check_square_move((rank - 1) * 8 + file - 1)
                if file < 7: self.check_square_move(rank * 8 + file + 1)
                if file > 0: self.check_square_move(rank * 8 + file - 1)

            # Now check for both kings' castling ability by inching them down and seeing if they remain out of check the whole way

            case 5: # white king castling
                if movefrom == 4 and b[5] == -1 and b[6] == -1 and self.miscs[0] == 1: #WK
                    if self.white_out_of_check():
                        self.pieces[5][0] = 5
                        b[4] = -1
                        b[5] = 0
                        if self.white_out_of_check():
                            self.pieces[5][0] = 6
                            b[5] = -1
                            b[6] = 0
                            if self.white_out_of_check():
                                self.pieces[5][0] = 4
                                b[6] = -1
                                b[4] = 0
                                self.add_choice(4, 6)
                        self.pieces[5][0] = 4
                        b[6] = -1
                        b[5] = -1
                        b[4] = 0
                if movefrom == 4 and b[1] == -1 and b[2] == -1 and b[3] == -1 and self.miscs[1] == 1: #WQ
                    if self.white_out_of_check():
                        self.pieces[5][0] = 3
                        b[4] = -1
                        b[3] = 5
                        if self.white_out_of_check():
                            self.pieces[5][0] = 2
                            b[3] = -1
                            b[2] = 5
                            if self.white_out_of_check():
                                self.pieces[5][0] = 4
                                b[2] = -1
                                b[4] = 5
                                self.add_choice(4, 2)
                        self.pieces[5][0] = 4
                        b[2] = -1
                        b[3] = -1
                        b[4] = 5
            case 11: # black king castling
                if movefrom == 60 and b[61] == -1 and b[62] == -1 and self.miscs[2] == 1: #BK
                    if self.black_out_of_check():
                        self.pieces[11][0] = 61
                        b[60] = -1
                        b[61] = 11
                        if(self.black_out_of_check()):
                            self.pieces[11][0] = 62
                            b[61] = -1
                            b[62] = 11
                            if(self.black_out_of_check()):
                                self.pieces[11][0] = 60
                                b[62] = -1
                                b[60] = 11
                                self.add_choice(60, 62)
                        self.pieces[11][0] = 60
                        b[62] = -1
                        b[61] = -1
                        b[60] = 11
                if movefrom == 60 and b[57] == -1 and b[58] == -1 and b[59] == -1 and self.miscs[3] == 1: #BQ
                    if self.black_out_of_check():
                        self.pieces[11][0] = 59
                        b[60] = -1
                        b[59] = 11
                        if self.black_out_of_check():
                            self.pieces[11][0] = 58
                            b[59] = -1
                            b[58] = 11
                            if self.black_out_of_check():
                                self.pieces[11][0] = 60
                                b[58] = -1
                                b[60] = 11
                                self.add_choice(60, 58)
                        self.pieces[11][0] = 60
                        b[58] = -1
                        b[59] = -1
                        b[60] = 11

    # gets all choices for white and adds them 
    def get_choices_white(self):
        for i in range(0, 6):
            for j in range(len(self.pieces[i])):
                self.get_choices(self.pieces[i][j])

    # gets all choices for black and adds them 
    def get_choices_black(self):
        for i in range(6, 12):
            for j in range(len(self.pieces[i])):
                self.get_choices(self.pieces[i][j])

    # checks whether the game has ended
    def check_game_end(self):

        if self.turn % 2 == 0:
            self.get_choices_white()
            if(len(self.children) == 0):
                if self.white_out_of_check(): # white is stalemated
                    return 2
                else: # white is checkmated
                    return 3
        if self.turn % 2 == 1:
            self.get_choices_black()
            if(len(self.children) == 0):
                if self.black_out_of_check(): # black is stalemated
                    return 1
                else: # black is checkmated
                    return 3
        return 0

    # recursively destroy all of this root's children >:)
    def destroy_tree(self):
        for i in self.children:
            i.destroy_tree()
        del(self)
    
    # check whether any of the possible user moves with a piece to a destination square is legal
    def check_user_move(self, p, dest, s):
        for i in p:
            if self.is_legal_move(i, dest):
                user_movefrom = i
                user_moveto = dest
                return False
        print("\"" + s + "\" is not a valid move. No piece of this type can move to this square without putting you into check.\n")
        return True

    # check whether any of the possible user moves with a piece on file to a destination square is legal
    def check_user_move_file(self, p, dest, s, file):
        for i in p:
            if i % 8 == ord(file) - ord('a') and self.is_legal_move(i, dest):
                user_movefrom = i
                user_moveto = dest
                return False
        print("\"" + s + "\" is not a valid move. No piece of this type and file can move to this square without putting you into check.\n")
        return True

    # check whether any of the possible user moves with a piece on rank to a destination square is legal
    def check_user_move_rank(self, p, dest, s, rank):
        for i in p:
            if(int(i / 8) == ord(rank) - ord('1') and self.is_legal_move(i, dest)):
                user_movefrom = i
                user_moveto = dest
                return False
        print("\"" + s + "\" is not a valid move. No piece of this type and rank can move to this square without putting you into check.\n")
        return True

    # check whether any of the possible user moves with a piece on file and rank to a destination square is legal
    def check_user_move_both(self, p, dest, s, file, rank):
        for i in p:
            if(i % 8 == ord(file) - ord('a') and int(i / 8) == ord(rank) - ord('1') and self.is_legal_move(i, dest)):
                user_movefrom = i
                user_moveto = dest
                return False
        print("\"" + s + "\" is not a valid move. No piece of this type, rank, and file can move to this square without putting you into check.\n")
        return True


# pieces occupying the 64 squares starting at a1->a8->h1->h8
# square locations of all 12 types of pieces starting with White's pawns
# int representing whose turn it is. 0 = White, 1 = Black, 2 = White, etc.
# castling: (0/1) WK, WQ, BK, BQ, en passant file (0-7), 50 move rule (int)
# past movesfrom
# past movesto
current = Node([-1] * 64, [[] * 12], 0, [1, 1, 1, 1, -1, 0], -1, -1)

tree_root = Node(current.board, current.pieces, current.turn, current.miscs, -1, -1)


# train (evolve) the algorithm
def train(time_limit, training_time_limit, mutation_strength, upper_limit, lower_limit):
    global current

    winner = 0
    global tree_root

    # only initialize the first square_evals list since this is the first winner
    square_eval0 = [[0.0] * 64] * 12
    square_eval1 = [[0.0] * 64] * 12
    for i in range(12):
        for j in range(64):
            square_eval0[i][j] = square_eval[i][j] + random.normalvariate(0.0, 0.1 * mutation_strength)

    # get the time at the start of training
    start_time = time.time_ns()

    # keep training until time is up
    while((time.time_ns() - start_time) / 1000 < training_time_limit):

        # initialize the new parameter lists, varied slightly and randomly
        if winner == 0:
            for i in range(12):
                for j in range(64):
                    square_eval0[i][j] = square_eval0[i][j] + random.normalvariate(0.0, 0.1 * mutation_strength)
                    square_eval1[i][j] = square_eval0[i][j] + random.normalvariate(0.0, 0.1 * mutation_strength)
                    if square_eval0[i][j] > upper_limit: square_eval0[i][j] = upper_limit
                    if square_eval0[i][j] < lower_limit: square_eval0[i][j] = lower_limit
                    if square_eval1[i][j] > upper_limit: square_eval1[i][j] = upper_limit
                    if square_eval1[i][j] < lower_limit: square_eval1[i][j] = lower_limit
        else:
            for i in range(12):
                for j in range(64):
                    square_eval0[i][j] = square_eval1[i][j] + random.normalvariate(0.0, 0.1 * mutation_strength)
                    square_eval1[i][j] = square_eval1[i][j] + random.normalvariate(0.0, 0.1 * mutation_strength)
                    if square_eval0[i][j] > upper_limit: square_eval0[i][j] = upper_limit
                    if square_eval0[i][j] < lower_limit: square_eval0[i][j] = lower_limit
                    if square_eval1[i][j] > upper_limit: square_eval1[i][j] = upper_limit
                    if square_eval1[i][j] < lower_limit: square_eval1[i][j] = lower_limit


        current.setup_board()
        game_over = False

        # play a game
        while(True):

            # White bot plays

            tree_root.base_evaluate(square_eval0, time_limit)

            new = current.execute_move(tree_root.best_movefrom, tree_root.best_moveto)
            current = new
                    
            game_status = current.check_game_end()

            if game_status > 0:
                game_over = True
                match game_status:
                    case 1: winner = 0 # White wins
                    case 2: winner = 1 # Black wins
                    case 3: winner = random.choice([0, 1]) # Draw
            if game_over: break
                        
                        
            # Black bot plays

            tree_root.base_evaluate(square_eval1, time_limit)

            new = current.execute_move(tree_root.best_movefrom, tree_root.best_moveto)
            current = new
                    
            game_status = current.check_game_end()

            if game_status > 0:
                game_over = True
                match game_status:
                    case 1: winner = 0 # White wins
                    case 2: winner = 1 # Black wins
                    case 3: winner = random.choice([0, 1]) # Draw
            if game_over: break

    # once time is up, fill square_eval with the new best trained square_eval from square_evals
    if winner == 0:
        for i in range(12):
            for j in range(64):
                square_eval[i][j] = square_eval0[i][j]
    else:
        for i in range(12):
            for j in range(64):
                square_eval[i][j] = square_eval1[i][j]

    # print square_eval to store it for later use
    string = "["

    for i in range(11):
        string += "["
        for j in range(63):
            string += str(square_eval[i][j]) + ","
        string += str(square_eval[i][63]) + "],\n"
        
    string += "["
    for j in range(63):
        string += str(square_eval[11][j]) + ","
    string += str(square_eval[11][63]) + "]]\n\n"
    
    print(string)

# parse the user's answer and get the movefrom and moveto squares
def parse_move(answer):
    global current

    s = ""

    # fill a new string with only meaningful characters
    for i in answer:
        if (ord(i) >= ord('0') and ord(i) <= ord('9')) or (ord(i) >= ord('a') and ord(i) <= ord('h')) or i == 'B' or i == 'K' or i == 'N' or i == 'Q' or i == 'R':
            s += i
    
    l = len(s)
    if l < 2 or l > 5:
        print("\"" + s + "\" is not a valid move. Moves must be 2, 3, 4, or 5 characters long.\n")
        return True
    if not (s[0] == 'N' or s[0] == 'B' or s[0] == 'R' or s[0] == 'Q' or s[0] == 'K' or (ord(s[0]) >= ord('a') and ord(s[0]) <= ord('h'))):
        print("\"" + s + "\" is not a valid move. Moves must start with a piece letter N/B/R/Q/K or board file a-h.\n")
        return True
    if not (ord(s[l - 2]) >= ord('a') and ord(s[l - 2]) <= ord('h') and ord(s[l - 1]) >= ord('1') and ord(s[l - 1]) <= ord('8')):
        print("\"" + s + "\" is not a valid move. Moves must end with a board file a-h and then a board rank 1-8.\n")
        return True
    
    p = current.pieces
    b = current.board
    t = current.turn
    m = current.miscs
    black = 0
    if t % 2 == 1: black = 6
    dest = (ord(s[l - 1]) - ord('1')) * 8 + ord(s[l - 2]) - ord('a')

    if s == "00": # kingside castle
        if black: #BK
            b[60] = -1
            b[61] = 9
            b[62] = 11
            b[63] = -1
            p[11][0] = 62
            for i in range(len(p[9])):
                if p[9][i] == 63:
                    p[9][i] = 61
                    break
        else: #WK
            b[4] = -1
            b[5] = 3
            b[6] = 5
            b[7] = -1
            p[5][0] = 58
            for i in range(len(p[3])):
                if p[3][i] == 7:
                    p[3][i] = 5
                    break
    if s == "000": # queenside castle
        if black: #BQ
            b[60] = -1
            b[59] = 9
            b[58] = 11
            b[57] = -1
            b[56] = -1
            p[11][0] = 58
            for i in range(len(p[9])):
                if p[9][i] == 56:
                    p[9][i] = 59
                    break
        else: #WQ
            b[4] = -1
            b[3] = 3
            b[2] = 5
            b[1] = -1
            b[0] = -1
            p[5][0] = 2
            for i in range(len(p[3])):
                if p[3][i] == 0:
                    p[3][i] = 3
                    break
    
    if l == 2: # handle 2-char moves
        return current.check_user_move(p[black], dest, s) # handle 2-char moves (pawn moves and en passants)
    elif l == 3: # handle 3-char moves
        match s[0]: # handle 3-char moves that begin with N/B/R/Q/K (non-pawn moves)
            case 'N':
                return current.check_user_move(p[1 + black], dest, s)
            case 'B':
                return current.check_user_move(p[2 + black], dest, s)
            case 'R':
                return current.check_user_move(p[3 + black], dest, s)
            case 'Q':
                return current.check_user_move(p[4 + black], dest, s)
            case 'K':
                return current.check_user_move(p[5 + black], dest, s)
        
        return current.check_user_move_file(p[black], dest, s) # handle 3-char moves that begin with a file (pawn captures)
        
    elif l == 4: # handle 4-char moves (source-dest notation and non-pawn moves on file or rank)
        is_file = ord(s[1]) >= ord('a') and ord(s[1]) <= ord('h')
        match s[0]: # handle 4-char moves that begin with N/B/R/Q/K (non-pawn moves on file or rank)
            case 'N':
                if is_file:
                    return current.check_user_move_file(p[1 + black], dest, s, s[1])
                return current.check_user_move_rank(p[1 + black], dest, s, s[1])
            case 'B':
                if is_file:
                    return current.check_user_move_file(p[2 + black], dest, s, s[1])
                return current.check_user_move_rank(p[2 + black], dest, s, s[1])
            case 'R':
                if is_file:
                    return current.check_user_move_file(p[3 + black], dest, s, s[1])
                return current.check_user_move_rank(p[3 + black], dest, s, s[1])
            case 'Q':
                if is_file:
                    return current.check_user_move_file(p[4 + black], dest, s, s[1])
                return current.check_user_move_rank(p[4 + black], dest, s, s[1])
            case 'K':
                if is_file:
                    return current.check_user_move_file(p[5 + black], dest, s, s[1])
                return current.check_user_move_rank(p[5 + black], dest, s, s[1])
        
        return current.check_user_move_both(p[black], dest, s, s[0], s[1]) # handle source-dest notation

    elif l == 5: # handle 5-char moves (non-pawn moves on file and rank)
        if not (ord(s[1]) >= ord('a') and ord(s[1]) <= ord('h') and ord(s[2]) >= ord('1') and ord(s[2]) <= ord('8')):
            print("\"" + s + "\" is not a valid move. Five-character moves must use a board file a-h and then a board rank 1-8 as the second and third characters.\n")
            return True
        
        match s[0]: # handle 5-char moves that begin with N/B/R/Q/K (non-pawn moves on file and rank)
            case 'N':
                return current.check_user_move_both(p[1 + black], dest, s, s[1], s[2])
            case 'B':
                return current.check_user_move_both(p[2 + black], dest, s, s[1], s[2])
            case 'R':
                return current.check_user_move_both(p[3 + black], dest, s, s[1], s[2])
            case 'Q':
                return current.check_user_move_both(p[4 + black], dest, s, s[1], s[2])
            case 'K':
                return current.check_user_move_both(p[5 + black], dest, s, s[1], s[2])
    
        print("\"" + s + "\" is not a valid move. Five-character moves must begin with a piece letter.\n")
        return True
    
    print("Could not process your move for unknown reasons.\n")
    return True

# print the board as ascii text
def print_board():
    global current

    for i in range(8):
        print("---------------------------------")
        s = "|"
        for j in range(8):
            match(current.board[(7 - i) * 8 + j]):
                case 0: s += " P "
                case 1: s += " N "
                case 2: s += " B "
                case 3: s += " R "
                case 4: s += " Q "
                case 5: s += " K "
                case 6: s += " p "
                case 7: s += " n "
                case 8: s += " b "
                case 9: s += " r "
                case 10: s += " q "
                case 11: s += " k "
                case _: s += "   "
            s += "|"
        print(s)
    print("---------------------------------\n\n\n")

# executes the player's move
def player_play():
    global current

    reprompt = True

    while reprompt:

        print_board()

        print("\nEnter your move in standard chess notation or in the form \"a4b6\". Enter nothing for more information.  ")
        answer = input()
        reprompt = True

        if answer == '':
            print("\nTo write a move in standard notation, first enter the capital letter corresponding to the piece being moved:")
            print("\n\tPawn = (no letter)\tKnight = \"N\"\nBishop = \"B\"\tRook = \"R\"\nQueen = \"Q\"\tKing = \"K\"\n\n")
            print("If the move captures another piece, you may put a \"x\" after the piece letter, but it is not necessary.\n")
            print("While pawn moves do not use a piece letter, pawn captures use the lowercase file letter the pawn starts on in place of a piece letter.\n")
            print("Examples: exd5, gh2.\n")
            print("Then, enter the lowercase file of the piece's destination square (a through h).\n")
            print("Next, enter the numerical rank of the piece's destination square (1 through 8).\n\n")
            print("If there is a legal move that involves the same type of piece moving to the same square as your move, you must differentiate your move from other moves.\n")
            print("Do this by adding either the file (as a lowercase letter) or the rank (as a number) of the square the piece is being moved from immediately after the piece letter.\n")
            print("Examples: Nec3, R5a5.\n")
            print("This must not still allow for two or more moves to be written the same way.\n")
            print("If using either one of the file and rank of the square the piece is moving from creates a move which cannot be differentiated from another move, you must use both the file and rank.")
            print("Examples: Qd2e3, Qa7b7.\n\n")
            print("If the move puts the opposing king in check, you may put a \"+\" after the move notation, but it is not necessary.\n")
            print("Kingside castling (between files e and h) is written as \"0-0\" or \"00\". Queenside castling (between files a and e) is written as \"0-0-0\" or \"000\".\n")
            print("Pawn promotions are written in the format of regular pawn moves, but with an added capital letter at the end corresponding to the piece being promoted to.\n")
            print("Examples: b8Q, f1N.\n")
            print("En passant pawn moves are written simply as the pawn's destination square as if moving a pawn forward.\n\n")
            print("Capitalization matters for all letters. Characters besides numbers 1-8, letters a-h and letters B/K/N/Q/R will be ignored and therefore do not matter.\n\n")
            print("For notation following the form \"a4b6\", replace the piece letter at the beginning of any move written using standard notation with the file and rank of the ")
            print("square your piece is moving from.\nFor pawn moves, simply add the square the pawn is moving from to the beginning of the notation.\n")
            print("The rest of the notation follows the above procedure.\n")
            print("Do not change the notation when castling; use \"00\", \"0-0\", \"000\" or \"0-0-0\".\n")
        else:
            reprompt = parse_move(answer)

    new = current.execute_move(user_movefrom, user_moveto)
    current = new
            
    return current.check_game_end()

# executes the engine's move
def engine_play(square_eval, time_limit, difficulty):
    global tree_root
    global current
    
    tree_root.base_evaluate(square_eval, time_limit)

    movefrom = tree_root.best_movefrom
    moveto = tree_root.best_moveto
    if difficulty < 100:

        # find all move possibilities
        choices = []
        s = len(tree_root.children)
        for i in range(s):
            choices.append(tree_root.children[i])
        
        # sort the move possibilities from best to worst
        if current.turn % 2 == 1:
            for i in range(s):
                for j in range(i + 1, s):
                    if choices[i] > choices[j]:
                        temp = choices[i]
                        choices[i] = choices[j]
                        choices[j] = temp
        else:
            for i in range(s):
                for j in range(i + 1, s):
                    if choices[i].eval < choices[j].eval:
                        temp = choices[i]
                        choices[i] = choices[j]
                        choices[j] = temp
        
        # randomly choose a move weighted based on difficulty
        r = random.binomialvariate(s - 1, float(100 - difficulty) / 200.0)
        movefrom = choices[r].movefrom
        moveto = choices[r].moveto

    new = current.execute_move(movefrom, moveto)
    current = new
            
    return current.check_game_end()

# main game loop that controls game progression
def game_loop(difficulty):
    global current


    keep_playing = True
    engine_plays_white = True
    answer = ""
    reprompt = True
    game_over = False
    game_status = 0
    
    # maximum length of time (microseconds) the engine is allowed to spend evaluating each move
    time_limit = 2000000

    while keep_playing:

        current.setup_board()
        game_over = False

        reprompt = True

        while reprompt:

            print("\nWould you like to play as white or black? (w/b)\n\n")
            answer = input()
            reprompt = False
            if answer == 'w' or answer == 'W' or answer == 'white' or answer == 'White':
                engine_plays_white = False
            elif answer == 'b' or answer == 'B' or answer == 'black' or answer == 'Black':
                engine_plays_white = True
            else:
                reprompt = True
                print("\nThe answer must be one of the following: \"w\", \"W\", \"white\", \"White\", \"b\", \"B\", \"black\", \"Black\".\n\n")

        # engine plays first move if playing white
        if engine_plays_white:
            
            game_status = engine_play(square_eval, time_limit, difficulty)

            if game_status > 0:
                game_over = True
                match game_status:
                    case 1:
                        print("\nGame over! White wins by checkmate. Enter \"x\" to leave, or anything else to play again.  ")
                    case 2:
                        print("\nGame over! Black wins by checkmate. Enter \"x\" to leave, or anything else to play again.  ")
                    case 3:
                        print("\nGame over! Draw by stalemate. Enter \"x\" to leave, or anything else to play again.  ")
                answer = input()
                if answer == 'x' or answer == 'X': return
            if game_over: continue

        # loop until the game ends
        while True:

            game_status = player_play()

            if game_status > 0:
                game_over = True
                match game_status:
                    case 1:
                        print("\nGame over! White wins by checkmate. Enter \"x\" to leave, or anything else to play again.  ")
                    case 2:
                        print("\nGame over! Black wins by checkmate. Enter \"x\" to leave, or anything else to play again.  ")
                    case 3:
                        print("\nGame over! Draw by stalemate. Enter \"x\" to leave, or anything else to play again.  ")
                answer = input()
                if answer == 'x' or answer == 'X': return
            if game_over: break
                
            game_status = engine_play(square_eval, time_limit, difficulty)

            if game_status > 0:
                game_over = True
                match game_status:
                    case 1:
                        print("\nGame over! White wins by checkmate. Enter \"x\" to leave, or anything else to play again.  ")
                    case 2:
                        print("\nGame over! Black wins by checkmate. Enter \"x\" to leave, or anything else to play again.  ")
                    case 3:
                        print("\nGame over! Draw by stalemate. Enter \"x\" to leave, or anything else to play again.  ")
                answer = input()
                if answer == 'x' or answer == 'X': return
            if game_over: break


# analyze the position of the current node
def analyze_position(time_limit):
    global current

    print("Analyzing this position...\n\n")
    tree_root.base_evaluate(square_eval, time_limit)

    moves = []
    for i in current.children:
        moves.append(i)

    s = len(moves)
    for i in range(s):
        for j in range(i + 1, s):
            if(current.turn % 2 == 1 and moves[i].eval > moves[j].eval):
                temp = moves[i]
                moves[i] = moves[j]
                moves[j] = temp
            if(current.turn % 2 == 0 and moves[i].eval < moves[j].eval):
                temp = moves[i]
                moves[i] = moves[j]
                moves[j] = temp

    piece_codes = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    file_codes = ["a", "b", "c", "d", "e", "f", "g", "h"]
    rank_codes = ["1", "2", "3", "4", "5", "6", "7", "8"]

    # print each move followed by its respective eval
    for i in range(s):
        print(piece_codes[current.board[moves[i].movefrom]] + file_codes[moves[i].movefrom % 8] + rank_codes[int(moves[i].movefrom / 8)] + file_codes[moves[i].moveto % 8] + rank_codes[int(moves[i].moveto / 8)] + "      " + moves[i].eval + "\n")
        



# parse a user-entered fen code
def parse_fen(answer):
    global current

    l = len(answer)
    p = current.pieces
    p = [[] * 12]
    b = current.board
    for i in range(64):
        b[i] = -1
    s = 0

    spot = 0
    rank = 7
    file = 0
    while rank >= 0:
        while file < 8:
            s = rank * 8 + file
            match answer[spot]:
                case '/':
                    rank -= 1
                    file = 0
                case 'P':
                    p[0].append(s)
                    b[s] = 0
                    file += 1
                case 'N':
                    p[1].append(s)
                    b[s] = 1
                    file += 1
                case 'B':
                    p[2].append(s)
                    b[s] = 2
                    file += 1
                case 'R':
                    p[3].append(s)
                    b[s] = 3
                    file += 1
                case 'Q':
                    p[4].append(s)
                    b[s] = 4
                    file += 1
                case 'K':
                    p[5].append(s)
                    b[s] = 5
                    file += 1
                case 'p':
                    p[6].append(s)
                    b[s] = 6
                    file += 1
                case 'n':
                    p[7].append(s)
                    b[s] = 7
                    file += 1
                case 'b':
                    p[8].append(s)
                    b[s] = 8
                    file += 1
                case 'r':
                    p[9].append(s)
                    b[s] = 9
                    file += 1
                case 'q':
                    p[10].append(s)
                    b[s] = 10
                    file += 1
                case 'k':
                    p[11].append(s)
                    b[s] = 11
                    file += 1
                        
            if ord(answer[spot]) >= ord('1') and ord(answer[spot]) <= ord('8'):
                file += int(answer[spot])

                spot += 1
                if spot >= l:
                    print("The FEN code incorrectly ended before all board squares were filled.\n\n")
                    return 1

    if answer[spot] != ' ':
        print("No space was detected after the board sequence.\n\n")
        return 1
    spot += 1
    if spot >= l:
        print("The FEN code incorrectly ended before the turn indicator.\n\n")
        return 1
    
    if answer[spot] != 'w' or answer[spot] != 'b':
        print("No 'w' or 'b' character indicating turn was detected after the board sequence.\n\n")
        return 1
    if answer[spot] == 'w':
        current.turn = 0
    else:
        current.turn = 1
    spot += 1

    if spot >= l:
        print("The FEN code incorrectly ended after the turn indicator.\n\n")
        return 1
    if answer[spot] != ' ':
        print("No space was detected after the turn indicator.\n\n")
        return 1
    while(answer[spot] == ' '):
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended after the turn indicator.\n\n")
            return 1

    for i in range(4):
        current.miscs[i] = 0
    current.miscs[4] = -1
    current.miscs[5] = 0

    if answer[spot] == 'K':
        current.miscs[0] = 1 # WK
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended during the castling indicator.\n\n")
            return 1
    if answer[spot] == 'Q':
        current.miscs[1] = 1 # WQ
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended during the castling indicator.\n\n")
            return 1
    if answer[spot] == 'k':
        current.miscs[2] = 1 # BK
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended during the castling indicator.\n\n")
            return 1
    if answer[spot] == 'q':
        current.miscs[3] = 1 # BQ
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended during the castling indicator.\n\n")
            return 1
    while answer[spot] == ' ' or answer[spot] == '-':
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended after the castling indicator.\n\n")
            return 1
    if ord(answer[spot]) >= ord('a') and ord(answer[spot]) <= ord('h'):
        current.miscs[4] = answer[spot] - 'a' # en passant
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended during the en passant indicator.\n\n")
            return 1
        if answer[spot] != ' ':
            spot += 1
            if spot >= l:
                print("The FEN code incorrectly ended during the en passant indicator.\n\n")
                return 1
    while answer[spot] == ' ' or answer[spot] == '-':
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended after the en passant indicator.\n\n")
            return 1
        
    while ord(answer[spot]) >= ord('0') and ord(answer[spot]) <= ord('9'):
        if(current.miscs[5] > 99):
            print("The FEN code incorrectly ended because the 50-move rule indicator was too large.\n\n")
            return 1
        current.miscs[5] *= 10
        current.miscs[5] += int(answer[spot])
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended during the 50-move rule indicator.\n\n")
            return 1
    while not (ord(answer[spot]) >= '0' and ord(answer[spot]) <= ord('9')):
        spot += 1
        if spot >= l:
            print("The FEN code incorrectly ended after the 50-move rule indicator.\n\n")
            return 1
    turn = 0
    while ord(answer[spot]) >= ord('0') and ord(answer[spot]) <= ord('9'):
        if turn > 99:
            print("The FEN code incorrectly ended because the 50-move rule indicator was too large.\n\n")
            return 1
        turn *= 10
        turn += int(answer[spot])
        spot += 1
        if spot >= l:
            current.turn += turn
            return 0
    
    return 0

def main():

    while True:

        print("Enter a board position FEN code for a position analysis or type a number from 0 to 1 million to train the engine for that many seconds.")
        print("Or enter an empty answer to play against the engine.\n")
        answer = input()
        l = len(answer)
        valid = False

        if l == 0: # play against engine

            while True:

                print("Enter a number from 0 to 100 to play against the engine at that difficulty level.\n")
                print("Level 0 is approximately 1000 ELO; Level 100 is the maximum engine ability at approximately 2100 ELO.\n")
                answer0 = input()
                l0 = len(answer0)

                if answer0.isnumeric():
                    num = int(answer0)
                    if num >= 0 and num <= 100:
                        game_loop(num)
                        continue

                print("Your answer must be a number from 0 to 100.\n")

                game_loop(100)
                continue
        elif answer.isnumeric(): # train
            num = int(answer)
            if num >= 0 and num <= 1000000:
                train(1000, num * 1000000, 1.0, 2.0, -2.0)
                continue
            print("Your answer must be a number from 0 to 1000000 to train the engine.\n\n")
        else: # load FEN position
            
            if parse_fen(answer): # parse the fen code and analyze the position if it is valid
                continue
            else:
                analyze_position(1000000)

main()
