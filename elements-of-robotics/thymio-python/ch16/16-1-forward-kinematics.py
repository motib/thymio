# Activity 16.1

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Forward kinematics

# Center button to start, stop
# Show state in circle leds

# The robot turns left, moves straight, turns right, moves straight
# Set the values in the array "period" to specify the angles and distances
# For inverse kinematics do the computations offline

MOTOR = 250
MOTOR_CHANGE = 100

state   = 0  # 0=off, 1=left turn, 2=straight, 3=right turn, 4=straight
period = [0,1000,4000,2000,4000]
motor_left  = [0, MOTOR-MOTOR_CHANGE, MOTOR, MOTOR+MOTOR_CHANGE, MOTOR]
motor_right = [0, MOTOR+MOTOR_CHANGE, MOTOR, MOTOR-MOTOR_CHANGE, MOTOR]

nf_leds_circle(0,0,0,0,0,0,0,0)
timer_period[0] = 0

# Set the circle leds to indicate the state
def set_circle_leds():
  if state==0: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if state==1: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if state==2: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if state==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if state==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if state==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# When center button released
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  if button_center == 0:
    # If off, set state to 1 (on) and dirve forwards
    if state == 0:
      state = 1
      motor_left_target  = MOTOR - MOTOR_CHANGE
      motor_right_target = MOTOR + MOTOR_CHANGE
      timer_period[0] = period[1]
      set_circle_leds()
    #   else: if state is on, stop the motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0
      timer_period[0] = 0
      set_circle_leds()

# Timer, go to next state
@onevent
def timer0():
  global state, motor_left_target, motor_right_target, timer_period
  if state == 0: return
  for i in range(1,5):
    if state == i:
      state = (state+1) % 5
      motor_left_target  = motor_left[state]
      motor_right_target = motor_right[state]
      timer_period[0] = period[state]
      set_circle_leds()
