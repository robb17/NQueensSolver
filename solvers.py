import chess
from itertools import permutations
import random
import math
import argparse

class SlightlyIntelligentBruteForceSolver:
	''' Brute force solver that makes use of the fact that there can exist at most one queen per row and at most one queen per column
	'''
	def __init__(self, length):
		self.board = None
		self.length = length

	def solve(self):
		all_allowed_permutations = []
		x = [i for i in range(0, self.length)]
		y = [i for i in range(0, self.length)]
		all_y_perms = list(permutations(y))
		for i in range(0, len(all_y_perms)):
			current_matching = []
			self.board = chess.Board(self.length)
			is_valid_board = True
			for j in x: # keep adding pieces using x, y_permutations until one addition violates constraints
				if not self.board.is_new_position_unthreatened(j, all_y_perms[i][j]):
					is_valid_board = False
					break
				new_queen = chess.Queen(j, all_y_perms[i][j])
				self.board.add_piece(new_queen)
			if is_valid_board:
				return self.board
		return self.board

class BasicBacktrackingSolver:
	'''
	'''
	def __init__(self, length):
		self.board = chess.Board(length)
		self.length = length
		self.queen_stack = []			#  for later backtracking: remove the most recent queen when in deadlock
		self.disallowed_y = {}

	def _add_constraint(self, x, y):
		new_queen = chess.Queen(x, y)
		self.queen_stack.append(new_queen)
		self.board.add_piece(new_queen)
		self.disallowed_y[y] = True
		return x, len(self.board) - 1	#  can be immediately certain that there are no other valid placements in the row

	def _remove_constraint(self):
		mru_queen = self.queen_stack.pop()
		self.board.remove_piece(mru_queen)
		self.disallowed_y.pop(mru_queen.y)
		return mru_queen.x, mru_queen.y	#  set x, y back to old queen's location

	def solve(self):
		x = 0
		while x <= len(self.board):
			y = 0
			if x >= len(self.board):
				x, y = self._remove_constraint()
				y += 1
			while y < len(self.board):
				if self.disallowed_y.get(y): 	#  optimization: if queen exists in column, no other queens can be placed here
					y += 1
					continue
				if self.board.is_new_position_unthreatened(x, y):
					x, y = self._add_constraint(x, y)
					if len(self.queen_stack) == self.length:			#  can only ever reach solved state on addition
						return self.board
				y += 1
			x += 1

class HeuristicSolver:
	''' Randomly populate a board and correct challenges––starting with pieces that are most exposed first
	'''
	def __init__(self, length):
		self.board = chess.Board(length)
		self.length = length

	def solve(self):

		#  initialize board
		for x in range(0, self.length):
			self.board.add_piece(chess.Queen(x, x))
		self.board.determine_threats()

		while self.board.is_at_least_one_threat():

			#  find queen to move
			all_queens = list(self.board.all_pieces())
			all_queens.sort(key=lambda q: len(q.threats), reverse=True)
			maxima = []
			i = 0
			while i < len(self.board) and len(all_queens[i].threats) == len(all_queens[0].threats):
				maxima.append(all_queens[i])
				i += 1
			queen_to_move = random.choice(maxima) #  avoid some local minima
			self.board.remove_piece(queen_to_move)
			for piece in self.board.all_pieces():
				if queen_to_move.is_threatening(piece.x, piece.y):
					piece.remove_threat(queen_to_move)

			# find best position to move it to
			minima = []
			minimum_threats = len(queen_to_move.threats)
			for x in range(0, self.length):
				for y in range(0, self.length):
					n_threats = 0
					for piece in self.board.all_pieces():
						if x == piece.x and y == piece.y:
							n_threats = math.inf
							continue
						if piece.is_threatening(x, y):
							n_threats += 1
					if n_threats <= minimum_threats:
						if n_threats < minimum_threats:
							minima = [(x, y)]
						else:
							minima.append((x, y))
						minimum_threats = n_threats

			# apply the move
			coordinates = random.choice(minima) #  avoid some local minima
			new_queen = chess.Queen(coordinates[0], coordinates[1])
			for piece in self.board.all_pieces():
				if new_queen.is_threatening(piece.x, piece.y):
					piece.add_threat(new_queen)
				if piece.is_threatening(new_queen.x, new_queen.y):
					new_queen.add_threat(piece)
			self.board.add_piece(new_queen)
		return self.board

if __name__ == "__main__":
	types = {"brute_force": [SlightlyIntelligentBruteForceSolver],
			"backtracking": [BasicBacktrackingSolver],
			"heuristic": [HeuristicSolver],
			"all": [SlightlyIntelligentBruteForceSolver, BasicBacktrackingSolver, HeuristicSolver]}
	parser = argparse.ArgumentParser(description='Solve the n-queens problem via several methods.')
	parser.add_argument('length', metavar='S', help='the size of the chess board', type=int)
	parser.add_argument('type', metavar='T', help='select the type of method used for solving', default="all", choices=types.keys())
	args = parser.parse_args()
	if args.type in types:
		for c in types[args.type]:
			instance = c(args.length)
			board = instance.solve()
			print(board)
