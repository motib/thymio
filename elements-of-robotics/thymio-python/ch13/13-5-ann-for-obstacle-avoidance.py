# Activity 13.5

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements obstacle avoidance using an ANN
# The inputs x1, x2, x3 are taken from
#   the left, center and right proximity sensors and scaled
# There is a constant input of 1 which is scaled to match
#   the scaled sensor values
# The inputs are multiplied by the weights as shown in the book
#   and used to set the motor powers
# The center button starts and stops the robot

# Weights of neuron inputs
w_fwd  = 20  # Reasonable forward speed
w_back = 40  # > fwd so robot will move backwards
w_neg  = 30  # also > fwd
w_pos  = 10  # amplifies fwd so not too large

# Neuron inputs and outputs
x1 = 0
x2 = 0
x3 = 0
y1 = 0
y2 = 0

# Scale factors for sensors and constant factor
sensor_scale   = 200
constant_scale =  20

# State for start and stop
state = 0

timer_period[0] = 100    # Milliseconds

# Toggle start and stop with center button
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  if button_center == 0:
    if state == 0:
      state = 1
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0

# Activiate neurons periodically
@onevent
def timer0():
  global x1, x2, x3, y1, y2
  global motor_left_target, motor_right_target
  # Do nothing if stopped
  if state == 0: return
  # Get and scale inputs
  x1 = prox_horizontal[0]//sensor_scale
  x2 = prox_horizontal[2]//sensor_scale
  x3 = prox_horizontal[4]//sensor_scale

  # Compute outputs of neurons and set motor powers
  y1 = 1*constant_scale*w_fwd + x1*w_pos - x2*w_back - x3*w_neg
  y2 = 1*constant_scale*w_fwd - x1*w_neg - x2*w_back + x3*w_pos
  motor_left_target  = y1
  motor_right_target = y2
