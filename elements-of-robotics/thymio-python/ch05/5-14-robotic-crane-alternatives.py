# Activity 5.14

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Center button to stop
# Left button for mode 1: fast_motor, long_period
# Right button for mode 2: slow_motor, short_period
# Forward button for mode 3: fast_motor, long_period
#   but moves backwards when the tape is detected
# Show state in circle leds
# Top leds red when tape found but
#   change to green when going backwards in mode 3

long_period  = 750    # period of fast actuator sample
short_period = 200    # period of slow actuator sample
fast_motor   = 400    # motor power fast actuator
slow_motor   = 200    # motor power slow actuator
threshold    = 300    # threshold to find tape
state        = 0      # 0=off, 1=fast, 2=slow, 3=both
found        = False  # tape found

timer_period[0] = 0
set_circle_leds()
set_top_leds()

# Stop everything
def stop():
    global motor_right_target, motor_left_target
    global state, found
    state = 0
    found = False
    motor_left_target = 0
    motor_right_target = 0
    timer_period[0] = 0

# Bottom sensors determine if tape is found
def found_tape():
    global found
    if prox_ground_delta[0] < threshold or \
       prox_ground_delta[1] < threshold:
      found = True
      set_top_leds()
    else:
      found = False
      set_top_leds()

# Check if tape found and process according to state
@onevent
def timer0():
    global state, timer_period
    global motor_left_target, motor_right_target
    # state 0: do nothing
    found_tape()
    if state == 0: return 
    # state 1:  of long arm, start turn=1
    elif state == 1 and found:
        stop()
    elif state == 2 and found:
        stop()
    elif state == 3 and found:
        set_mode(4, -slow_motor, short_period)
    elif state == 4 and not found:
        stop()

# Stop robot
@onevent
def button_center():
    if button_center == 0:
            stop()

# Set mode: state, motors, period
def set_mode(s, m, p):
    global motor_right_target, motor_left_target, state, timer_period
    state = s
    motor_left_target = m
    motor_right_target = m
    timer_period[0] = p
    set_circle_leds()
    set_top_leds()

# Set mode 1
@onevent
def button_left():
    if button_left == 0: set_mode(1, fast_motor, long_period)

# Set mode 2
@onevent
def button_right():
    if button_right == 0: set_mode(2, slow_motor, short_period)

# Set mode 3
@onevent
def button_forward():
    if button_forward == 0: set_mode(3, fast_motor, long_period)

# Set top leds: red if found but green if going backwards
def set_top_leds():
    global state, found
    if found: nf_leds_top(32,0,0)
    else:     nf_leds_top(0,0,0)
    if state == 4: nf_leds_top(0,32,0)

# Display state in circle leds
def set_circle_leds():
  if state==0: nf_leds_circle(0,0,0,0,0,0,0,0)    
  if state==1: nf_leds_circle(32,0,0,0,0,0,0,0)   
  if state==2: nf_leds_circle(32,32,0,0,0,0,0,0)  
  if state==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if state==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
