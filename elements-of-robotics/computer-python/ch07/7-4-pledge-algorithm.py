"""
  Wall following algorithm including Pledge's improvement
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  A grid defines the environment with the walls marked
  The grid is a list of lists
  A cell contains 0 for open space, -1 for obstacles
  The location of the robot is a pair [row,col]

  In init_grid() choose obstacle that the original algorithm
    can or cannot avoid successfully
  In follow_wall() choose original algorithm or Pledge algorithm
"""

grid   = []   # Grid map
robot  = []   # [Row,col] is the location of the robot
dir    = 0    # Direction in degrees
steps  = 0    # Count the number of steps the robot takes

verbose = True # Verbose: print (grids and paths incrementally

# print (the grid
#   X = obstacle, _ = open cell
#   A,>,V,< = the robot facing in different directions
def print_grid():
    global grid,robot
    print ('direction =', dir)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if robot == [i,j]:
                if dir % 360 ==   0: print ('A ',end='')
                if dir % 360 ==  90: print ('> ',end='')
                if dir % 360 == 180: print ('V ',end='')
                if dir % 360 == 270: print ('< ',end='')
            elif grid[i][j] == -1:
                print ('X ',end='')
            else:
                print ('_ ',end='')
        print ()
    print ()

# Initialize the grid
def init_grid():
    global grid, robot
    # Build grid of zeros
    grid = [[0 for i in range(10)] for j in range(9)]

    # Set wall
    for i in range(1,8):
        grid[2][i] = -1
    for i in range(3,6):
        grid[i][1] = -1
    for i in range(1,6):
        grid[6][i] = -1
    # Add the following cell for a G-shaped obstacle
    #   that causes the original algorithm to loop indefinitely
    grid[5][5] = -1

    # Initial position of the robot
    robot = [7,7]

# Return the value of the cell "ahead" of the robot
def forward():
    global grid,dir,robot
    row, col = robot
    if dir % 360 ==   0: return grid[row-1][col]
    if dir % 360 ==  90: return grid[row][col+1]
    if dir % 360 == 180: return grid[row+1][col]
    if dir % 360 == 270: return grid[row][col-1]
    
# Return the value of the cell to the "right" of the robot
def right():
    global grid,dir,robot
    row, col = robot
    if dir % 360 ==   0: return grid[row][col+1]
    if dir % 360 ==  90: return grid[row+1][col]
    if dir % 360 == 180: return grid[row][col-1]
    if dir % 360 == 270: return grid[row-1][col]

# Move robot one step forward depending on its direction
def go_forward():
    global grid,dir,robot,steps
    row, col = robot
    if dir % 360 ==   0: robot = [row-1,col]
    if dir % 360 ==  90: robot = [row,col+1]
    if dir % 360 == 180: robot = [row+1,col]
    if dir % 360 == 270: robot = [row,col-1]
    steps += 1
    
# When the robot is not near an obstacle it moves forwards
#   to find the wall
def find_wall():
    global grid,dir,robot
    while True:
        # Reached the top row, terminate the algorithm
        if robot[0] == 0:
            return -1
        # If forward open, go forward
        #   else turn left and return
        if forward() == 0:
            go_forward()
        else:
            dir -= 90
            go_forward()
            return 0
        if verbose: print_grid()

# Follow the wall
def follow_wall():
    global grid,dir
    while True:
        # If forward open,
        #   check if direction is "north" or "zero"
        #   If so, return
        #   If right open, turn right
        #   Go forwards
        # Otherwise, forward blocked so turn left
        if forward() == 0:
            # if dir % 360 == 0:   # Incorrect algorithm
            if dir == 0:           # Pledge algorithm
                return
            if right() == 0:
                dir += 90
            go_forward()
        else:
            dir -= 90
        if verbose: print_grid()

# Initialize
init_grid()
print ('Initial grid')
print_grid()

# Loop to find wall and avoid it
while True:
    stop = find_wall()
    if stop == -1:
        print ('Avoided obstacle')
        break
    # Set limit on infinite loop
    elif abs(dir) >= 720:
        print ('Infinite loop')
        break
    print ('Found wall')
    print_grid()
    follow_wall()

