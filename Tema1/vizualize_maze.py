import matplotlib.pyplot as plt

maze = []
with open("maze.txt", 'r') as file:
    for line in file:
        line = line.rstrip()
        row = []
        for c in line:
            if c == '1':
                row.append(1) # spaces are 1s
            elif c == '0':
                row.append(0) # walls are 0s
        maze.append(row)

plt.pcolormesh(maze, cmap ='Greens')
plt.axes().set_aspect('equal') #set the x and y axes to the same scale
plt.xticks([]) # remove the tick marks by setting to an empty list
plt.yticks([]) # remove the tick marks by setting to an empty list
plt.axes().invert_yaxis() #invert the y-axis so the first row of data is at the top
plt.show()