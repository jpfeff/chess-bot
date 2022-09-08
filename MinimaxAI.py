# Modified by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/11/2021

import chess
import time

class MinimaxAI():
    def __init__(self, depth):
        # hold number of calls to value function for testing
        self.num_calls = 0
        self.depth = depth
        self.best_move = None
        # values from https://stackoverflow.com/questions/59039152/python-chess-minimax-algorithm-how-to-play-with-black-pieces-bot-has-white
        self.position_values = {
            "p":    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
                     5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
                     1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0,
                     0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5,
                     0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0,
                     0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5,
                     0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5,
                     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],

            "n":    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
                     -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0,
                     -3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0,
                     -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0,
                     -3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0,
                     -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0,
                     -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0,
                     -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],

            "b":    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                     -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                     -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
                     -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
                     -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
                     -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
                     -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
                     -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],

            "r":    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0,
                     0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5,
                     -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                     -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                     -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                     -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                     -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                     0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0],

            "q":    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
                     -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                     -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                     -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                     -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                     -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                     -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
                     -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],

            "k":    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                     -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                     -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                     -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                     -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                     -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                     2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0,
                     2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]}

    # chooses the best move given the minimax algorithm
    def choose_move(self, board):
        start = time.time()
        self.num_calls = 0
        # intiialize value of best move to be negative infinity
        best_move_value = float('-inf')
        # to hold the actual move to be pushed
        best_move = None
        # get next moves
        moves = list(board.legal_moves)
        # loop over possible moves
        for move in moves:
            # update the board
            board.push(move)
            # calculate the value of the move
            value = self.value(board, self.depth, True)
            # undo the move
            board.pop()
            # if the new value is better than the current best value
            if value > best_move_value:
                # store the new value and move
                best_move_value = value
                best_move = move
        print("Best value: ", best_move_value)
        print("Nodes searched:", self.num_calls)
        end = time.time()
        print("Time elapsed:", end-start)
         # return the best move
        return best_move

    # root of minimax algorithm
    def value(self, board, depth, is_maximizer):
        self.num_calls += 1
        # if cutoff_test returns true (we have reached the depth or a terminal state)
        if self.cutoff_test(board, depth):
            # evaluate the board
            return self.evaluate(board)
        # otherwise run max_value if agent is maximizer
        if is_maximizer:
            return self.max_value(board, depth, is_maximizer)
        # and min_value otherwise
        else:
            return self.min_value(board, depth, is_maximizer)

    # max_value helper function for minimax
    def max_value(self, board, depth, is_maximizer):
        # initialize value to negative infinity
        v = float('-inf')
        # get list of moves
        moves = list(board.legal_moves)
        # loop over moves, pushing them onto the board
        for move in moves:
            board.push(move)
            # assign the max of the current value and a recursive call to minimax to v
            v = max(v, self.value(board, depth-1, not is_maximizer))
            # undo move
            board.pop()
        # return final value
        return v

    # min_value helper function for minimax
    def min_value(self, board, depth, is_maximizer):
        # initialize value to negative infinity
        v = float('inf')
        # get list of moves
        moves = list(board.legal_moves)
        # loop over moves, pushing them onto the board
        for move in moves:
            board.push(move)
            # assign the min of the current value and a recursive call to minimax to v
            v = min(v, self.value(board, depth-1, not is_maximizer))
            # undo move
            board.pop()
        # return final value
        return v

    # returns true if we have reached the depth or a terminal state
    def cutoff_test(self, board, depth):
        if depth == 0 or board.is_game_over():
            return True
        return False

    # evaluates the state of the board, returning a value
    def evaluate(self, board):
        # initialize total values for each color to 0
        white_total_value = 0
        black_total_value = 0

        # loop over every position on the board
        for pos in range(64):
            cur_piece = board.piece_at(pos)
            # if there is no piece in the spot, do nothing
            if cur_piece == None:
                continue
            # if piece is white
            if cur_piece.color == chess.WHITE:
                # add the piece's value to total white value
                white_total_value += self.piece_value(str(cur_piece), pos)
            else:
                # otherwise add the piece's value to total black value
                black_total_value += self.piece_value(str(cur_piece), pos)
        # return the difference
        return black_total_value - white_total_value

    # values the pieces according to their utility and position
    def piece_value(self, piece, pos):
        if piece == None:
            return 0
        # normalizes case of piece symbol
        piece = piece.lower()

        # pawns are valued at 10, knights and bishops at 30, rooks at 50, queens at 90, and kings at 100
        # adds material value to positional score     
        if piece == "p":
            return self.position_values["p"][pos] + 10
        if piece == "n":
            return self.position_values["n"][pos] + 30
        if piece == "b":
            return self.position_values["b"][pos] + 30
        if piece == "r":
            return self.position_values["r"][pos] + 50
        if piece == "q":
            return self.position_values["q"][pos] + 90
        if piece == "k":
            return self.position_values["k"][pos] + 100

        return 0
