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
	NONE: "-"
}

class Piece:
	def __init__(self, x, y, type=""):
		self.x = x
		self.y = y
		self.threat_patterns = ALL_PATTERNS[type]
		self.type = type

	def is_threatening(self, x, y):
		for pattern in self.threat_patterns:
			if pattern.is_threatening(self.x, self.y, x, y):
				return True
		return False

	def __str__(self):
		return ALL_REPRESENTATIONS[self.type]

	def __hash__(self):
		return self.x * 1000 + self.y

NULLPIECE = Piece(-1, -1, NONE)

class Queen(Piece):
	def __init__(self, x, y):
		super().__init__(x, y, QUEEN)

class Board:
	def __init__(self, n):
		self.board = [NULLPIECE] * n
		self.board = [deepcopy(self.board) for x in range(0, n)]
		self.size = n
		self.pieces = {}

	def all_pieces(self):
		return self.pieces

	def add_piece(self, piece):
		self.pieces[piece] = piece
		self.board[piece.x][piece.y] = str(piece)

	def remove_piece(self, piece):
		self.pieces.pop(piece)
		self.board[piece.x][piece.y] = str(NULLPIECE)

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
