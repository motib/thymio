"""
  Dijkstra's shortest path algorithm on a grid map
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  The grid is a list of lists
  A cells contains the distance (initially 0's, 1's for obstacles)
  A coordinate is a two-element list [row,column]
"""

grid   = []   # Grid map
source = []   # Source cell
goal   = []   # Goal node
marked = []   # List of marked nodes
path   = []   # Build the shortest path
marks  = 0    # Number of cells marked

verbose = True # Verbose: print grids and paths incrementally

# Print the marked cells with costs
def print_marked():
    print ('Marked = ',end='')
    for i in range(len(marked)):
        r = marked[i][0]
        c = marked[i][1]
        print ('['+str(r)+', '+str(c)+', '+str(grid[r][c])+'], ',end='')
    print ()
    print ()

# Print the grid: S = source, G = goal, X = obstacle
def print_grid():
    global grid, source, goal, marked
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if source == [i,j]:
                print ('S', ' ',end='')
            elif goal == [i,j]:
                print ('G', ' ',end='')
            elif grid[i][j] == -1:
                print ('X', ' ',end='')
            else:
                print (grid[i][j], ' ',end='')
        print ()
    print_marked()

# Initialize the grid to 0's, -1's for obstacles
def init_grid():
    global grid, source, goal, marked, marks
    # Build grid of zeros
    grid = [[0 for i in range(6)] for j in range(5)]
    # Set obstacles
    grid[4][2] = -1
    grid[3][2] = -1
    grid[2][4] = -1
    grid[2][5] = -1
    grid[0][2] = -1
    grid[1][2] = -1
    source = [4,0]
    goal = [4,5]
    marked = [source]
    marks = 1

# Mark cell [row,col] with distance d+1
def mark_cell(row,col,d):
    global grid, source, marked, marks
    # Don't mark source even though its distance is 0!
    if [row,col] == source:
        return
    # Check if cell is in the grid
    if row < 0 or row >= len(grid) or \
       col < 0 or col >= len(grid[row]):
        return
    # If unmarked, mark with distance and add to marked list
    if grid[row][col] == 0:
        grid[row][col] = d+1
        marked.append([row,col])
        marks += 1
    else:
        return

# If cell [row,col] is at distance d-1, add it to the path
def add_cell_to_path(row,col,d):
    global grid, path
    if row < 0 or row >= len(grid) or \
       col < 0 or col >= len(grid[row]):
        return
    if grid[row][col] == d-1:
        path.append([row,col])
        return True
    else:
        return False

# Mark cells in grid with distance
def mark_cells_in_grid():
    while True:
        # Get oldest cell (shortest distance so far)
        row, col = marked.pop(0)
        # If it is the goal, terminate
        if goal == [row,col]:
            break
        # Distance of current cell
        distance = grid[row][col]
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
        if verbose: print (path)
        # Distance of current cell
        distance = grid[row][col]
        # Add some cell at distance-1
        if add_cell_to_path(row+1,col, distance):
            row += 1;
            continue
        if add_cell_to_path(row-1,col, distance):
            row -= 1;
            continue
        if add_cell_to_path(row,col+1, distance):
            col += 1;
            continue
        if add_cell_to_path(row,col-1, distance):
            col -= 1;
            continue
    # Path starts from goal so reverse
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
get_path()
print ('\nShortest path =', path)
print ('Length =', len(path)-1)
