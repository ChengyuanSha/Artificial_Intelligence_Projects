
#input include all the grids in it
input = []
inputLine = []
inputGrid = []
grid = []

with open('pathfinding_a.txt', 'r') as f:
    for line in f:
        for x in line:
            if x != '\n':
                 inputLine.append(x)
        inputGrid.append(inputLine)
        inputLine = []
    for a in inputGrid:
        if a == [] and grid != []:
            input.append(grid)
            grid = []
        else:
            grid.append(a)
    if grid != []:
        input.append(grid)
        grid = []
