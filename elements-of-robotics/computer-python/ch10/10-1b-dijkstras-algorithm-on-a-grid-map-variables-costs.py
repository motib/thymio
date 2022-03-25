"""
  Dijkstra's shortest path algorithm on a grid map with variable costs
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  The grid is a list of lists
  A cell contains the distance (initially 0's, -1's for obstacles)
    and the cost (usually 1)
  A coordinate is a two-element list [row,column]
"""

grid   = []   # Grid map
source = []   # Source cell
goal   = []   # Goal node
marked = []   # List of marked nodes
path   = []   # Build the shortest path
marks  = 0    # Number of cells marked

verbose = True # Verbose: print (grids and paths incrementally

# print (the marked cells with costs
def print_marked():
    print ('Marked = ',end='')
    for i in range(len(marked)):
        r = marked[i][0]
        c = marked[i][1]
        print ('['+str(r)+', '+str(c)+', '+str(grid[r][c][0])+'], ',end='')
    print ()
    print ()

# print (the grid: S = source, G = goal, X = obstacle
def print_grid():
    global grid, source, goal, marked
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if source == [i,j]:
                print ('[S, '+str(grid[i][j][1])+']  ',end='')
            elif goal == [i,j]:
                print ('[G, '+str(grid[i][j][1])+']   ',end='')
            elif grid[i][j] == [-1,0]:
                print ('[X   ]', ' ',end='')
            else:
                print (grid[i][j], ' ',end='')
        print ()
    print_marked()

# Initialize the grid to 0's, -1's for obstacles
def init_grid():
    global grid, source, goal, marked, marks
    # Build grid of zeros and cost 1
    grid = [[[0,1] for i in range(6)] for j in range(5)]
    # Set obstacles
    grid[4][2] = [-1, 0]; grid[3][2] = [-1, 0]; grid[2][4] = [-1, 0]
    grid[2][5] = [-1, 0]; grid[0][2] = [-1, 0]; grid[1][2] = [-1, 0]
    # Cells with higher cost
    grid[3][1] = [0,2]
    grid[3][4] = [0,2]
    grid[3][5] = [0,2]
    grid[4][4] = [0,2]
    source = [4,0]
    goal = [4,5]
    marked = [source]
    marks = 1

# Mark cell [row,col] with distance d+1
def mark_cell(row,col,d):
    global grid, source, marked, marks
    # Don't mark source!
    if [row,col] == source:
        return
    # Check if cell is in the grid
    if row < 0 or row >= len(grid) or \
       col < 0 or col >= len(grid[row]):
        return
    # If unmarked, mark with distance and add to marked list
    if grid[row][col][0] == 0:
        grid[row][col][0] = d + grid[row][col][1]
        marked.append([row,col])
        # Sort by cost: distance from source
        marked.sort(key=lambda cost: grid[cost[0]][cost[1]][0])
        marks += 1
    else:
        return

# Return distance of neighbors or -1
def add_cell_to_path(row,col):
    global grid, path
    if row < 0 or row >= len(grid) or \
       col < 0 or col >= len(grid[row]):
        return -1
    return grid[row][col][0]

# Mark cells in grid with distance
def mark_cells_in_grid():
    while True:
        # Get oldest cell (shortest distance so far)
        row, col = marked.pop(0)
        # If it is the goal, terminate
        if goal == [row,col]:
            break
        # Distance of current cell
        distance = grid[row][col][0]
        # Mark four neighbor cells, if possible
        mark_cell(row+1,col,distance)
        mark_cell(row-1,col,distance)
        mark_cell(row,col+1,distance)
        mark_cell(row,col-1,distance)
        if verbose: print_grid()

# Get the shortest path starting from the goal
def get_path():
    row, col = goal
    # Terminate when source cell is reached
    while [row,col] != source:
        # Get distances of neighboring cells
        n1 = add_cell_to_path(row+1,col)
        n2 = add_cell_to_path(row-1,col)
        n3 = add_cell_to_path(row,col+1)
        n4 = add_cell_to_path(row,col-1)
        # Initial value for minimum distance
        min = 10000
        # For each valid neighbor, check if it is the minimum
        if n1 != -1:
            closest_cell = 1; min = n1
        if n2 != -1 and n2 < min:
            closest_cell = 2; min = n2
        if n3 != -1 and n3 < min:
            closest_cell = 3; min = n3
        if n4 != -1 and n4 < min:
            closest_cell = 4; min = n4
        # Change row or col to that of closest cell
        if closest_cell == 1: row += 1
        if closest_cell == 2: row -= 1
        if closest_cell == 3: col += 1
        if closest_cell == 4: col -= 1
        # Append the new cell to the path
        path.append([row,col])
        if verbose: print (path)
    # Path list starts from goal so reverse
    path.reverse()


# Initialize
init_grid()
print ('Initial grid')
print_grid()

# Mark cells
mark_cells_in_grid()
print ('Final grid')
print_grid()
print ('Cells marked =', marks)
print ()

# Start with goal in path and get path
path = [goal]
if verbose: print ('Build path'); print(path)
get_path()
if verbose: print ()
print ('Shortest path =', path)
print ('Length =', grid[goal[0]][goal[1]][0])
