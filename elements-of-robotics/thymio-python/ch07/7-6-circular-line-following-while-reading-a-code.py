# Activity 7.6

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Circular line following while reading a code
# Drive in a circle
#   Stop if black tape detected, or
#     if timer interval has passed
# Adjust TIMER and check of second count as needed

THRESHOLD = 300  # for sensing tape
TIMER = 1000     # timer for computing direction

motor  = 0    # The motor power
state  = 0    # 0 = off, 1 = on
count  = 0    # Of seconds (half seconds would be more accurate...)
stop  = 0     # Seconds to stop
nf_leds_circle(0,0,0,0,0,0,0,0)

# Set the circle leds to indicate the motor power
# Set number of seconds to turn for each power
def set_circle_leds():
  global stop
  if motor//100==0:
      nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor//100==1:
      nf_leds_circle(32,0,0,0,0,0,0,0)
      stop = 18 
  if motor//100==2:
      nf_leds_circle(32,32,0,0,0,0,0,0)
      stop = 9 
  if motor//100==3:
      nf_leds_circle(32,32,32,0,0,0,0,0)
      stop = 6 
  if motor//100==4:
      nf_leds_circle(32,32,32,32,0,0,0,0)
      stop = 5 
  if motor//100==5:
      nf_leds_circle(32,32,32,32,32,0,0,0)
      stop = 4 

# Left and right button event handlers
#   Increase or decrease motor power within 0-500
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

# When center button released
@onevent
def button_center():
  global motor, state, count, timer_period
  global motor_left_target, motor_right_target
  if button_center == 0:
    # If off, set state to 1 (on) and dirve forwards
    if  state == 0:
      state = 1
      motor_left_target  = motor
      motor_right_target = 0
      timer_period[0] = TIMER
      count = 0
    #   else: if state is on, stop the motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0   
    set_circle_leds()

# Timer event occurs
@onevent
def timer0():
  global state, count
  global motor_left_target, motor_right_target
  if state == 1:
    count += 1
    if count > stop:
      motor_left_target  = 0
      motor_right_target = 0
      state = 0

# Proximity event occurs, stop if no detection
@onevent
def prox():
  global state
  global motor_left_target, motor_right_target
  if prox_ground_delta[0] < THRESHOLD or \
     prox_ground_delta[1] < THRESHOLD:
     motor_left_target  = 0
     motor_right_target = 0
     state = 0
