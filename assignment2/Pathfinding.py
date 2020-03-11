import heapq as pq

class pathfinding:
    def __init__(self, file_a_path="pathfinding_a.txt", file_b_path="pathfinding_b.txt"):
        self.a_grids = self.read_file(file_a_path)
        self.b_grids= self.read_file(file_b_path)
        self.movement_without_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.movement_with_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

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
                start_position, goal_position = self.start_goal_position(grid)
                A_star_path = self.A_star(grid, start_position, goal_position, self.movement_without_diagonal, is_diagonal)
                print("A star path:", A_star_path)
                if A_star_path == "Not found":
                    print("No solution found by A* algorithm\n")
                else:
                    print("Solution found by A* algorithm\n")
                    # write to file
        else:
            print("Part B, allow diagonal ")
            for grid in self.b_grids:
                start_position, goal_position = self.start_goal_position(grid)
                A_star_path = self.A_star(grid, start_position, goal_position, self.movement_with_diagonal,is_diagonal)
                print("A star path:", A_star_path)
                if A_star_path == "Not found":
                    print("No solution found by A* algorithm\n")
                else:
                    print("Solution found by A* algorithm\n")
                    # write to file


if __name__ == "__main__":
    pf = pathfinding()
    pf.main(False) # Without diagonal
    pf.main(True) # With diagonal

