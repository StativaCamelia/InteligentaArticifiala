from tkinter import *

class MazeApplication():
    def __init__(self, maze):
            self.maze = maze
            self.n = len(maze)
            self.m = len(maze[1])
            self.start = [-1, -1]
            self.end = [-1, -1]
            self.window = Tk()


    def start_interface(self):
        self.window.title("Maze Solver")
        canvas_width = self.n * 15
        canvas_height = self.m * 15
        self.get_coordinates_interface()
        self.ffs = Canvas(self.window, width=canvas_width, height=canvas_height, bg='grey')
        self.ffs.pack()
        self.create_maze(ffs)
        window.mainloop()


    def get_coordinates_interface(self):
        coordinates_label = Label(self.window,
                                  text="Introduceti coordonatele pozitiei de start x in intervalul:{},{} si y in intervalul:{},{}".format(
                                      0, n, 0, m), font=("Arial Bold", 15))
        coordinates_label.pack()
        start_x = Entry(window, width=10)
        start_x.insert(0, 'Start X')
        start_y = Entry(window, width=10)
        start_y.insert(0, 'Start Y')
        start_x.pack()
        start_y.pack()

        def get_coordinates():
            coordinates = [int(start_x.get()), int(start_y.get())]
            while not len(coordinates) == 2 or not verify_coordinates(coordinates[0], coordinates[1]) or \
                    maze[coordinates[0]][coordinates[1]] == 1:
                coordinates = [int(x.get()) for x in coordinates if x.get().isnumeric()]
                if len(coordinates) != 2:
                    print("Trebuie sa introduceti exact doua coordonate")
                elif not verify_coordinates(coordinates[0], coordinates[1]):
                    print("Coordonatele sunt inafara labirintului, incercati iar")
                elif maze[coordinates[0]][coordinates[1]] == 1:
                    print("Este o bariera, mai incerca")
            return coordinates

        btn = Button(window, text="Submit!", command=get_coordinates)
        btn.pack()
        print(start_x.get)