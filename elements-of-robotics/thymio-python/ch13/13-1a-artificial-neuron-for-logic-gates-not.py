# Activity 13.1

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements an artificial neuron to simulate the "not" logic gate
# The input x1 is 1 or 0 deping on whether
#   the center sensor detect an object
# There is also a constant input of 1

# The output y is the "not" of x1
# The output is indicated by the top leds:
#   0 = white, 1 = red
# and by movement of the robot:
#   0 = not object detected, stop
#   1 = not not object detected = object detected, move

THRESHOLD = 1500

weights = [10,-20]    # Weights
x1 = 0   # Input
y  = 0  # Output

timer_period[0] = 100    # Milliseconds

# Activiate neuron periodically
@onevent
def timer0():
  global x1, y, motor_left_target, motor_right_target
  # Get inputs: center proximity sensor > threshold
  if prox_horizontal[2] > THRESHOLD:
    x1 = 1
  else:
    x1 = 0

  # The neuron computes the value of y
  y = 1*weights[0] + x1*weights[1]

  # A positive value of y is a "1", otherwise "0"
  if y > 0:
    nf_leds_top(32,0,0)
    motor_left_target = 0
    motor_right_target = 0
  else:
    nf_leds_top(32,32,32)
    motor_left_target = 100
    motor_right_target = 100
