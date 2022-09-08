# Written by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/11/2021

from AlphaBetaAI import AlphaBetaAI

class IterativeDeepeningAI():
    # calls alpha-beta __init__ and stores depth (+1 to account for 0 depth search) as depth_limit
    def __init__(self, depth):
        AlphaBetaAI.__init__(self, depth)
        self.depth_limit = depth + 1
        self.best_move = None

    # sorts moves that involve captures to the front of the list because they are high-value moves
    def sort_moves(self, moves, board):
        return AlphaBetaAI.sort_moves(self, moves, board)

    # chooses the best move based on the alpha-beta pruning algorithm
    def choose_move(self, board):
        # iterates over depths from 0 to self.depth, calling the minimax function at each limit
        for depth in range(self.depth_limit):
            self.depth = depth
            self.best_move = AlphaBetaAI.choose_move(self, board)
        return self.best_move

    # root of alpha-beta algorithm
    def value(self, board, depth, alpha, beta, is_maximizer):
        return AlphaBetaAI.value(self, board, depth, alpha, beta, is_maximizer)

    # max_value helper function for alpha-beta
    def max_value(self, board, depth, alpha, beta, is_maximizer):
        return AlphaBetaAI.max_value(self, board, depth, alpha, beta, is_maximizer)

    # min_value helper function for alpha-beta
    def min_value(self, board, depth, alpha, beta, is_maximizer):
        return AlphaBetaAI.min_value(self, board, depth, alpha, beta, is_maximizer)

    # returns true if we have reached the depth or a terminal state
    def cutoff_test(self, board, depth):
        return AlphaBetaAI.cutoff_test(self, board, depth)

    # evaluates the state of the board, returning a value
    def evaluate(self, board):
        return AlphaBetaAI.evaluate(self, board)

    # values the pieces according to their utility and position
    def piece_value(self, piece, pos):
        return AlphaBetaAI.piece_value(self, piece, pos)

