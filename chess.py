from copy import deepcopy
from math import inf
from association_table import AssociationTable

STRAIGHT = 0
DIAGONAL = 1
L = 2
NONE = 9

KING = 0
QUEEN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
PAWN = 5
MARKED_NULL = 6

class ThreatPattern:
	def __init__(self, pattern_string, distance):
		self.pattern_string = pattern_string
		self.distance = distance

	def is_threatening(self, starting_x, starting_y, x, y):
		if starting_x == x and starting_y == y:
			return False
		if self.pattern_string == STRAIGHT:
			return (starting_x == x and self.distance >= abs(starting_x - x)) or (starting_y == y and self.distance >= abs(starting_y - y))
		elif self.pattern_string == DIAGONAL:
			return abs((y - starting_y) / (x - starting_x)) == 1 and self.distance >= abs(y - starting_y)
		elif self.pattern_string == L:
			return (abs(x - starting_x) == 1 and abs(y - starting_y) == 2) or (abs(x - starting_x) == 2 and abs(y - starting_y) == 1)
		elif self.pattern_string == NONE:
			return False

	def all_subsequent_threatened_locations(self, x, y, length):
		''' Gives all threatened locations for x' in x < x' < length 
			and y' in y < y' < length
		'''
		locations = []
		if self.pattern_string == STRAIGHT:
			x_temp = x + 1
			while x_temp < length:
				locations.append((x_temp, y))
				x_temp += 1
			y += 1
			while y < length:
				locations.append((x, y))
				y += 1
		elif self.pattern_string == DIAGONAL:
			x_temp = x + 1
			y_temp = y - 1
			x += 1
			y += 1
			while x_temp < length and y_temp >= 0:
				locations.append((x_temp, y_temp))
				x_temp += 1
				y_temp -= 1
			while x < length and y < length:
				locations.append((x, y))
				x += 1
				y += 1
		elif self.pattern_string == L:
			dx = [1, -1, 2, -2]
			dy = [2, 2, 1, 1]	# y strictly increases
			for i in range(0, len(dx)):
				if dx[i] + x >= 0 and dx[i] + x < length and dy[i] + y >= 0 and dy[i] + y < length:
					locations.append((dx[i] + x, dy[i] + y))
		return locations

ALL_PATTERNS = {
	KING: [ThreatPattern(STRAIGHT, 1), ThreatPattern(DIAGONAL, 1)],
	QUEEN: [ThreatPattern(STRAIGHT, inf), ThreatPattern(DIAGONAL, inf)],
	ROOK: [ThreatPattern(STRAIGHT, inf)],
	KNIGHT: [ThreatPattern(L, None)],
	BISHOP: [ThreatPattern(DIAGONAL, inf)],
	PAWN: [ThreatPattern(DIAGONAL, 1)],
	NONE: [ThreatPattern(NONE, None)]
	}

ALL_REPRESENTATIONS = AssociationTable({	# support bidirectional indexing
	KING: "K",
	QUEEN: "Q",
	ROOK: "R",
	KNIGHT: "K",
	BISHOP: "B",
	PAWN: "P",
	NONE: "-",
	MARKED_NULL: "!"
})

class Piece:
	def __init__(self, x, y, type=""):
		self.x = x
		self.y = y
		self.threat_patterns = ALL_PATTERNS[type]
		self.type = type
		self.threats = {}

	def is_threatening(self, x, y):
		for pattern in self.threat_patterns:
			if pattern.is_threatening(self.x, self.y, x, y):
				return True
		return False

	def add_threat(self, piece):
		self.threats[piece] = True

	def remove_threat(self, piece):
		self.threats.pop(piece)

	def is_unthreatened(self):
		return len(self.threats) == 0

	def all_subsequent_threatened_locations(self, x, y, length):
		locations = []
		for pattern in self.threat_patterns:
			locations += pattern.all_subsequent_threatened_locations(x, y, length)
		return locations

	def __str__(self):
		#if self.type == NONE and len(self.threats) > 0:
		#	return ALL_REPRESENTATIONS[MARKED_NULL]
		return ALL_REPRESENTATIONS[self.type]

	def __int__(self):
		return self.type

	def __hash__(self):
		return self.x * 10000 + self.y

