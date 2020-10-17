from tkinter import *
from tkinter.messagebox import *
from MazeSolver import MazeSolver


class MazeApplication:
    def __init__(self, maze):
        self.mazeSolver = MazeSolver(self)
        self.maze = maze
        self.n = len(maze)
        self.m = len(maze[1])
        self.start = [-1, -1]
        self.end = [-1, -1]
        self.cell_size = 15
        self.window = Tk()

    def start_interface(self):
        self.window.title("Maze Solver")
        canvas_width = (self.n + 1) * 15
        canvas_height = (self.m + 1) * 15
        self.ffs = Canvas(self.window, width=canvas_width, height=canvas_height, bg='grey')
        self.ffs.pack()
        self.get_coordinates_start_frame()
        self.create_maze()
        self.window.mainloop()


    def get_coordinates_start_frame(self):
        self.coordinates_label = Label(self.window,
                                  text="Introduceti coordonatele pozitiei de start x in intervalul:{},{} si y in intervalul:{},{}".format(
                                       0, self.n, 0, self.m), font=("Arial Bold", 15))
        self.coordinates_label.pack()
        self.init_entries()
        self.submit_button = Button(self.window, text="Submit", command=self.submit_start_coordinates)
        self.submit_button.pack()

    def init_entries(self):
        self.coord_x_label = Label(self.window, text="Coordonata X:")
        self.coord_x_label.pack()
        self.coord_x = Entry(width=10)
        self.coord_x.pack()
        self.coord_y_label = Label(self.window, text="Coordonata Y:")
        self.coord_y_label.pack()
        self.coord_y = Entry(width=10)
        self.coord_y.pack()

    def get_coordinates_end_frame(self):
        self.coordinates_label = Label(self.window,
                                  text="Introduceti coordonatele pozitiei de final x in intervalul:{},{} si y in intervalul:{},{}".format(
                                      0, self.n, 0, self.m), font=("Arial Bold", 15))
        self.coordinates_label.pack()
        self.init_entries()
        self.submit_button = Button(self.window, text="Submit", command=self.submit_end_coordinates)
        self.submit_button.pack()

    def submit_start_coordinates(self):
        self.start = [int(x) for x in [self.coord_x.get(), self.coord_y.get()] if x.isnumeric()]
        if self.get_coordinates_answers(self.start):
            self.destroy_old()
            self.draw(self.start[0], self.start[1], "Black")
            self.get_coordinates_end_frame()

    def submit_end_coordinates(self):
        self.end = [int(x) for x in [self.coord_x.get(), self.coord_y.get()] if x.isnumeric()]
        if self.get_coordinates_answers(self.end):
            self.destroy_old()
            self.draw(self.end[0], self.end[1], "Black")
            self.get_algorithm()

    def get_algorithm(self):
        self.coordinates_label = Label(self.window,
                                       text="       Alegeti algoritmul cu ajutorul caruia doriti sa rezolvati labirintul:          ", font=("Arial Bold", 15))
        self.coordinates_label.pack()
        self.default = StringVar(self.window)
        self.default.set("Backtracking")
        self.menu = OptionMenu(self.window, self.default, "Backtracking", "BFS", "HillClimbing", "Simulated")
        self.menu.pack()
        button_submit = Button(self.window, text="Submit", command=self.submit_alg)
        button_submit.pack()

    def submit_alg(self):
        alg = self.default.get()
        initial_state = self.mazeSolver.initialize_start_state(self.n, self.m, self.maze, self.start, self.end)
        if alg == 'Backtracking':
            result = self.mazeSolver.backtracking_solve_maze(initial_state, self.start)
        elif alg == 'BFS':
            result = self.mazeSolver.bfs_solve_maze(initial_state, self.start)
        elif alg == 'HillClimbing':
            result = self.mazeSolver.hillclimbing_solve_maze(initial_state, self.start, self.end)
        elif alg == 'Simulated':
            result = self.mazeSolver.simulated_solve_maze(initial_state, self.start, self.end)
        if not result:
            showinfo("Result", "Nu exista nici un drum de la coordonatele de start la cele de final")
        print(result)
    def destroy_old(self):
        self.coord_x.destroy()
        self.coord_y.destroy()
        self.coord_x_label.destroy()
        self.coord_y_label.destroy()
        self.submit_button.destroy()
        self.coordinates_label.destroy()

    def get_coordinates_answers(self, coordinates):
        if len(coordinates) != 2:
            showerror("Error", "Trebuie sa introduceti exact doua coordonate")
            return False
        elif not self.verify_coordinates(coordinates[0], coordinates[1]):
            showerror("Error", "Coordonatele sunt inafara labirintului, incercati iar")
            return False
        elif self.maze[coordinates[0]][coordinates[1]] == 1:
            showerror("Error", "Este o bariera, mai incerca")
            return False
        return True

    def verify_coordinates(self, x, y):
        return False if x > self.n or x < 0 or y > self.m or y < 0 else True

    def create_maze(self):
        for row in range(self.n):
            for col in range(self.m):
                if self.maze[row][col] == 1:
                    color = 'Red'
                elif self.maze[row][col] == 0:
                    color = 'White'
                self.draw(row, col, color)

    def draw(self, row, col, color):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.ffs.create_rectangle(x1, y1, x2, y2, fill=color)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end
