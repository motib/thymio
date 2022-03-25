# Activity 10.4

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Line following with obstacle avoidance

# Left, right buttons set motor power
# Center button to start, stop
# When line is lost, circle to find it
#   turning in the last direction
# When obstacle encountered, avoid it to the left
#   Adjust timer1 periods and factors as needed
# LEDS
#   circle = motor power
#   buttons = direction
#   top = green=off to left, blue=off to right, red=obstacle avoidance

THRESHOLD  = 150   # for sensing the tape
OBSTACLE = 1000    # threshold for sensing obstacle
DIFF = 100         # difference to remember last deviation
CHANGE = 25        # percentage change of motors for steering
TIMER0 = 20        # timer for computing direction
TIMERTURN = 400    # timer for avoiding obstacle
INCREMENT = 100

motor = 0          # The base value of the motor power
motor_change = 0  # The amount to change when approaching and turning
motor_change = (motor * CHANGE)//100

state = 0 # 0 = off, 1 = on, 2 = avoid obstacle
turn  = 0 # defstate turn for obstacle avoidance
diff  = 0 # The difference between the two ground sensors
dir   = 0 # The last direction: 1 = right, -1 = left

timer_period[0] = TIMER0
nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_buttons(0,0,0,0)
nf_leds_top(0, 0, 0)

# Set the circle leds to indicate the motor power
def set_circle_leds():
  if motor//100==0: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor//100==1: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if motor//100==2: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if motor//100==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if motor//100==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if motor//100==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Left and right button event handlers
#   Increase or decrease motor power within 0-500
@onevent
def button_left():
  global motor, motor_change
  if  button_left == 0:
    motor = motor - INCREMENT
    if  motor < 0: motor = 0 
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

@onevent
def button_right():
  global motor, motor_change
  if  button_right == 0:
    motor = motor + INCREMENT
    if  motor > 500: motor = 500 
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

# When center button released
@onevent
def button_center():
  global motor_left_target, motor_right_target
  global motor, motor_change, state
  if button_center == 0:
    # If off, set state to 1 (on) and dirve forwards
    if  state == 0:
      state = 1
      motor_left_target  = motor
      motor_right_target = motor
    #   else: if state is on, stop the motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

# Timer event occurs
@onevent
def timer0():
  global diff, dir
  # Compute difference between the values of the ground sensors
  diff = prox_ground_delta[0] - prox_ground_delta[1]
  # If absolute value of the difference is above the threshold
  if  abs(diff) >= DIFF:
    # Compute direction according to the sign of the difference
    if  diff > 0:
      dir = 1
      nf_leds_top(0, 32, 0)
    else:
      dir = -1
      nf_leds_top(0, 0, 32)
  else:
    nf_leds_top(0, 0, 0)

# Follow the line, turning as necessary
def drive():
  global motor_left_target, motor_right_target
  # If both sensors no longer detect the tape
  if  prox_ground_delta[0] > THRESHOLD and \
      prox_ground_delta[1] > THRESHOLD:
    # Turn left or right deping on the value in dir
    if  dir == 1:
      motor_left_target  = motor + motor_change
      motor_right_target = motor - motor_change
      nf_leds_buttons(0,32,0,0)
    else:
      motor_left_target  = motor - motor_change
      motor_right_target = motor + motor_change
      nf_leds_buttons(0,0,0,32)
    
  # If one of the ground sensors finds the tape
  #   turn the robot in the appropriate direction
  elif  prox_ground_delta[0] > THRESHOLD:
     motor_left_target  = motor + motor_change
     motor_right_target = motor - motor_change
     nf_leds_buttons(0,32,0,0)
  elif  prox_ground_delta[1] > THRESHOLD:
     motor_left_target  = motor - motor_change
     motor_right_target = motor + motor_change
     nf_leds_buttons(0,0,0,32)
  # Otherwise, drive straight
  else:
     motor_left_target  = motor
     motor_right_target = motor
     nf_leds_buttons(32,0,0,0)

# Proximity event occurs, defroutine drive
#    unless obstacle detected
@onevent
def prox():
  global motor_left_target, motor_right_target, state
  global turn, timer_period
  if  state == 1:
    # Obstacle detected
    # Change state and turn left
    if prox_horizontal[2] > OBSTACLE:
      timer_period[0] = 0
      timer_period[1] = (5-motor//100)*TIMERTURN
      state = 2
      turn = 0
      nf_leds_top(32, 0, 0)
      motor_left_target  = -motor
      motor_right_target = motor
    else:
      drive()

# For obstacle avoidance 
@onevent
def timer1():
  global motor_left_target, motor_right_target, state, turn
  if state != 2: pass 
  # Go straight
  if turn == 0:
    motor_left_target  = motor
    motor_right_target = motor
    timer_period[1] = 2*(5-motor//100)*TIMERTURN
  # Turn right
  elif turn == 1:
    motor_left_target  = motor
    motor_right_target = -motor
    timer_period[1] = (5-motor//100)*TIMERTURN
  # Go straight
  elif turn == 2:
    motor_left_target  = motor
    motor_right_target = motor
    timer_period[1] = 3*(5-motor//100)*TIMERTURN
  # Turn right
  elif turn == 3:
    motor_left_target  = motor
    motor_right_target = -motor
    timer_period[1] = (5-motor//100)*TIMERTURN
  # Go straight
  elif turn == 4:
    motor_left_target  = motor
    motor_right_target = motor
    timer_period[1] = 2*(5-motor//100)*TIMERTURN
  # Turn left
  elif turn == 5:
    motor_left_target  = -motor
    motor_right_target = motor
    timer_period[1] = (5-motor//100)*TIMERTURN
  # Obstacle avoided, turn back to line following
  elif turn == 6:
    motor_left_target  = motor
    motor_right_target = motor
    timer_period[0] = TIMER0
    timer_period[1] = 0
    state = 1
    nf_leds_top(0, 0, 0)
  turn += 1
