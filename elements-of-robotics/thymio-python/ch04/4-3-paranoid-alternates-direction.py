# Activity 4.3

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0
# Does not implement the last requirement because it is not clear
#   if the robot is not turning except initially

# Paranoid behavior but alternates direction

state = 0
start_stop = 0

# set timer 0 to alternate
timer_period[0] = 0
nf_leds_top(0,0,0)

# Start and stop with center button
@onevent
def button_center():
  global start_stop, state, motor_left_target, motor_right_target
  if  button_center == 0:
    state = 0
    if  start_stop == 0:
      start_stop = 1
    else:
      start_stop = 0
      motor_left_target  = 0
      motor_right_target = 0
      nf_leds_top(0,0,0)

@onevent
def prox():
    global state, start_stop, motor_left_target, motor_right_target, time_period
    if start_stop == 0: return
    if prox_horizontal[2] > 2000:
        motor_left_target = 200
        motor_right_target = 200
        nf_leds_top(32,0,0)
    elif prox_horizontal[2] < 1000 and state == 0:
        motor_left_target = -200
        motor_right_target = 200
        timer_period[0] = 1000
        nf_leds_top(0,32,0)
    elif prox_horizontal[2] < 1000 and state == 1:
        motor_left_target = 200
        motor_right_target = -200
        timer_period[0] = 1000
        nf_leds_top(0,0,32)

@onevent
def timer0():
    global state, time_period, start_stop
    if start_stop == 0: return
    timer_period[0] = 0
    if state == 0:
        state = 1
        nf_leds_top(0,32,0)
    else:
        state = 0
        nf_leds_top(0,0,32)
