import time
import random
import numpy as np


class MazeSolver:
    def __init__(self, application):
        self.maze_app = application
        self.path = []
        self.temperature = 0.9

    def initialize_start_state(self, n, m, maze, start, end):
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

    def is_final_state(self, state, position):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[position[0]][position[1]] == 'f':
                    return True
        return False

    def is_valid_transition(self, state, position):
        n = len(state)
        m = len(state[0])
        if position[0] > n or position[0] < 0 or position[1] > m or position[1] < 0:
            return False
        if state[position[0]][position[1]] == 1:
            return False
        return True

    def update_ui(self, position, color):
        self.maze_app.draw(position[0], position[1], color)
        time.sleep(0.1)
        self.maze_app.window.update()

    def new_transition(self, state, position, color):
        state[position[0]][position[1]] = 'r'
        self.update_ui(position, color)
        return state

    def get_neighbours(self,position):
        up = [position[0] + 1, position[1]]
        down = [position[0] - 1, position[1]]
        left = [position[0], position[1] - 1]
        right = [position[0], position[1] + 1]
        return [up, down, left, right]

    def backtracking_solve_maze(self, state, position):
        if not self.is_valid_transition(state, position) or state[position[0]][position[1]] == 'r':
            return False
        if self.is_final_state(state, position):
            state[position[0]][position[1]] = 'r'
            self.path.append(position)
            self.new_transition(state, position, "blue")
            return self.path
        if self.is_valid_transition(state, position):
            state = self.new_transition(state, position, "blue")
            self.path.append(position)
            for neigh in self.get_neighbours(position):
                if self.backtracking_solve_maze(state, neigh):
                    return self.path
            self.path.pop()
        return False

    def get_adjacents(self,state, position):
        final = list()
        for i in self.get_neighbours(position):
            if self.is_valid_transition(state, i) and state[i[0]][i[1]] != 'r':
                final.append(i)
        return final

    def bfs_solve_maze(self, state, start):
        queue = [start]
        while len(queue) != 0:
            if queue[0] == start:
                path = [queue.pop(0)]
            else:
                path = queue.pop(0)
            position = path[-1]
            if self.is_final_state(state, position):
                self.new_transition(state, position, "green")
                return path
            elif state[position[0]][position[1]] != 'r':
                for i in self.get_adjacents(state, position):
                    newPath = list(path)
                    newPath.append(i)
                    queue.append(newPath)
                self.new_transition(state, position, "green")
        return False

    def hillclimbing_solve_maze(self, state, start, end):
        random.seed(25)
        current_position = start
        self.new_transition(state, start, "orange")
        path = [current_position]
        while not self.is_final_state(state, current_position):
            prev_state = current_position
            neighbours = self.get_neighbours(current_position)
            random.shuffle(neighbours)
            for neighbour in neighbours:
                if self.is_valid_transition(state, neighbour):
                    if self.is_final_state(state, neighbour):
                        path.append(neighbour)
                        self.new_transition(state, neighbour, "orange")
                        return path
                    if self.is_better(neighbour, current_position, end):
                        current_position = neighbour
                        break
            if current_position == prev_state:
                return False
            self.new_transition(state, current_position, "orange")
            path.append(current_position)
        return path

    def value(self, state, end):
        return abs(end[0] - state[0]) + abs(end[1] - state[1])

    def is_better(self, s1, s2, end):
        val1 = self.value(s1, end)
        val2 = self.value(s2, end)
        if val1 == val2:
            return s1[0] > s2[0]
        return val1 < val2

    def update_temperature(self):
        self.temperature = self.temperature - 0.01

    def simulated_solve_maze(self, state, start, end):
        self.temperature = 0.9
        current_position = start
        self.new_transition(state, start, "pink")
        path = [current_position]
        while not self.is_final_state(state, current_position):
            prev_state = current_position
            for neighbour in self.get_neighbours(current_position):
                if self.is_valid_transition(state, neighbour):
                    if self.is_final_state(state, neighbour):
                        path.append(neighbour)
                        self.new_transition(state, neighbour, "pink")
                        return path
                    if self.is_better(neighbour, current_position, end):
                        current_position = neighbour
                        break
                    elif random.uniform(0, 1) < np.exp(-abs(self.value(current_position, end) - self.value(neighbour, end)) / self.temperature):
                        current_position = neighbour
                        self.update_temperature()
                        print(self.temperature)
                        break
            if current_position == prev_state:
                return False
            self.new_transition(state, current_position, "pink")
            path.append(current_position)
        return path