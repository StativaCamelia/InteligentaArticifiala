import matplotlib.pyplot as plt
import numpy as np

def read_file(path):
    maze = []
    with open(path) as f:
        for line in f.readlines():
            matrix_line = [int(x) for x in line.split(',')]
            maze.append(matrix_line)
    return maze


def initialize_start_state(n, m, maze, start, end):
    init_state = [[0 for i in range(n)] for j in range(m)]
    for i in range(n):
        for j in range(m):
            if i == start[0] and j == start[1]:
                init_state[i][j] = 's'
            elif i == end[0] and j == end[1]:
                init_state[i][j] = 'f'
            else:
                init_state[i][j] = int(maze[i][j])
    return init_state


def verify_coordinates(x, y):
    return False if x > n or x < 0 or y > m or y < 0  else True


def get_coordinates():
    coordinates = [-1, -1]
    while not len(coordinates) == 2 or not verify_coordinates(coordinates[0], coordinates[1]) or maze[coordinates[0]][coordinates[1]] == 1:
        coordinates = [int(x) for x in input().strip().split() if x.isnumeric()]
        if len(coordinates) != 2:
            print("Trebuie sa introduceti exact doua coordonate")
        elif not verify_coordinates(coordinates[0], coordinates[1]):
            print("Coordonatele sunt inafara labirintului, incercati iar")
        elif maze[coordinates[0]][coordinates[1]] == 1:
            print("Este o bariera, mai incerca")
    return coordinates


def is_final_state(state, position):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[position[0]][position[1]] == 'f':
                return True
    return False


def is_valid_transition(state, position):
    n = len(state)
    m = len(state[0])
    return False if state[position[0]][position[1]] == 1 or position[0] > n or position[0] < 0 or position[1] > m or position[1] < 0 else True


def new_transition(state, position):
    state[position[0]][position[1]] = 'r'
    return state


def backtracking_solve_maze(state, position):
    if state[position[0]][position[1]] == 'r' or not is_valid_transition(state, position):
        return False
    if is_final_state(state, position):
        state[position[0]][position[1]] = 'r'
        path.append(position)
        return path
    if is_valid_transition(state, position):
        state = new_transition(state, position)
        path.append(position)
        if backtracking_solve_maze(state, [position[0] + 1, position[1]]):
            return path
        if backtracking_solve_maze(state, [position[0], position[1] + 1]):
            return path
        if backtracking_solve_maze(state, [position[0] - 1, position[1]]):
            return path
        if backtracking_solve_maze(state, [position[0], position[1] - 1]):
            return path
        path.pop()
    return False


def get_adjacents(state, position):
    final = list()
    for i in get_neighbours(position):
        if is_valid_transition(state, i) and state[i[0]][i[1]] != 'r':
            final.append(i)
    return final


def get_neighbours(position):
    up = [position[0] + 1, position[1]]
    down = [position[0] - 1, position[1]]
    left = [position[0], position[1] - 1]
    right = [position[0], position[1] + 1]
    return [up, down, left, right]


def bfs_solve_maze(state, start):
    queue = [start]
    while len(queue) !=0:
        if queue[0] == start:
            path = [queue.pop(0)]
        else:
            path = queue.pop(0)
        position = path[-1]
        if is_final_state(state, position):
            return path
        elif state[position[0]][position[1]] != 'r':
            for i in get_adjacents(state, position):
                newPath = list(path)
                newPath.append(i)
                queue.append(newPath)
            new_transition(state, position)
    return False


def hillclimbing_solve_maze(state, start, end):
    current_position = start
    path = [current_position]
    while current_position != end:
        prev_state = current_position
        for neighbour in get_neighbours(current_position):
            if is_valid_transition(state, neighbour):
                if is_final_state(state, neighbour):
                    path.append(neighbour)
                    new_transition(state, neighbour)
                    return path
                succ = neighbour
                if function_to_minimise(succ, current_position, end):
                    current_position = succ
        if current_position == prev_state:
            return False
        new_transition(state, current_position)
        path.append(current_position)
    return path


def value(state, end):
    return abs(end[0] - state[0]) + abs(end[1] - state[1])


def function_to_minimise(s1, s2, end):
    val1 = value(s1, end)
    val2 = value(s2, end)
    if val1 == val2:
        return s1[0] > s2[0]
    return val1 < val2


def start_maze_vizualizer():
    plt.ion()
    plt.pcolormesh(maze, cmap ='Reds')
    plt.axes().set_aspect('equal') #set the x and y axes to the same scale
    plt.xticks([]) # remove the tick marks by setting to an empty list
    plt.yticks([]) # remove the tick marks by setting to an empty list
    plt.axes().invert_yaxis() #invert the y-axis so the first row of data is at the top


if __name__ == '__main__':
    maze = read_file("maze.txt")
    n = len(maze)
    m = len(maze[0])
    print("Introduceti coordonatele pozitiei de start x in intervalul:{},{} si y in intervalul:{},{}".format(0, n, 0, m))
    start = get_coordinates()
    print("Introduceti coordonatele pozitie de final x in intervalul:{},{} si y in intervalul:{},{}".format(0, n, 0, m))
    end = get_coordinates()
    print("Coordonate start:{}".format(start))
    print("Coordonate end:{}".format(end))
    initial_state = initialize_start_state(n, m, maze, start, end)
    print("Alegeti unul din urmatorii algoritmi:")
    print("1. Backtracking")
    print("2. BFS")
    print("3. Hillclimbing")
    answer = input()

    while answer != 'quit':
        initial_state = initialize_start_state(n, m, maze, start, end)
        if answer == '1':
            path = []
            print(backtracking_solve_maze(initial_state, start))
        elif answer == '2':
            print(bfs_solve_maze(initial_state, start))
        elif answer == '3':
            print(hillclimbing_solve_maze(initial_state, start, end))
        else:
            print("Please enter: 1,2 or 3")
        answer = input()
