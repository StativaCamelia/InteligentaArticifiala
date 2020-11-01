from tkinter import *

from ChekersGame import ChekersGame

if __name__ == '__main__':
	root = Tk()
	root.title("Checkers Tk")
	root.resizable(0, 0)
	game = ChekersGame(root)
	root.mainloop()