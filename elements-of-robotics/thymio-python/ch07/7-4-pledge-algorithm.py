# Activity 7.4
# Also Activity 7.3

# Copyright 2013, 2016, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Obstacle avoidance with and without Pledge algorithm,
#   deping on computation of turn_sum in prox()
#Uncomment the line for the selected algorithm ####

# The Thymio is assumed to start traveling "north"
#   and encounters an obstacle
# It follows the wall (here using a black tape
#   and following the left edge using two sensors
#   (right on tape, left off tape) for a smooth ride

# The surface is at an incline so the yaw and pitch
#   accelerometers measure the heading of the robot
#   The heading is displayed on the top leds
# When the robot is off the tape and traveling north
#   it has avoided the obstacle and continues north

# There is a bug corrected by the Pledge algorithm:
#   The robot travels straight if the sum of its turns
#   is 0 degrees, not north (0 degrees mod 360)
# The difference is in the event handler for prox:
#    Choose: turn_sum % 360 == 0  or  sum_sum == 0

# Left, right buttons set motor power in increments of 50
#   The circle leds display the power setting
# Center button to start, stop

THRESHOLD_LOW = 450   # for sensing the tape
THRESHOLD_HIGH = 250
ACC = 6               # threshold for acclerometers

# Variables
state  = 0       # 0 = off, 1 = on
motor  = 50       # Selected motor power
yaw    = 0       # Save acc[0]
pitch  = 0       # Save acc[1]
found_black = 0  # Initial detection of obstacle
turn_sum = 0     # Cumulative sum of turns, +//- 90 on each turn
heading  = 0     # 0 = left, 1 = down, 2 = right, 3 = up
previous_heading = -1 # To check for a turn

# Initialization
nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_top(0,0,0)
motor_left_target  = 0
motor_right_target = 0

# Set the circle leds to indicate the motor power
def set_circle_leds():
  if motor//50==1: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor//50==2: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if motor//50==3: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if motor//50==4: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if motor//50==5: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if motor//50==6: nf_leds_circle(32,32,32,32,32,0,0,0) 
  if motor//50==7: nf_leds_circle(32,32,32,32,32,32,0,0) 
  if motor//50==8: nf_leds_circle(32,32,32,32,32,32,32,0) 
  if motor//50==9: nf_leds_circle(32,32,32,32,32,32,32,32) 

# Left and right button event handlers
# Increase or decrease motor power in increments of 50
@onevent
def button_left():
  global motor
  if  button_left == 0:
    motor = motor - 50
    if  motor < 0: motor = 0 
    set_circle_leds()
  
@onevent
def button_right():
  global motor
  if  button_right == 0:
    motor = motor + 50
    if  motor > 500: motor = 500 
    set_circle_leds()

# Center button event handler: start and stop
@onevent
def button_center():
  global motor, state, found_black, turn_sum, previous_heading
  global motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, reinitialize, set state to on and start motors
    if  state == 0:
      state = 1
      found_black = 0
      turn_sum = 0
      previous_heading = -1
      motor_left_target  = motor
      motor_right_target = motor
      set_circle_leds()
      nf_leds_top(0,0,0)
   # If on, set state to off and stop motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0  
      nf_leds_circle(0,0,0,0,0,0,0,0)
      nf_leds_top(0,0,0)

# Proximity event
@onevent
def prox():
  global state, found_black, heading, turn_sum, motor  
  global motor_left_target, motor_right_target
  if  state == 0: return
  # Obstacle not yet found
  if found_black == 0:
    # If obstacle found, set found_black and heading
    if prox_ground_delta[0] < THRESHOLD_LOW or \
       prox_ground_delta[1] < THRESHOLD_LOW:
      found_black = 1
      heading = 3      # Up is north
  # Follow line
  # If off line,: if not north or not turn_sum = 0, turn right
  elif  prox_ground_delta[0] > THRESHOLD_HIGH and \
        prox_ground_delta[1] > THRESHOLD_HIGH and \
        not (turn_sum == 0):        # Pledge algorithm
#   elif  prox_ground_delta[0] > THRESHOLD_HIGH and \
#         prox_ground_delta[1] > THRESHOLD_HIGH and \
#         not (turn_sum % 360 == 0):   # Incorrect algorithm
      motor_left_target  = motor
      motor_right_target = -motor
  # If on line: turn left
  elif prox_ground_delta[0] < THRESHOLD_LOW and \
          prox_ground_delta[1] < THRESHOLD_LOW:
      motor_left_target  = -motor
      motor_right_target = motor
   # Else (right on, left off) drive straight
  else:
     motor_left_target  = motor
     motor_right_target = motor

# Update cumulative sum of turns
def update_turn_sum():
  global heading, previous_heading, turn_sum
  # Initially, previous_heading is -1
  if previous_heading == -1:
    previous_heading = heading
  # If heading not changed, pass
  elif heading == previous_heading:
      pass 
  # If heading changed, add//deftract 90 to//from direction
  elif heading == (previous_heading+1) % 4:
    turn_sum += 90
  elif heading == (previous_heading+3) % 4:
    turn_sum -= 90
  # Save current heading
  previous_heading = heading

# Acceleromter event handler
@onevent
def acc():
  global yaw, pitch, ACC, heading, acc
  # Save values in named variables for clarity
  yaw = acc[0]
  pitch = acc[1]
  # Both yaw and pitch too low, pass
  if abs(yaw) < ACC  and abs(pitch) < ACC: 
    pass
  # Yaw low, pitch high -> heading is up or down
  elif abs(yaw) < ACC and abs(pitch) >= ACC:
    if pitch > 0:
      heading = 3         # Up - red
      nf_leds_top(32,0,0)
    else:
      heading = 1         # Down - magenta
      nf_leds_top(32,0,32) 
  # Yaw high, pitch low -> heading is left or right
  elif abs(yaw) >= ACC and abs(pitch) < ACC:
    if yaw > 0:
      heading = 0         # Left - green
      nf_leds_top(0,32,0)
    else:
      heading = 2         # Right - cyan
      nf_leds_top(0,32,32)
  # Update turn sum
  update_turn_sum()
