# Activity 13.6

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements obstacle avoidance using an ANN
# Unlike the previous program where detection by the center
#   sensor caused the robot to move backwards,
#   here there are only two sensors and
#   the robot moves backwards when both sensors detect the obstacle
# When no obstalce is detected the robot moves forward

# The ANN is two-layered:
#   The neurons in the first layer read the sensor inputs x1 and x2
#     and output intermediate values u1 and u2 to the neurons of
#     the second layer
#   In the second layer, there is a neuron for each motor,
#     which receives the corresponding intermediate value
#     and a large constant value
#     There is also a bias neuron to ensure that the robot
#       moves forward when there is no obstacle

# Symbolically:
#  L//R is left//right, S is sensor, N is neuron, M is motor, B is Bias
# LS*1  + RS*-1        -> N1
# LS*-1 + RS*1         -> N2
# 200 - LS - RS        -> B
# N1*2  + (-100)*1 + B -> M1
# N2*2  + (-100)*1 + B -> M2

# The inputs x1, x2 are taken from
#   the left and right proximity sensors and scaled
#   so that their values are between 0 and 100
# There is a constant input of -100

# The center button starts and stops the robot

# Weights of neuron inputs
w_input        = 1  
w_intermediate = 2
w_constant     = 1

# Constant input value
constant_input = -100
# Constant bias value
constant_bias  = 200

# Neuron inputs, intermediates and outputs
x1 = 0
x2 = 0
u1 = 0
u2 = 0
y1 = 0
y2 = 0

# Output of bias neuron
bias = 0

# Scale factors for sensors and motors
sensor_scale   = 40
motor_scale    =  2

# State for start and stop
state = 0

timer_period[0] = 100    # Milliseconds

# Toggle start and stop with center button
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  if button_center == 0 :
    if state == 0:
      state = 1
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0

# Activiate neurons periodically
@onevent
def timer0():
  global x1, x2, u1, u2, y1, y2, bias
  global motor_left_target, motor_right_target
  # Do nothing if stopped
  if state == 0: return

  # Get and scale inputs
  x1 = prox_horizontal[0]//sensor_scale
  x2 = prox_horizontal[4]//sensor_scale

  # Compute outputs of neurons and set motor powers
  # Compute first layer of neurons
  u1 = x1*w_input - x2*w_input
  u2 = -x1*w_input + x2*w_input

  # Compute bias neuron
  bias = constant_bias - x1 - x2
  
  # Compute second layer of neurons
  y1 = constant_input*w_constant + u1*w_intermediate + bias
  y2 = constant_input*w_constant + u2*w_intermediate + bias

  # Set motor powers
  motor_left_target  = y1*motor_scale
  motor_right_target = y2*motor_scale
