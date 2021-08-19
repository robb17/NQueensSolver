import chess
from itertools import permutations
import random
import math
import argparse
import time

class SlightlyIntelligentBruteForceSolver:
	''' Brute force solver that makes use of the fact that there can exist at most one queen per row and at most one queen per column
	'''
	def __init__(self, size):
		self.board = None
		self.size = size

	def solve(self):
		all_allowed_permutations = []
		x = [i for i in range(0, self.size)]
		y = [i for i in range(0, self.size)]
		all_y_perms = list(permutations(y))
		for i in range(0, len(all_y_perms)):
			current_matching = []
			self.board = chess.Board(self.size)
			is_valid_board = True
			for j in x: # keep adding pieces using x, y_permutations until one addition violates constraints
				if not self.board.is_new_position_unthreatened(j, all_y_perms[i][j], downward_opt=False):
					is_valid_board = False
					break
				new_queen = chess.Queen(j, all_y_perms[i][j])
				self.board.add_piece(new_queen, mark_new_threats=True)
			if is_valid_board:
				return self.board
		return self.board

class BasicBacktrackingSolver:
	''' Bread and butter
	'''
	def __init__(self, size):
		self.board = chess.Board(size)
		self.size = size
		self.queen_stack = []			#  for later backtracking: remove the most recent queen when in deadlock
		self.disallowed_y = {}

	def _add_constraint(self, x, y):
		new_queen = chess.Queen(x, y)
		self.queen_stack.append(new_queen)
		self.board.add_piece(new_queen, mark_new_threats=True)
		self.disallowed_y[y] = True
		return x, len(self.board) - 1	#  can be immediately certain that there are no other valid placements in the row

	def _remove_constraint(self):
		mru_queen = self.queen_stack.pop()
		self.board.remove_piece(mru_queen, remove_threats=True)
		self.disallowed_y.pop(mru_queen.y)
		return mru_queen.x, mru_queen.y	#  set x, y back to old queen's location

	def solve(self):
		x = 0
		while x <= self.size:
			y = 0
			if x >= self.size:
				x, y = self._remove_constraint()
				y += 1
			while y < self.size:
				if self.disallowed_y.get(y): 	#  optimization: if queen exists in column, no other queens can be placed here
					y += 1
					continue
				if self.board.is_new_position_unthreatened(x, y):
					x, y = self._add_constraint(x, y)
					if len(self.queen_stack) == self.size:		#  can only ever reach solved state on addition
						return self.board
				y += 1
			x += 1

class BacktrackingLookaheadSolver:

	def __init__(self, size):
		self.board = chess.Board(size)
		self.size = size
		self.queen_stack = []

	def pop_queen(self, x, y):
		mru_queen = self.queen_stack.pop()
		self.board.remove_piece(mru_queen, remove_threats=True)
		return mru_queen.x, mru_queen.y

	def solve(self):
		x = 0
		while x <= self.size:
			y = 0
			while y < self.size:
				if self.board.is_new_position_unthreatened(x, y):
					new_queen = chess.Queen(x, y)
					self.queen_stack.append(new_queen)
					self.board.add_piece(new_queen, mark_new_threats=True)
					if len(self.queen_stack) == self.size:		#  can only ever reach solved state on addition
						return self.board
					if (x < self.size - 1 and self.board.is_entire_row_threatened(x + 1)):
						x, y = self.pop_queen(x, y)
				if (x == self.size - 1 and y == self.size - 1) or (y == self.size - 1 and self.board.no_queens_in_row(x)):
					x, y = self.pop_queen(x, y)
					if y == self.size - 1 and self.board.no_queens_in_row(x):  # possible that the most recent queen was in the far-right column
						x, y = self.pop_queen(x, y)
				y += 1
			x += 1

