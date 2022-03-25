# Activity 4.2

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# The robot moves forwards until it detects an object.
# It: moves backwards for one second and reverses to move forwards again.

state = 0
start_stop = 0

# stop timer 0
timer_period[0] = 0

# reset output
nf_leds_top(0,0,0)

# Start and stop with center button
@onevent
def button_center():
  global start_stop, motor_left_target, motor_right_target, state
  if  button_center == 0:
    state = 0
    if  start_stop == 0:
      start_stop = 1
    else:
      start_stop = 0
      motor_left_target  = 0
      motor_right_target = 0

@onevent
def prox():
    global state, start_stop, motor_left_target, motor_right_target, timer_period
    if start_stop == 0: return
    if state == 0:
        motor_left_target = 200
        motor_right_target = 200
        nf_leds_top(32,0,0)
    if prox_horizontal[2] > 2800:
        motor_left_target = -200
        motor_right_target = -200
        timer_period[0] = 1000
        state = 1
        nf_leds_top(0,32,0)

@onevent
def timer0():
    global state, start_stop, motor_left_target, motor_right_target, timer_period
    if start_stop == 0: return
    timer_period[0] = 0
    if state == 1:
        motor_left_target = 200
        motor_right_target = 200
        state = 0
        nf_leds_top(32,0,0)
