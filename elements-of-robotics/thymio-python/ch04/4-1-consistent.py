# Activity 4.1

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# The robot cycles through four states, changing state once every second:
# moving forwards, turning left, turning right, moving backwards.

state = [0,0,0,0]
new_state = [0,0,0,0]

start_stop = 0

nf_leds_circle(0,0,0,0,0,0,0,0)

# subroutine to display the current state
def display_state():
    nf_leds_circle(0,state[1]*32,0,state[3]*32,0,state[2]*32,0,state[0]*32)

# Start and stop with center button
@onevent
def button_center():
  global start_stop, motor_left_target, motor_right_target
  if  button_center == 0:
    if  start_stop == 0:
      start_stop = 1
    else:
      start_stop = 0
      motor_left_target  = 0
      motor_right_target = 0

# Progress through four states by tapping
@onevent
def tap():
    global state, new_state, motor_left_target, motor_right_target, time_period
    if start_stop == 0: return
    if state[0] == 0 and state[1] == 0:
        motor_left_target = 200
        motor_right_target = 200
        new_state[0] = 0
        new_state[1] = 1

    elif state[0] == 0 and state[1] == 1:
        motor_left_target = -200
        motor_right_target = 200
        new_state[0] = 1
        new_state[1] = 0

    elif state[0] == 1 and state[1] == 0:
        motor_left_target = 200
        motor_right_target = -200
        new_state[0] = 1
        new_state[1] = 1
    
    else: # state[0] == 1 and state[1] == 1:
        motor_left_target = -200
        motor_right_target = -200
        new_state[0] = 0
        new_state[1] = 0

    nf_math_copy(state, new_state)
    display_state()
