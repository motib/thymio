# Activity 13.1

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements an artificial neuron to simulate
#   the logic gates "or" and "and"
# The inputs x1 (respectively, x2) are 1 or 0 deping on whether
#   the left (respectively, right) sensors detect an object
# There is also a constant input of 1

# The output y is the "and" or "or" of x1 and x2
# The output is indicated by the top leds:
#   0 = white, 1 = red
# and by movement of the robot:
#   0 = move, 1 = object detected so stop

# The center button toggles between "or" and "and" gates
# The gate is indicated by the circle leds:
#   1 led for "or", 2 leds for "and"

THRESHOLD = 1500

timer_period[0] = 100    # Milliseconds

or_weights    = [-10,20,20]  # Weights for or gate
and_weights   = [-30,20,20]  # Weights for and gate
w             = or_weights   # Set with weights for "and" or "or"

x1 = 0   # First input
x2 = 0   # Second input
y  = 0   # Output
gate = 0 # 0 for "or" gate, 1 for "and" gate

timer_period[0] = 100    # Milliseconds
gate = 0                 # Initialize to "or" gate
w = or_weights
nf_leds_circle(32,0,0,0,0,0,0,0)

# Toggle between "or" and "and" gates
@onevent
def button_center():
  global w, gate
  if button_center == 0:  # Run on release of button
    if gate == 1:
      w = or_weights
      nf_leds_circle(32,0,0,0,0,0,0,0)
    else:
      w = and_weights
      nf_leds_circle(32,0,0,0,32,0,0,0)   
    gate = 1 - gate

# Activiate neuron periodically
@onevent
def timer0():
  global x1, x2, y, motor_left_target, motor_right_target
  # Get inputs: left or right proximity sensors > threshold
  if prox_horizontal[0] > THRESHOLD or \
     prox_horizontal[1] > THRESHOLD:
    x1 = 1
  else:
    x1 = 0
  if prox_horizontal[3] > THRESHOLD or \
     prox_horizontal[4] > THRESHOLD:
    x2 = 1
  else:
    x2 = 0  

  # The neuron computes the value of y
  y = 1*w[0] + x1*w[1] + x2*w[2]

  # A positive value of y is a "1", otherwise "0"
  if y > 0:
    nf_leds_top(32,0,0)
    motor_left_target = 0
    motor_right_target = 0
  else:
    nf_leds_top(32,32,32)
    motor_left_target = 100
    motor_right_target = 100
