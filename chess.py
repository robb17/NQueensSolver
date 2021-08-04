from copy import deepcopy
from math import inf

STRAIGHT = 0
DIAGONAL = 1
L = 2
NONE = 3

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
		if self.pattern_string == STRAIGHT:
			return (starting_x == x and self.distance >= abs(starting_x - x)) or (starting_y == y and self.distance >= abs(starting_y - y))
		elif self.pattern_string == DIAGONAL:
			return abs((y - starting_y) / (x - starting_x)) == 1 and self.distance >= abs(y - starting_y)
		elif self.pattern_string == L:
			return (abs(x - starting_x) == 1 and abs(y - starting_y) == 2) or (abs(x - starting_x) == 2 and abs(y - starting_y) == 1)
		elif self.pattern_string == NONE:
			return False

	def all_subsequent_threatened_locations(self, x, y, length):
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
			for i in range(0, len(dloc)):
				if dloc[i] + x >= 0 and dloc[i] + x < length and dloc[i] + y >= 0 and dloc[i] + y < length:
					locations.append((dloc[i] + x, dloc[i] + y))
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

ALL_REPRESENTATIONS = {
	KING: "K",
	QUEEN: "Q",
	ROOK: "R",
	KNIGHT: "K",
	BISHOP: "B",
	PAWN: "P",
	NONE: "-",
	MARKED_NULL: "!"
}

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

	def all_subsequent_threatened_locations(self, x, y, length):
		locations = []
		for pattern in self.threat_patterns:
			locations += pattern.all_subsequent_threatened_locations(x, y, length)
		return locations

	def __str__(self):
		#if self.type == NONE and len(self.threats) > 0:
		#	return ALL_REPRESENTATIONS[MARKED_NULL]
		return ALL_REPRESENTATIONS[self.type]

	def __hash__(self):
		return self.x * 1000 + self.y

NULLPIECE = Piece(-1, -1, NONE)

class Queen(Piece):
	def __init__(self, x, y):
		super().__init__(x, y, QUEEN)

class Board:
	def __init__(self, n):
		self.board = []
		for x in range(0, n):
			self.board.append([Piece(x, y, NONE) for y in range(0, n)])
		self.size = n
		self.pieces = {}

	def all_pieces(self):
		return self.pieces

	def add_piece(self, piece, mark_new_threats=False):
		self.pieces[piece] = piece
		self.board[piece.x][piece.y] = piece
		if mark_new_threats:
			self.add_threats(piece.all_subsequent_threatened_locations(piece.x, piece.y, self.size), piece)

	def remove_piece(self, piece, remove_threats=False):
		self.pieces.pop(piece)
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

	def is_new_position_unthreatened(self, x, y):
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
