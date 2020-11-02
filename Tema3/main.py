from tkinter import *

from CheckersGame import CheckersGame

if __name__ == '__main__':
	root = Tk()
	root.title("Checkers Tk")
	root.resizable(0, 0)
	game = CheckersGame(root)
	root.mainloop()
