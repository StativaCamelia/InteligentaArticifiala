from tkinter import *

class ChekersGame(object):
	def init_board_with_pieces(self):
		self.board_with_pieces = [[0 for i in range(self.dimension)]for j in range(self.dimension)]
		for row in range(self.dimension):
			for column in range(self.dimension):
				if row == 0:
					self.board_with_pieces[row][column] = 'c'
				elif row == self.dimension - 1:
					self.board_with_pieces[row][column] = 'h'
				else:
					self.board_with_pieces[row][column] = self.board[row][column]
		print()

	def mouseCalc(self, x, y):
		return y // self.cell_size, x // self.cell_size

	def get_rectangle_color(self, row, col):
		return "black" if (row + col) % 2 else "white"

	def mouseClick(self, event):
		row, col = self.mouseCalc(event.x, event.y)
		if self.turn == "h":
			if self.selected_piece == []:
				if self.board_with_pieces[row][col] == "h":
					self.selected_piece = (row, col)
			else:
				if self.legal_move(row, col):
					self.update_matrix(row, col)
					self.update_interface(row, col)
					self.turn = "c"
					self.selected_piece = []

	def update_interface(self, row, col):
		old_row, old_col = self.selected_piece[0], self.selected_piece[1]
		self.draw_oval(row, col, self.human_color)
		self.draw_rectangle(old_row, old_col,
							self.get_rectangle_color(old_row, old_col))

	def update_matrix(self, row, col):
		old_row, old_col = self.selected_piece[0], self.selected_piece[1]
		self.board_with_pieces[row][col] = 'h'
		self.board_with_pieces[old_row][old_col] = (old_row + old_col) % 2

	def check_move(self, row, col):
		return True if (col >= 0 and col < self.dimension) and (row >= 0 and row < self.dimension) and (self.board_with_pieces[row][col] != 'h' and self.board_with_pieces[row][col] != 'c') else False

	def get_valid_moves(self):
		moves = []
		if self.turn == "h":
			direction_up, direction_down = -1, 1
		else:
			direction_up, direction_down = 1, -1
		directions = [ (1*direction_up, -1), (1*direction_up, 0), (1*direction_up, 1), (0, 1), (1 * direction_down, 1), (1*direction_down, 0), (1*direction_down, -1), (0, -1)]
		for d in directions:
			if self.check_move(self.selected_piece[0] + d[0], self.selected_piece[1] + d[1]):
				moves.append([self.selected_piece[0] + d[0], self.selected_piece[1] + d[1]])
		return moves

	def legal_move(self, row, col):
		if [row, col] in self.get_valid_moves():
			return True
		return False


	def init_board_GUI(self, root):
		canvas_width = (self.dimension) * self.cell_size
		canvas_height = (self.dimension) * self.cell_size
		self.canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='grey')
		self.canvas.pack()
		self.canvas.bind("<Button-1>", self.mouseClick)
		self.draw_table()

	def draw_table(self):
		for row in range(self.dimension):
			for col in range(self.dimension):
				if self.board[row][col] == 1:
					color = 'Black'
				elif self.board[row][col] == 0:
					color = 'White'
				self.draw_rectangle(row, col, color)

	def draw_rectangle(self, row, col, color):
		x1 = col * self.cell_size
		y1 = row * self.cell_size
		x2 = x1 + self.cell_size
		y2 = y1 + self.cell_size
		self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)


	def draw_initial_pieces(self):
		for row in range(self.dimension):
			for col in range(self.dimension):
				if self.board_with_pieces[row][col] == 'c':
					color = self.computer_color
					self.draw_oval(row, col, color)
				elif self.board_with_pieces[row][col] == 'h':
					color = self.human_color
					self.draw_oval(row, col, color)


	def draw_oval(self, row, col, color):
		x1 = col * self.cell_size
		y1 = row * self.cell_size
		x2 = x1 + self.cell_size
		y2 = y1 + self.cell_size
		if color == self.human_color:
			self.canvas.create_oval(x1, y1, x2, y2, fill=color, activeoutline = "yellow")
		else:
			self.canvas.create_oval(x1, y1, x2, y2, fill=color)

	def __init__(self, root):
		self.turn = "h"
		self.selected_piece = []
		self.dimension = 4
		self.cell_size = 150
		self.computer_color = "green"
		self.human_color = "red"
		self.board = [[0 if (i+j)%2==0 else 1 for i in range(self.dimension)] for j in range(self.dimension)]
		self.board_with_pieces = [[]]
		self.init_board_with_pieces()
		self.init_board_GUI(root)
		self.draw_initial_pieces()
