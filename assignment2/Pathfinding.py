import heapq as pq
import os

class pathfinding:
    def __init__(self, file_a_path="pathfinding_a.txt", file_b_path="pathfinding_b.txt"):
        self.a_grids = self.read_file(file_a_path)
        self.b_grids= self.read_file(file_b_path)
        self.movement_without_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.movement_with_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.file_a_path_out = "pathfinding_a_out.txt"
        self.file_b_path_out = "pathfinding_b_out.txt"

    # read grids from file
    def read_file(self, file_path):
        input = []
        inputLine = []
        inputGrid = []
        grid = []
        with open(file_path, 'r') as f:
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
        return input

    # write grids to file
    def write_file(self, grid, path, file_path, greeOrA):
        input = []
        result_Grid = grid
        rows, cols = len(result_Grid), len(result_Grid[0])
        for row in range(rows):
            for col in range(cols):
                if (row, col) in path and result_Grid[row][col] == "_":
                    result_Grid[row][col] = "P"
        with open(file_path, 'a+') as f:
            f.write(greeOrA + "\n")
            for line in result_Grid:
                for char in line:
                    f.write(char)
                f.write("\n")

    # check grids is limit
    def checkGrid(self, grid):
        # check the row is limit
        if(len(grid) < 8 or len(grid) > 1024):
            print("For the grid: ")
            print(grid)
            print("Take a m x n (where 8<=m<=1024 and 8<=n<=1024) input grid!\n")
            return False
        else:
            # check the col is limit
            rowLength = len(grid[0])
            if (rowLength < 8 or rowLength > 1024):
                print("For the grid: ")
                print(grid)
                print("Take a m x n (where 8<=m<=1024 and 8<=n<=1024) input grid!\n")
                return False
            else:
                for line in grid:
                    if (len(line) != rowLength):
                        print("For the grid: ")
                        print(grid)
                        print("Each columns of one grid should be smae size!\n")
                        return False
            return True


    def start_goal_position(self, grid): # Find start point and goal point
        start_position, goal_position = None, None
        rows, cols = len(grid), len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "G":
                    goal_position = (row, col)
                elif grid[row][col] == "S":
                    start_position = (row, col)
        print("start_position: " + str(start_position) + " goal_position: ", str(goal_position) + " (0 based indexing)")
        return start_position, goal_position

    def heuristic(self, a, b, t): # Find corresponding heuristic algorithm to use
        return self.chebyshev(a, b) if t else self.manhattan(a, b)

    def manhattan(self, x, y): # Manhattan distance on a grid
        return sum([(a - b)**2 for a, b in zip(x, y)])

    def chebyshev(self, x, y): # Chebyshev distance on a grid
        return max([abs(a - b) for a, b in zip(x, y)])

    # following notes posted on the assignment
    def Greedy(self, grid, start, goal, movement, diag):  #  Greedy algorithm based on pseudo code given
        # create Priority queue
        frontier = []
        priority = {start: self.heuristic(start, goal, diag)}
        pq.heappush(frontier, (priority[start], start))
        came_from = {}
        visited = set()
        while frontier:
            current = pq.heappop(frontier)[1]
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path = list(reversed(path))
                return path
            visited.add(current)
            for i, j in movement:
                neighbor = current[0] + i, current[1] + j  # Check for neighbors
                # checking legal neighbors
                if not (self.is_neighbor_legal(neighbor, grid)) or \
                        (neighbor in visited):
                    # illegal neighbor, start another round
                     continue
                # when the neighbor is available
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    priority[neighbor] = self.heuristic(neighbor, goal, diag)
                    pq.heappush(frontier, (priority[neighbor], neighbor))
        return "Not found"

    # following notes posted on the assignment
    def A_star(self, grid, start, goal, movement, diag): # A* algorithm based on pseudo code given
        # create Priority queue
        frontier = []
        priority = {start: self.heuristic(start, goal, diag)}
        pq.heappush(frontier, (priority[start], start))
        cost_so_far = {start: 0}
        came_from = {}
        visited = set()
        while frontier:
            current = pq.heappop(frontier)[1]
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path = list(reversed(path))
                return path
            visited.add(current)
            for i, j in movement:
                neighbor = current[0] + i, current[1] + j # Check for neighbors
                new_cost = cost_so_far[current] + 1
                # checking legal neighbors
                if not(self.is_neighbor_legal(neighbor, grid)) or \
                        (neighbor in visited and new_cost >= cost_so_far.get(neighbor, 0)):
                    # illegal neighbor, start another round
                    continue
                # when the neighbor is available
                if new_cost < cost_so_far.get(neighbor, 0) or neighbor not in came_from:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    priority[neighbor] = new_cost + self.heuristic(neighbor, goal, diag)
                    pq.heappush(frontier, (priority[neighbor], neighbor))
        return "Not found"

    def is_neighbor_legal(self, neighbor, grid):
        if (0 <= neighbor[0]) and (neighbor[0] < len(grid)):
            if (0 <= neighbor[1]) and (neighbor[1] < len(grid[0])):
                if grid[neighbor[0]][neighbor[1]] == "X":
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def main(self, is_diagonal): # main two algorithms to get results
        if not(is_diagonal):
            print("Part A, does not allow diagonal ")
            for grid in self.a_grids:
                if(self.checkGrid(grid)):
                    start_position, goal_position = self.start_goal_position(grid)
                    Greedy_path = self.Greedy(grid, start_position, goal_position, self.movement_without_diagonal, is_diagonal)
                    A_star_path = self.A_star(grid, start_position, goal_position, self.movement_without_diagonal, is_diagonal)

                    print("Greedy path:", Greedy_path)
                    if Greedy_path == "Not found":
                        print("No solution found by Greedy algorithm\n")
                    else:
                        print("Solution found by Greedy algorithm\n")
                        # write to file
                        self.write_file(grid, Greedy_path, self.file_a_path_out, "Greedy")

                    print("A star path:", A_star_path)
                    if A_star_path == "Not found":
                        print("No solution found by A* algorithm\n")
                    else:
                        print("Solution found by A* algorithm\n")
                        # write to file
                        self.write_file(grid, A_star_path, self.file_a_path_out, "A*")
                        with open(self.file_a_path_out, 'a+') as f:
                            f.write("\n")
        else:
            print("Part B, allow diagonal ")
            for grid in self.b_grids:
                if (self.checkGrid(grid)):
                    start_position, goal_position = self.start_goal_position(grid)
                    Greedy_path = self.A_star(grid, start_position, goal_position, self.movement_with_diagonal,is_diagonal)
                    A_star_path = self.A_star(grid, start_position, goal_position, self.movement_with_diagonal,is_diagonal)

                    print("Greedy path:", Greedy_path)
                    if Greedy_path == "Not found":
                        print("No solution found by Greedy algorithm\n")
                    else:
                        print("Solution found by Greedy algorithm\n")
                        # write to file
                        self.write_file(grid, Greedy_path, self.file_b_path_out, "Greedy")

                    print("A star path:", A_star_path)
                    if A_star_path == "Not found":
                        print("No solution found by A* algorithm\n")
                    else:
                        print("Solution found by A* algorithm\n")
                        # write to file
                        self.write_file(grid, A_star_path, self.file_b_path_out, "A*")
                        with open(self.file_b_path_out, 'a+') as f:
                            f.write("\n")


if __name__ == "__main__":
    if os.path.isfile("pathfinding_a_out.txt"):
        os.remove("pathfinding_a_out.txt")
    if os.path.isfile("pathfinding_b_out.txt"):
        os.remove("pathfinding_b_out.txt")
    pf = pathfinding()
    pf.main(False) # Without diagonal
    pf.main(True) # With diagonal



