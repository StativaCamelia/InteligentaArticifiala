from MazeApplication import MazeApplication


def read_file(path):
    maze = []
    with open(path) as f:
        for line in f.readlines():
            matrix_line = [int(x) for x in line.split(',')]
            maze.append(matrix_line)
    return maze


if __name__ == '__main__':
    maze = read_file("maze.txt")
    maze_app = MazeApplication(maze)
    maze_app.start_interface()


