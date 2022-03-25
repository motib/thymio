"""
  Frontier algorithm
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA
"""

import copy

# Limit for low occupancy probability
LOW = .4

# Grid maps
#   Negative numbers represent unknown cells
#   When printing: "?" is an unknown cell
#                  "*" is a frontier cell
#                  "@" is the location of the robot
grid1 = [
    [-1 for col in range(16)],
    [-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,1,.9,-1,-1],
    [-.9,-.1,-.1,-.1,-.2,1,.1,.1,-1,-.1,-.1,1,.2,1,-1,-1],
    [-1,-.1,-.1,-.1,-.1,1,.1,.1,.1,.1,.1,.1,.2,1,-1,-1],
    [-1,-.1,-.1,-.9,-.1,.9,.1,.1,.1,.1,.1,.1,.2,1,-1,-1],
    [-1,-.1,-.3,-1,-.1,.1,.1,.1,.1,.1,.1,.1,.1,-.8,-1,-1],
    [-1,-.1,-1,-1,-.1,.1,.1,.1,.1,.1,.1,.1,.1,-.1,-1,-1],
    [-1,-.1,-.1,-.1,-.1,-.8,-.1,.2,.1,.1,.2,.2,.1,-.1,-1,-1],
    [-1,-.1,-.1,-.1,-.1,-1,-1,1,1,.9,1,-1,-.1,-.1,-1,-1],
    [-1,-1,-1,-1,-1,-.8,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1 for col in range(16)]
    ]

grid2 = [
    [-1 for col in range(7)],
    [-1,-.1,-.1,.1,-.1,-.1,-1],
    [-1,-.1,.1,.1,1,-1,-1],
    [-1,-.1,.1,.1,1,-1,-1],
    [-1,1,1,1,1,-1,-1],
    [-1 for col in range(7)],
    [-1 for col in range(7)],
    ]

# Print the grid indicating the frontier
#   and the position of the robot
def print_grid(g,frontier,robot):
    for row in range(len(g)):
        for col in range(len(g[0])):
            # Unknown cell
            if g[row][col] < 0:
                print("  ?  ",end="")
            # Print "1" without decimal
            elif g[row][col] == 1:
                print("  1  ",end="")
            else:
                # Print cell with robot
                if robot[0] == row and robot[1] == col:
                    print("{:4.1f}@".format(g[row][col]),end="")
                # Print frontier cell
                elif (row,col) in frontier:
                    print("{:4.1f}*".format(g[row][col]),end="")
                # Print cell with occupancy probability
                else:
                    print("{:4.1f} ".format(g[row][col]),end="")
        print()
    print()

# Print the path
#     "?" unknown cell
#     "*" obstacle cell
#     "0" open cell
#     "n" step of the path
def print_path(g,path):
    for row in range(len(g)):
        for col in range(len(g[0])):
            if g[row][col] < 0:
                print("  ?  ",end="")
            elif g[row][col] > LOW:
                print("  *  ",end="")
            else:
                if (row,col) in path:
                    print("{:4d} ".format(path.index((row,col))+1),end="")
                else:
                    print("  0  ",end="")
        print()
    print()

# Compute the frontier
#   Cell must have positive occupancy probability <= LOW and
#     an adjacent cell (left,right,up,down) has unknown probability
def compute_frontier(g):
    frontier = []
    for row in range(len(g)):
        for col in range(len(g[0])):
            if (g[row][col] > 0 and
                g[row][col] <= LOW and
                (g[row-1][col] < 0 or
                 g[row][col-1] < 0 or
                 g[row][col+1] < 0 or
                 g[row+1][col] < 0)):
                frontier.append((row,col))
    return frontier

# Update the grid by sensing occupancy probabilities
#   of unknown adjacent cells
def update_grid(g,robot):
    r = robot[0]
    c = robot[1]
    # Horizontal and vertical
    g[r-1][c]   = abs (g[r-1][c]) 
    g[r][c-1]   = abs (g[r][c-1])
    g[r][c+1]   = abs (g[r][c+1])
    g[r+1][c]   = abs (g[r+1][c])
    # Diagonal
    g[r-1][c-1] = abs (g[r-1][c-1])
    g[r-1][c+1] = abs (g[r-1][c+1])
    g[r+1][c-1] = abs (g[r+1][c-1])
    g[r+1][c+1] = abs (g[r+1][c+1])
    return g

# Get closest frontier cell
#   by Manhattan distance metric
def get_closest_frontier_cell(frontier,robot):
    min = 1000
    while frontier != []:
        cell = frontier.pop()
        distance = abs(robot[0]-cell[0]) + abs(robot[1]-cell[1])
        if distance < min:
            min = distance
            closest = cell
    return closest

# Count number of neighbors of a cell
def count_neighbors(grid,cell):
    n = 0
    row = cell[0]
    col = cell[1]
    # Horizontal and vertical
    if grid[row-1][col] < 0: n += 1
    if grid[row+1][col] < 0: n += 1
    if grid[row][col-1] < 0: n += 1
    if grid[row][col+1] < 0: n += 1
    # Diagonal
    if grid[row-1][col-1] < 0: n += 1
    if grid[row+1][col+1] < 0: n += 1
    if grid[row-1][col+1] < 0: n += 1
    if grid[row+1][col-1] < 0: n += 1
    return n
    
# Get closest frontier cell with priority to cell with
#   the maximum value of distance / number of unknown neighbors
def get_closest_frontier_cell_priority(grid,frontier,robot):
    max_priority = 0
    # Collect all cells of minimum distance in a list
    closest = []
    while frontier != []:
        cell = frontier.pop()
        # Compute distance and unknown neighbors
        distance = abs(robot[0]-cell[0]) + abs(robot[1]-cell[1])
        neighbors = count_neighbors(grid,cell)
        # Compute priority
        priority = float(neighbors / distance)
        # Check if higher than current maximum priority
        if priority > max_priority:
            max_priority = priority
            closest = cell
    return closest

# Explore the grid map
# Parameters:
#  grid map (use a deep copy to reuse global grid declaration!)
#  row and col of the robot
#  priority to frontier cell with most unknown neighbors
#  verbose to print grid map after each step
def explore(grid,row,col,priority,verbose):
    # Initial position of robot
    robot = (row,col)

    # Initialize path to the robot's initial position
    path = [robot]
    print("Frontier algorithm")

    # Compute initial frontier and print grid
    frontier = compute_frontier(grid)
    print_grid(grid,frontier,robot)

    # Explore grid
    while frontier != []:
        # Move to the closest frontier cell
        if priority:
            closest = get_closest_frontier_cell_priority(grid,frontier,robot)
        else:
            closest = get_closest_frontier_cell(frontier,robot)
        path.append(closest)
        robot = closest
        # Update the grid by sensing from new position
        grid = update_grid(grid,robot)
        # Update the frontier
        frontier = compute_frontier(grid)
        if verbose:
            print_grid(grid,frontier,robot)

    # Exploration terminated, print the path
    print_path(grid,path)

# Main program

explore(copy.deepcopy(grid1),5,9,priority=False,verbose=True)

explore(copy.deepcopy(grid2),3,3,priority=False,verbose=True)

explore(copy.deepcopy(grid2),3,3,priority=True,verbose=True)
