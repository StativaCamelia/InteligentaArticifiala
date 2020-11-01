import math
from tkinter import *


class ChekersGame(object):
	def init_board_with_pieces(self):
		self.board_with_pieces = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
		for row in range(self.dimension):
			for column in range(self.dimension):
				if row == 0:
					self.board_with_pieces[row][column] = 'c'
				elif row == self.dimension - 1:
					self.board_with_pieces[row][column] = 'h'
				else:
					self.board_with_pieces[row][column] = self.board[row][column]

	def mouse_calc(self, x, y):
		return y // self.cell_size, x // self.cell_size

	@staticmethod
	def get_rectangle_color(row, col):
		return "black" if (row + col) % 2 else "white"


	def get_best_move(self, new_state, opposant_state):
		return sum([piece_c[1] for piece_c in new_state ])- sum([piece_h[1] for piece_h in opposant_state])

	def ai_one_level(self):
		maxim, move_maxim = -math.inf, (-1, -1)
		pieces_locations_calc = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if self.board_with_pieces[i][j] == 'c']
		pieces_locations_human = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
								 self.board_with_pieces[i][j] == 'h']
		for index, piece in enumerate(pieces_locations_calc):
			moves = self.get_valid_moves(piece[0], piece[1])
			new_state = pieces_locations_calc.copy()
			for move in moves:
				new_state[index] = move
				move_value = self.get_best_move(new_state, pieces_locations_human)
				if  move_value > maxim:
					maxim = move_value
					move_maxim = move
					old_position = pieces_locations_calc[index]
		self.update_matrix(move_maxim[0], move_maxim[1], old_position, 'c')
		self.update_interface(move_maxim[0], move_maxim[1], old_position, 'c')
		self.turn = 'h'

	def mouse_click(self, event):
		row, col = self.mouse_calc(event.x, event.y)
		if self.turn == "h":
			if not self.selected_piece:
				if self.board_with_pieces[row][col] == "h":
					self.selected_piece = (row, col)
			else:
				if self.legal_move(row, col):
					self.update_matrix(row, col, self.selected_piece, 'h')
					self.update_interface(row, col, self.selected_piece, 'h')
					self.turn = "c"
					self.selected_piece = []
					self.ai_one_level()

	def final_state(self):
		computer_pieces = sum(
			[1 for i in range(self.dimension) if self.board_with_pieces[self.dimension - 1][i] == 'c'])
		human_pieces = sum([1 for i in range(self.dimension) if self.board_with_pieces[self.dimension - 1][i] == 'h'])
		if computer_pieces == self.dimension:
			return True, 'c'
		elif human_pieces == self.dimension:
			return True, 'h'
		else:
			return False, None

	def update_interface(self, row, col, old_position, who_moved):
		old_row, old_col = old_position[0], old_position[1]
		if who_moved == 'h':
			self.draw_oval(row, col, self.human_color)
		else:
			self.draw_oval(row, col, self.computer_color)
		self.draw_rectangle(old_row, old_col,
							self.get_rectangle_color(old_row, old_col))

	def update_matrix(self, row, col, old_position, who_moved):
		old_row, old_col = old_position[0], old_position[1]
		self.board_with_pieces[row][col] = who_moved
		self.board_with_pieces[old_row][old_col] = (old_row + old_col) % 2

	def check_move(self, row, col):
		return True if (0 <= col < self.dimension) and (0 <= row < self.dimension) and (
				self.board_with_pieces[row][col] != 'h' and self.board_with_pieces[row][col] != 'c') else False

	def get_valid_moves(self, row, col):
		moves = []
		if self.turn == "h":
			direction_up, direction_down = -1, 1
		else:
			direction_up, direction_down = 1, -1
		directions = [(1 * direction_up, -1), (1 * direction_up, 0), (1 * direction_up, 1), (0, 1),
					  (1 * direction_down, 1), (1 * direction_down, 0), (1 * direction_down, -1), (0, -1)]
		for d in directions:
			if self.check_move(row + d[0], col + d[1]):
				moves.append([row + d[0], col + d[1]])
		return moves


	def legal_move(self, row, col):
		if [row, col] in self.get_valid_moves(self.selected_piece[0], self.selected_piece[1]):
			return True
		return False

	def init_board_GUI(self, root):
		canvas_width = self.dimension * self.cell_size
		canvas_height = self.dimension * self.cell_size
		self.canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='grey')
		self.canvas.pack()
		self.canvas.bind("<Button-1>", self.mouse_click)
		self.draw_table()

	def draw_table(self):
		global color
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
			self.canvas.create_oval(x1, y1, x2, y2, fill=color, activeoutline="yellow")
		else:
			self.canvas.create_oval(x1, y1, x2, y2, fill=color)

	def __init__(self, root):
		self.win = False
		self.turn = "h"
		self.selected_piece = []
		self.dimension = 4
		self.cell_size = 150
		self.computer_color = "green"
		self.human_color = "red"
		self.board = [[0 if (i + j) % 2 == 0 else 1 for i in range(self.dimension)] for j in range(self.dimension)]
		self.board_with_pieces = [[]]
		self.init_board_with_pieces()
		self.init_board_GUI(root)
		self.draw_initial_pieces()
