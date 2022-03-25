# Activity 7.5
# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Follow a line with localization

# Line following using right sensor
# Left sensor detects code:
#   top led red for white, blue for black
# Left, right buttons set motor power
# Center button to start, stop 

THRESHOLD_HIGH = 400  # for sensing the tape
THRESHOLD_LOW = 200
CHANGE = 25           # percentage change of motors for steering

# Variables
motor = 0          # The base value of the motor power
motor_change = 0   # The amount to change if approaching and turning
state = 0          # 0 = off, 1 = on

motor_change = (motor * CHANGE)//100
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

# When center button released
@onevent
def button_center():
  global motor, motor_change, state
  global motor_left_target, motor_right_target
  if  button_center == 0:
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
    nf_leds_top(0,0,0)
    set_circle_leds()

# Proximity event occurs, turn if necessary
@onevent
def prox():
  global motor, motor_change
  global motor_left_target, motor_right_target
  if  state != 0:
      if  prox_ground_delta[1] > THRESHOLD_HIGH:
         motor_left_target  = motor + motor_change
         motor_right_target = motor - motor_change
      elif prox_ground_delta[1] < THRESHOLD_LOW:
         motor_left_target  = motor - motor_change
         motor_right_target = motor + motor_change
      else:
         motor_left_target  = motor
         motor_right_target = motor
      if prox_ground_delta[0] < THRESHOLD_LOW:
         nf_leds_top(0, 0, 32)
      else:
         nf_leds_top(32, 0, 0)
