import math
import random
from copy import deepcopy
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
import time


class CheckersGame(object):
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

	def get_best_move(self, new_state, opposer_state):
		return sum([piece_c[0] for piece_c in new_state]) - sum([piece_h[0] for piece_h in opposer_state])

	def check_remaining_moves(self, who):
		pieces_locations = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
								 self.board_with_pieces[i][j] == who]
		moves = []
		for index, piece in enumerate(pieces_locations):
			moves.append(self.get_valid_moves(piece[0], piece[1]))
		return False if len(moves) == 0 else True

	def cost_state(self, state):
		calculator_pieces  = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
								 state[i][j] == 'c']
		human_pieces  = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
								 state[i][j] == 'h']
		return sum([piece_c[0] for piece_c in calculator_pieces]) - sum([piece_h[0] for piece_h in human_pieces])


	def minimax_search(self, curDepth, state, maxTurn, targetDepth, maxi, mini):
		calculator_pieces = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
							 state[i][j] == 'c']
		human_pieces = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
						state[i][j] == 'h']
		if curDepth == targetDepth or self.final_state_c() or not self.check_remaining_moves('c'):
			return self.cost_state(state)
		if maxTurn:
			for index, piece in enumerate(calculator_pieces):
				moves = self.get_valid_moves(piece[0], piece[1])
				if piece[0] != 3:
					for move in moves:
						new_state = deepcopy(state)
						new_state[move[0]][move[1]] = 'c'
						new_state[piece[0]][piece[1]] = (piece[0] + piece[1]) % 2
						result = self.minimax_search(curDepth + 1, new_state, False, targetDepth, maxi, mini)
						if result > maxi:
							maxi = result
							state_maxi = state
			return maxi
		else:
			for index, piece in enumerate(human_pieces):
				moves = self.get_valid_moves(piece[0], piece[1])
				for move in moves:
					new_state = deepcopy(state)
					new_state[move[0]][move[1]] = 'h'
					new_state[piece[0]][piece[1]] = (piece[0] + piece[1]) % 2
					result = self.minimax_search(curDepth + 1, new_state, True, targetDepth, maxi, mini)
					if result < mini:
						mini = result
						state_mini = state
					print(result)
			return mini

	def ai_one_level(self):
		maxim, move_maxim = -math.inf, (-1, -1)
		pieces_locations_calc = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if self.board_with_pieces[i][j] == 'c']
		random.shuffle(pieces_locations_calc)
		pieces_locations_human = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if self.board_with_pieces[i][j] == 'h']
		if self.check_remaining_moves('c'):
			for index, piece in enumerate(pieces_locations_calc):
				moves = self.get_valid_moves(piece[0], piece[1])
				new_state = pieces_locations_calc.copy()
				if piece[0] != 3:
					for move in moves:
						new_state[index] = move
						move_value = self.get_best_move(new_state, pieces_locations_human)
						if move_value > maxim:
							maxim = move_value
							move_maxim = move
							print(maxim, move_maxim)
							old_position = pieces_locations_calc[index]
			self.update_matrix(move_maxim[0], move_maxim[1], old_position, 'c')
			self.update_interface(move_maxim[0], move_maxim[1], old_position, 'c')
			if self.final_state_c():
				showerror("Game Over!", "You lost the game!")
			else:
				self.turn = 'h'
		else:
			if self.check_winner() == 'c':
				showerror("Game Over!", "You lost the game!")
			elif self.check_winner() == 'h':
				showinfo("Congratulation!", "You win!")
			else:
				showinfo("Tie", "It's a tie")

	def check_winner(self):
		pieces_locations_calc = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
								 self.board_with_pieces[i][j] == 'c']
		pieces_locations_human = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if
								 self.board_with_pieces[i][j] == 'c']
		c = pieces_locations_calc.count(lambda x: x[0] == self.dimension - 1)
		h = pieces_locations_human.count(lambda x: x[0] == 0)
		if c > h:
			return "c"
		elif h >c:
			return "h"
		else:
			return "r"

	def mouse_click(self, event):
		row, col = self.mouse_calc(event.x, event.y)
		if self.turn == "h":
			if self.check_remaining_moves("h"):
				if not self.selected_piece:
					if self.board_with_pieces[row][col] == "h":
						self.selected_piece = (row, col)
				else:
					if self.board_with_pieces[row][col] == "h":
						self.selected_piece = (row, col)
					elif self.legal_move(row, col):
						self.update_matrix(row, col, self.selected_piece, 'h')
						self.update_interface(row, col, self.selected_piece, 'h')
						self.turn = "c"
						self.selected_piece = []
						if self.final_state_h():
							showinfo("Congratulation!", "You win!")
						else:
							self.ai_one_level()
			else:
				if self.check_winner() == 'c':
					showerror("Game Over!", "You lost the game!")
				elif self.check_winner() == 'h':
					showinfo("Congratulation!", "You win!")
				else:
					showinfo("Tie", "It's a tie")
		elif not self.final_state_h():
			showwarning("Warning!", "Please wait, it's not your turn!")

	def final_state_c(self):
		pieces_locations_calc = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if self.board_with_pieces[i][j] == 'c']
		for piece in pieces_locations_calc:
			if piece[0] != self.dimension - 1:
				return False
		return True

	def final_state_h(self):
		pieces_locations_human = [[i, j] for i in range(self.dimension) for j in range(self.dimension) if self.board_with_pieces[i][j] == 'h']
		for piece in pieces_locations_human:
			if piece[0] != 0:
				return False
		return True

	def update_interface(self, row, col, old_position, who_moved):
		old_row, old_col = old_position[0], old_position[1]
		if who_moved == 'h':
			self.draw_oval(row, col, self.human_color)
		else:
			self.draw_oval(row, col, self.computer_color)
		self.draw_rectangle(old_row, old_col, self.get_rectangle_color(old_row, old_col))

	def update_matrix(self, row, col, old_position, who_moved):
		old_row, old_col = old_position[0], old_position[1]
		self.board_with_pieces[row][col] = who_moved
		self.board_with_pieces[old_row][old_col] = (old_row + old_col) % 2
		print(self.board_with_pieces)

	def check_move(self, row, col):
		return True if (0 <= col < self.dimension) and (0 <= row < self.dimension) and (
				self.board_with_pieces[row][col] != 'h' and self.board_with_pieces[row][col] != 'c') else False

	def get_valid_moves(self, row, col):
		moves = []
		if self.turn == "h":
			direction_up, direction_down = -1, 1
		else:
			direction_up, direction_down = 1, -1
		directions = [(1 * direction_up, -1), (1 * direction_up, 0), (1 * direction_up, 1), (0, 1), (1 * direction_down, 1), (1 * direction_down, 0), (1 * direction_down, -1), (0, -1)]
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
		self.root.geometry("{}x{}".format(canvas_width, canvas_height))
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


	def remove(self):
		self.start_label.destroy()
		self.menu.destroy()
		self.button_submit.destroy()

	def submit_start(self):
		self.remove()
		self.init_board_with_pieces()
		self.init_board_GUI(self.root)
		self.draw_initial_pieces()
		if self.default.get() == "Human":
			self.turn = "h"
		else:
			self.turn = "c"
			self.minimax_search(0, self.board_with_pieces, True, 2, -math.inf, math.inf)

	def start_menu(self):
		self.root.geometry("400x200")
		self.start_label = Label(self.root,
									   text="Who start?",
									   font=("Arial Bold", 15))
		self.start_label.pack()
		self.default = StringVar(self.root)
		self.default.set("Human")
		self.menu = OptionMenu(self.root, self.default, "Human", "Computer")
		self.menu.pack()
		self.button_submit = Button(self.root, text="Start", command=self.submit_start)
		self.button_submit.pack()

	def __init__(self, root):
		self.win = False
		self.root = root
		self.turn = "h"
		self.selected_piece = []
		self.dimension = 4
		self.cell_size = 150
		self.computer_color = "green"
		self.human_color = "red"
		self.board = [[0 if (i + j) % 2 == 0 else 1 for i in range(self.dimension)] for j in range(self.dimension)]
		self.board_with_pieces = [[]]
		self.start_menu()
