# Activity 4.4a

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# The robot searches left and right until it detects an object
# It approaches the object, stopping if it is near
# The state is displayed in the top leds

## This program uses timers not obstacles for changing the search direction ##

MOTOR = 150        # motor power
DETECTION = 1000   # threshold for detecting an object
NEAR = 3000        # threshold for detecting a near object
TIMER = 1000       # timer for changing direction

state = 0  # 0 = stopped/found, 1 = left, 2 = right, 3 = approach
nf_leds_top(0,0,0)
timer_period[0] = 0

# Turn on or off if the center button is released
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  if button_center == 0:
    if state == 0:
      # Initially search left
      state = 1
      timer_period[0] = TIMER
    else:
      # Stop
      state = 0
      nf_leds_top(0,0,0)
      motor_left_target = 0
      motor_right_target = 0
      timer_period[0] = 0
 
# Timer expired
@onevent
def prox():
  global state, motor_left_target, motor_right_target, timer_period
  # Search left
  if state == 0: return
  if state == 1 or state == 2:
    # Object detected by center sensor -> approach
    if prox_horizontal[2] > DETECTION:
      motor_left_target = MOTOR
      motor_right_target = MOTOR
      state = 3
      timer_period[0] = 0
      nf_leds_top(32,0,0)
    else:
      timer_period[0] = TIMER
  # Approaching, if the object is near stop
  elif state == 3 and prox_horizontal[2] > NEAR:
    motor_left_target = 0
    motor_right_target = 0
    state = 0
    nf_leds_top(0,0,0)

@onevent
def timer0():
    global state, motor_left_target, motor_right_target
    if state == 0 or state == 3: return
    if state == 1:
        motor_left_target = MOTOR
        motor_right_target = -MOTOR
        state = 2
        nf_leds_top(0,32,0)
    elif state == 2:
        motor_left_target = -MOTOR
        motor_right_target = MOTOR
        state = 1
        nf_leds_top(0,0,32)
