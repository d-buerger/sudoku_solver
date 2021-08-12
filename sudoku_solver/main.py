#imports
from random import shuffle
import copy

"""
Produces a solved 9x9 Sudoku puzzle with numbers 1-9. 
Utilizes a brute force algorithm (backtracking) to create it.
Removes numbers inside solved puzzle to render it unsolved for the user.
"""
class SudokuGenerator:


	def __init__(self):
		"""initialize method used at object creation"""

		# set instance variables for counter and path
		self.counter = 0  # number of solutions to puzzle counter
		self.path = []

		# generate an empty grid of 0's using list comprehension
		self.grid = [[0 for i in range(9)] for j in range(9)]

		# generate a puzzle
		self.create_puzzle()


	def create_puzzle(self):
		"""generates a solved puzzle then remove numbers"""

		# generates a solved puzzle
		self.create_solved_puzzle(self.grid)

		# print the puzzle
		print("Puzzle solved:")
		self.print_puzzle()

		# remove numbers in the solved puzzle to create an unsolved puzzle
		self.remove_numbers()

		# print the user a puzzle to solve
		print("\nPuzzle to solve:")
		self.print_puzzle()

		return

	def print_puzzle(self):
		"""prints the puzzle"""
		for row in self.grid:
			print(row)
		return


	def number_in_row(self, grid, row, number):
		"""returns True if number is in row"""
		if number in grid[row]:
			return True
		return False

	def number_in_col(self,grid,col,number):
		"""returns True if number is in column"""
		for i in range(9):
			if grid[i][col] == number:
				return True
		return False

	def number_in_box(self,grid,row,col,number):
		"""returns True if number is in 3x3 box"""
		sub_row = (row // 3) * 3
		sub_col = (col // 3)  * 3
		for i in range(sub_row, (sub_row + 3)):
			for j in range(sub_col, (sub_col + 3)):
				if grid[i][j] == number:
					return True
		return False

	def get_valid_empty_square(self,grid,row,col,number):
		"""return True if the number is not in row, col, or box"""
		if self.number_in_row(grid, row,number):
			return False
		elif self.number_in_col(grid,col,number):
			return False
		elif self.number_in_box(grid,row,col,number):
			return False
		return True

	def get_next_empty_square(self,grid):
		"""return the next empty square coordinates in the grid"""
		for i in range(9):
			for j in range(9):
				if grid[i][j] == 0:
					return (i,j)
		return

	def solve_temp_puzzle(self, grid):
		"""solves a temp puzzle with backtracking"""
		# loop for 81 positions
		for i in range(0, 81):
			row = i // 9
			col = i % 9
			# get next empty cell
			if grid[row][col] == 0:
				for number in range(1, 10):
					# check that the number hasn't been used in the row/col/box
					if self.get_valid_empty_square(grid, row, col, number):
						grid[row][col] = number
						if not self.get_next_empty_square(grid):
							self.counter += 1  # multiple solutions to temp puzzle, increase solution counter
							break
						else:
							if self.solve_temp_puzzle(grid):
								return True
				break
		grid[row][col] = 0
		return False

	def create_solved_puzzle(self, grid):
		"""creates a solved puzzle with backtracking"""
		number_list = [1,2,3,4,5,6,7,8,9]

		# loop for 81 positions
		for i in range(0,81):
			row=i//9  # integer division with //
			col=i%9  # modulus remainder with %

			# get next empty cell
			if grid[row][col]==0:

				#shuffle list of numbers so each puzzle is unique
				shuffle(number_list)

				# loop all numbers
				for number in number_list:
					if self.get_valid_empty_square(grid, row, col, number):  # check for empty location
						self.path.append((number, row, col))
						grid[row][col]=number
						if not self.get_next_empty_square(grid):
							return True
						else:
							# repeat until the grid is full
							if self.create_solved_puzzle(grid):
								return True
				break
		grid[row][col]=0
		return False

	def get_all_non_empty_squares(self,grid):
		"""returns a shuffled list of the puzzle"""
		non_empty_squares = []
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != 0:
					non_empty_squares.append((i,j))
		shuffle(non_empty_squares)
		return non_empty_squares

	def remove_numbers(self):
		"""remove numbers from the grid to create the puzzle"""

		non_empty_squares = self.get_all_non_empty_squares(self.grid)
		non_empty_squares_count = len(non_empty_squares)

		rounds = 3

		# loop for 3 rounds and have at least 20 hints
		while rounds > 0 and non_empty_squares_count >= 20:

			row,col = non_empty_squares.pop()
			non_empty_squares_count -= 1

			# keep square in memory, might need to return it if there are multiple solutions
			removed_square = self.grid[row][col]

			# set that grind space to 0
			self.grid[row][col]=0

			# create copy of instance to a new object
			grid_copy = copy.deepcopy(self.grid)

			# initialize solutions counter to zero
			self.counter=0

			# solve this new puzzle with the temp copy
			self.solve_temp_puzzle(grid_copy)

			# if there is more than one solution then put the last removed square back into the grid
			if self.counter!=1:
				self.grid[row][col]=removed_square
				non_empty_squares_count += 1
				rounds -=1

		return