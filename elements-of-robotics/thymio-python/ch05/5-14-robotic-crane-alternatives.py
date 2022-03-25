# Activity 5.14

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Center button to start, stop
# Show state in circle leds

LONG_PERIOD = 1000  # period of fast actuator sample
SHORT_PERIOD = 200  # period of slow actuator sample
FAST_MOTOR = 400    # motor power fast actuator
SLOW_MOTOR = 200    # motor power slow actuator
THRESHOLD = 300     # threshold to find tape

# 0=off, 1=fast, 2=slow, 3=both
state = 0

# Tape found
found = 0

timer_period[0] = 0
nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_top(0,0,0)

# Display state in circle leds
def set_circle_leds():
  if state==0: nf_leds_circle(0,0,0,0,0,0,0,0)    
  if state==1: nf_leds_circle(32,0,0,0,0,0,0,0)   
  if state==2: nf_leds_circle(32,32,0,0,0,0,0,0)  
  if state==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if state==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if state==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

def stop():
  global motor_right_target, motor_left_target, state, found, timer_period
  state = 0
  found = 0
  motor_left_target = 0
  motor_right_target = 0
  timer_period[0] = 0

@onevent
def button_center():
    global state
    if button_center == 0:
      nf_leds_circle(0,0,0,0,0,0,0,0)
      nf_leds_top(0,0,0)
      stop()

@onevent
def button_left():
    global motor_right_target, motor_left_target, state, timer_period
    if button_left == 0:
      state = 1
      nf_leds_top(0,0,0)
      set_circle_leds()
      motor_left_target = FAST_MOTOR
      motor_right_target = FAST_MOTOR
      timer_period[0] = LONG_PERIOD

@onevent
def button_right():
    global motor_right_target, motor_left_target, state, timer_period
    if button_right == 0:
      state = 2
      nf_leds_top(0,0,0)
      set_circle_leds()
      motor_left_target =  SLOW_MOTOR
      motor_right_target = SLOW_MOTOR
      timer_period[0] = SHORT_PERIOD

@onevent
def button_forward():
    global motor_right_target, motor_left_target, state, timer_period
    if button_forward == 0:
      state = 3
      nf_leds_top(0,0,0)
      set_circle_leds()
      motor_left_target =  FAST_MOTOR
      motor_right_target = FAST_MOTOR
      timer_period[0] = LONG_PERIOD

def found_tape():
    global found
    if prox_ground_delta[0] < THRESHOLD or \
       prox_ground_delta[1] < THRESHOLD:
      found = 1
    else:
      found = 0

@onevent
def timer0():
  global state, motor_left_target, motor_right_target, timer_period
  # State 0: do nothing
  found_tape()
  if state == 0: return 
  # State 1:  of long arm, start turn=1
  elif state == 1 and found == 1:
    nf_leds_top(0,32,0)
    stop()
  elif state == 2 and found == 1:
    nf_leds_top(0,0,32)
    stop()
  elif state == 3 and found == 1:
    state = 4    
    nf_leds_top(32,0,0)
    set_circle_leds()
    motor_left_target =  -SLOW_MOTOR
    motor_right_target = -SLOW_MOTOR
    timer_period[0] = SHORT_PERIOD
  elif state == 4 and found == 0:
    nf_leds_top(32,32,32)
    stop()
