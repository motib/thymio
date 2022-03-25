# Activity 12.5

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements blob detection
# The Thymio moves over a pattern (as shown in the book)
# When the black rectangle is first detected it turns on the top led
#   and continues to do so as long as black is detected
# When the black rectangle s, it has detected the blog and
#   doesn't search for another one.

# Buttons:
#   Center:   start data collection (and stop)

SAMPLES = 30   # the number of samples taken

power        = 100 # Motor power
period       = 120 # Timer period
threshold    = 200 # Threshold for detection
state        = 0   # 0 = stop, 1 = start, 2 = found blob, 3 =  of blob
i            = 0   # Loop index

nf_leds_top(0,0,0)
timer_period[0] = 0

# Subroutine for stopping processing
def stop():
    global motor_left_target, motor_right_target, state
    state = 0
    motor_left_target = 0
    motor_right_target = 0
    timer_period[0] = 0
    state = 0
    nf_leds_top(0,0,0)

# Start first pass (initialize) and stop
@onevent
def button_center():
  global motor_left_target, motor_right_target, state, i
  global threshold, timer_period
  if button_center == 0:
      if state == 0:
        i = 0
        motor_left_target  = power
        motor_right_target = power
        timer_period[0] = period
        state = 1
      else:
        stop() 

# First pass timer event handler
@onevent
def timer0():
  global state, i
  i += 1
  if i > SAMPLES:
    stop()
    return
  if state == 0 or state == 3: return
  if state == 1:
    if prox_ground_delta[0] < threshold:
      state = 2
      nf_leds_top(32,32,32)
  elif prox_ground_delta[0] > threshold:
      state = 3
      nf_leds_top(0,0,0)
