import Chess

class BasicRecursiveSolver:
	def __init__(self, length):
		self.board = Chess.Board(length)
		self.solve()

	def solve(self):
		for x in range(0, len(self.board)):
			for y in range(0, len(self.board)):
				for queen in self.board.all_pieces():
					if not queen.is_threatening(x, y):
						queen = Chess.Queen(x, y)
						self.board.add_piece(x, y)
		print(self.board)