class HeuristicSolver:
	''' Populate a board naively and correct challenges––starting with pieces that are most exposed first
	'''
	def __init__(self, size, filename=None):
		self.board = chess.Board(size, filename)
		self.size = size
		self.prior_states = {}
		self.relaxed_selection = False
		self.relaxed_placement = False

	def set_constraint_relaxation(self, type):
		if type == "placement":
			self.relaxed_placement = True
		elif type == "selection":
			self.relaxed_selection = True

	def solve(self):

		#  initialize board
		if len(self.board.all_pieces()) == 0:
			for x in range(0, self.size):
				self.board.add_piece(chess.Queen(x, x))
		self.board.determine_threats()
		relaxed_constraints = False

		while self.board.is_at_least_one_threat():

			#  find queen to move
			all_queens = list(self.board.all_pieces())
			queen_to_move = None
			if relaxed_constraints and self.relaxed_selection:
				queen_to_move = random.choice(all_queens)
				relaxed_constraints = False
			else:
				all_queens.sort(key=lambda q: len(q.threats), reverse=True)
				maxima = []
				i = 0
				while i < len(self.board) and len(all_queens[i].threats) == len(all_queens[0].threats):
					maxima.append(all_queens[i])
					i += 1
				queen_to_move = random.choice(maxima) #  avoid some local minima

			# remove the queen
			self.board.remove_piece(queen_to_move)
			for piece in self.board.all_pieces():
				if queen_to_move.is_threatening(piece.x, piece.y):
					piece.remove_threat(queen_to_move)

			# find best position to move it to
			minima = []
			coordinates = None
			if relaxed_constraints and self.relaxed_placement:
				coordinates = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
			else:
				minimum_threats = math.inf
				for x in range(0, self.size):
					for y in range(0, self.size):
						if x == queen_to_move.x and y == queen_to_move.y:	# don't move to old location
							continue
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
				coordinates = random.choice(minima) #  avoid some local minima
			# apply the move
			new_queen = chess.Queen(coordinates[0], coordinates[1])
			for piece in self.board.all_pieces():
				if new_queen.is_threatening(piece.x, piece.y):
					piece.add_threat(new_queen)
				if piece.is_threatening(new_queen.x, new_queen.y):
					new_queen.add_threat(piece)
			self.board.add_piece(new_queen)
			if self.prior_states.get(self.board.__hash__()):
				relaxed_constraints = True
			else:
				self.prior_states[self.board.__hash__()] = True
		return self.board

class H1(HeuristicSolver):
	def __init__(self, size, filename=None):
		super().__init__(size, filename)
		super().set_constraint_relaxation("placement")

class H2(HeuristicSolver):
	def __init__(self, size, filename=None):
		super().__init__(size, filename)
		super().set_constraint_relaxation("selection")

def average(lst):
	acc = 0
	for i in lst:
		acc += i
	return acc / len(lst)

if __name__ == "__main__":
	types = {"brute_force": [SlightlyIntelligentBruteForceSolver],
			"backtracking": [BasicBacktrackingSolver],
			"h1": [H1],
			"h2": [H2],
			"lookahead": [BacktrackingLookaheadSolver],
			"all": [H1, H2, BacktrackingLookaheadSolver, BasicBacktrackingSolver, SlightlyIntelligentBruteForceSolver]}
	types_keys = list(types.keys())
	formatted_types = "".join(x + ", " for x in types_keys[:-1])
	formatted_types += types_keys[-1]

	parser = argparse.ArgumentParser(description='Solve the n-queens problem via several methods.')
	parser.add_argument('size', metavar='S', help='the size of the chess board', type=int)
	parser.add_argument('type', metavar='T', nargs="*", help='select the type of method used in finding a \
			solution. Available types:' + formatted_types, default="all", choices=types_keys)
	parser.add_argument('-l', "--load", help='load a file containing a representation of \
			the ' + "board's" + ' starting state––allowed only if solving with "h1" or "h2"')
	args = parser.parse_args()

	if isinstance(args.type, str):
		args.type = [args.type]
	all_times_1 = []
	all_times_2 = []
	for t in args.type:
		for c in types[t]:
			t1 = time.time()
			instance = c(args.size) if c != H1 and c != H2 else c(args.size, args.load)
			if (c != H1 and c != H2) and args.load:
				print("Specified starting board state was NOT used in determining the following solution:")
			board = instance.solve()
			print(board)
			print("Finished in " + str(round(time.time() - t1, 2)) + " seconds")