class Queen(Piece):
	def __init__(self, x, y):
		super().__init__(x, y, QUEEN)

class Board:
	def __init__(self, n, filename=None):
		self.size = n
		self.non_dummy_pieces = {}
		if filename:
			self.load_from_file(filename)
		else:
			self.board = []
			for x in range(0, n):
				self.board.append([Piece(x, y, NONE) for y in range(0, n)])

	def load_from_file(self, filename):
		self.board = []
		row = []
		x = 0
		y = 0
		self.size = None
		with open(filename, "r") as rep:
			for line in rep:
				for c in line:
					if c == " ":
						continue
					elif ALL_REPRESENTATIONS.get(c):
						piece = Piece(x, y, ALL_REPRESENTATIONS[c])
						if ALL_REPRESENTATIONS[c] != NONE and ALL_REPRESENTATIONS[c] != MARKED_NULL:
							self.non_dummy_pieces[piece] = piece
						row.append(piece)
						y += 1
				self.board.append(row)
				row = []
				if not self.size:
					self.size = y
				elif y != self.size:
					print("malformed board: variable width")
					exit(1)
				x += 1
				y = 0
			if not ((x == self.size and y == 0) or (x == self.size - 1 and y == self.size - 1)):
				print("malformed board: height does not match width")
				exit(1)
		print("Load complete")
		print(self)

	def all_pieces(self):
		return self.non_dummy_pieces

	def add_piece(self, piece, mark_new_threats=False):
		self.non_dummy_pieces[piece] = piece
		self.board[piece.x][piece.y] = piece
		if mark_new_threats:
			self.add_threats(piece.all_subsequent_threatened_locations(piece.x, piece.y, self.size), piece)

	def remove_piece(self, piece, remove_threats=False):
		self.non_dummy_pieces.pop(piece)
		self.board[piece.x][piece.y] = Piece(piece.x, piece.y, NONE)
		if remove_threats:
			self.remove_threats(piece.all_subsequent_threatened_locations(piece.x, piece.y, self.size), piece)

	def determine_threats(self):
		for theatened_piece in self.all_pieces():
			for piece in self.all_pieces():
				if piece.is_threatening(theatened_piece.x, theatened_piece.y):
					theatened_piece.add_threat(piece)

	def add_threats(self, locations, threatening_piece):
		for location in locations:
			self.board[location[0]][location[1]].add_threat(threatening_piece)

	def remove_threats(self, locations, threatening_piece):
		for location in locations:
			if threatening_piece.is_threatening(location[0], location[1]):
				self.board[location[0]][location[1]].remove_threat(threatening_piece)

	def is_entire_row_threatened(self, x):
		row = self[x]
		for piece in row:
			if len(piece.threats) == 0:
				return False
		return True

	def no_queens_in_row(self, x):
		for piece in self[x]:
			if piece.type == QUEEN:
				return False
		return True

	def is_at_least_one_threat(self):
		for piece in self.all_pieces():
			if len(piece.threats) > 0:
				return True
		return False

	def is_new_position_unthreatened(self, x, y, downward_opt=True):
		if downward_opt:
			return self.board[x][y].is_unthreatened()
		else:
			for piece in self.all_pieces():
				if piece.is_threatening(x, y):
					return False
			return True

	def __str__(self):
		string_rep = "\n"
		for row in self.board:
			for piece in row:
				string_rep += str(piece) + " "
			string_rep += "\n"
		return string_rep

	def __setitem__(self, x, val):
		self.board[x] = val

	def __getitem__(self, x):
		return self.board[x]

	def __len__(self):
		return self.size

	def __hash__(self):
		hsh = 0
		for x in range(0, self.size):
			for y in range(0, self.size):
				hsh *= 10
				hsh += int(self.board[x][y])
		return hsh
