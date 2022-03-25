# Activity 5.10

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Center button to start, stop
# Left, right buttons set motor power (by +//- 100)
# Forward, backward buttons to set difference
#   between left and right motors (by +//- 10)
# Use difference for calibration so that the robot moves straight

# Robot runs for FORWARD_TIMER seconds
# Then it checks if it is over a black tape
# If not it moves backwards and forwards for SEARCH_TIME ms
#   going faster and faster until it finds the tape

# Optional jitter in forward motion

motor  = 0        # Motor power
motor_diff = 0    # Difference between motors
state = 0         # 0 = off, 1 = on, 2= timer expired, search
jitter = 0        # Random jitter

JITTER = 3
FORWARD_TIMER = 4000
SEARCH_TIME = 600
SCALE_MOTOR = 15

nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_top(0,0,0)
timer_period[0] = 0
timer_period[1] = 0

# Set the circle leds to indicate the motor power
def set_circle_leds():
  if motor//100==0: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor//100==1: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if motor//100==2: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if motor//100==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if motor//100==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if motor//100==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Button event handlers
#   Left//right: increase or decrease motor power within 0-500
@onevent
def button_left():
  global motor
  if  button_left == 0:
    motor = motor - 100
    if  motor < 0: motor = 0 
    set_circle_leds()

@onevent
def button_right():
  global motor
  if  button_right == 0:
    motor = motor + 100
    if  motor > 500: motor = 500 
    set_circle_leds()

#   forwards, backwards: increase or decrease diff within 0-100
@onevent
def button_forward():
  global motor_diff
  if  button_forward == 0:
    motor_diff = motor_diff + 10
    if  motor_diff > 100: motor_diff = 100 

@onevent
def button_backward():
  global motor_diff
  if  button_backward == 0:
    motor_diff = motor_diff - 10
    if  motor_diff < 0: motor_diff = 0 

# When center button released
@onevent
def button_center():
  global state, motor_diff, motor, timer_period
  global motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, set state to 1 (on) and dirve forwards
    if  state == 0:
      state = 1
      motor_left_target  = motor + motor_diff
      motor_right_target = motor
      nf_leds_top(0,0,0)
      timer_period[0] = FORWARD_TIMER
      timer_period[1] = 0
    #   else: if state is on, stop the motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0
      motor = 0
      motor_diff = 0
      set_circle_leds()
      nf_leds_top(0,0,0)
      timer_period[0] = 0
      timer_period[1] = 0  

# Add jitter and check for goal
@onevent
def prox():
  global state, motor_diff, motor, jitter
  global motor_left_target, motor_right_target
  # Add jitter
  ran = math_rand()
  jitter = JITTER * (ran//1000)
  if state == 1:
   motor_left_target  = motor + jitter + motor_diff
   motor_right_target = motor + jitter
   return

  # Check for goal tape  
  if state == 2:
    if prox_ground_delta[0] < 200 or \
       prox_ground_delta[1] < 200:
      nf_leds_top(32,0,0)
      motor_left_target  = 0
      motor_right_target = 0
      state = 0

# Forwards timer: if expired go to search state and set search timer
@onevent
def timer0():
  global timer_period, state, motor
  if state != 1: pass
  else:
      timer_period[1] = SEARCH_TIME
      motor = 100
      state = 2

# Search timer: go faster and faster
@onevent
def timer1():
  global state, motor
  global motor_left_target, motor_right_target
  if state != 2: pass
  else:
    motor = -1*((motor*SCALE_MOTOR)//10)
    motor_left_target = motor
    motor_right_target = motor
