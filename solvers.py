import chess

class BasicRecursiveSolver:
	def __init__(self, length, target_number):
		self.board = chess.Board(length)
		self.target_number = target_number

	def solve(self):
		queen_stack = []							#  for later backtracking: remove the most recent queen when in deadlock
		x = 0
		while x < len(self.board):
			y = 0
			while y < len(self.board):
				new_position_not_threatened = True
				for queen in self.board.all_pieces():
					if queen.is_threatening(x, y):
						new_position_not_threatened = False
						break
				if new_position_not_threatened:
					new_queen = chess.Queen(x, y)
					queen_stack.append(new_queen)
					self.board.add_piece(new_queen)
					if len(queen_stack) == self.target_number:				#  can only ever reach solved state on addition
						return self.board
				if x == len(self.board) - 1 and y == len(self.board) - 1:	#  pop the most-recently used queen
					mru_queen = queen_stack.pop()
					self.board.remove_piece(mru_queen)
					x = mru_queen.x
					y = mru_queen.y											#  set x and y to be that queen's coordinates
				y += 1
			x += 1

if __name__ == "__main__":
	BRU = BasicRecursiveSolver(8, 8)
	board = BRU.solve()
	print(board)