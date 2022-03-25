# Activity 7.2

# Copyright 2016, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Wall following
# Start with the right ground sensor on the tape
#   and the left ground sensor off the tape
# Based on line following with one sensor program
#   except that right sensor is used
# Start on the tape not on the floor
# When the objects is detected go to it and stop if near

THRESHOLD_LOW = 200    # for sensing tape
THRESHOLD_HIGH = 400
CHANGE = 100           # percentage change of motors for steering
DETECT = 1000          # for sensing goal

# Variables
motor = 0         # The base value of the motor power
# The amount to change if approaching and turning
motor_change = (motor * CHANGE)//100
state = 0         # 0 = off, 1 = on, 2 = go to goal

# Initialization
nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_top(0,0,0)

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
    motor = motor - 100
    if  motor < 0: motor = 0 
    motor_change = (motor * CHANGE)//100
    set_circle_leds()
  
@onevent
def button_right():
  global motor, motor_change
  if  button_right == 0:
    motor = motor + 100
    if  motor > 500: motor = 500 
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

@onevent
def button_center():
  global motor, state, motor_change
  global motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, reinitialize, set state to on and start motors
    if  state == 0:
      state = 1
      nf_leds_top(32,0,32)
      motor_left_target  = motor
      motor_right_target = motor
   # If on, set state to off and stop motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

# Go to the goal object
def goto_goal():
  global motor_left_target, motor_right_target, state
  # Turn towards the goal
  if prox_horizontal[0] > DETECT or \
     prox_horizontal[1] > DETECT:
      motor_left_target  = motor - motor_change
      motor_right_target = motor + motor_change
  elif prox_horizontal[3] > DETECT or \
       prox_horizontal[4] > DETECT:
      motor_left_target  = motor + motor_change
      motor_right_target = motor - motor_change
  # Stop if near
  elif prox_horizontal[2] > 4*DETECT:
      motor_left_target  = 0
      motor_right_target = 0
      state = 0
  # Go to the goal
  else:
      motor_left_target  = motor
      motor_right_target = motor

# Proximity event occurs
@onevent
def prox():
  global state, motor_left_target, motor_right_target
  # Return in off state
  if  state == 0: pass
  # If some horizontal sensor detects, go to the goal
  elif  state == 2: goto_goal()
  elif prox_horizontal[0] > DETECT or prox_horizontal[1] > DETECT or \
     prox_horizontal[2] > DETECT or prox_horizontal[3] > DETECT or \
     prox_horizontal[4] > DETECT:
    state = 2
    nf_leds_top(32,32,32)
    goto_goal()
  # Otherwise, follow line
  elif  prox_ground_delta[1] > THRESHOLD_HIGH:
      motor_left_target  = motor + motor_change
      motor_right_target = motor - motor_change
      nf_leds_top(0, 32, 0)
  elif prox_ground_delta[1] < THRESHOLD_LOW:
      motor_left_target  = motor - motor_change
      motor_right_target = motor + motor_change
      nf_leds_top(0, 0, 32)
  else:
      motor_left_target  = motor
      motor_right_target = motor
      nf_leds_top(32,0,0)
