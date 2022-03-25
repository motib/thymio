# Activity 3.9

# Copyright 2017, 2022 by Francesco Mondada and Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# ANN for spatial processing

# This program implements spatial processing using an ANN
#   that is broad: many neurons in the input layer,
#   but shallow
# The robot must turn towards any _single_ sensor that
#   detects an obstacle
# If many // all sensors detect the obstacle the robot
#   has three modes of behavior:
#     stop, move forwards, move backwards
# To move forwards or backwards an additional neuron
#   computes the sum of all the inputs and
#   multiplies by a coefficient

# The ANN is two-layered:
#   The neurons in the first layer read the sensor inputs x[0..4]
#     and output intermediate values u[0..4] to the neurons of
#     the second layer
#   In the second layer, there is a neuron for each motor,
#     and each neuron receives all the intermediate values

# The center button starts and stops the robot

# The forward button cycles between the three modes
# Mode is indicated by the circle leds

# Weights of neuron inputs
w0 = [ 4,-4, 0, 0, 0] 
w1 = [-2, 4,-2, 0, 0] 
w2 = [ 0,-2, 4,-2, 0] 
w3 = [ 0, 0,-2, 4,-2] 
w4 = [ 0, 0, 0,-4, 4]

# Weights of the intermediate values to obtain the motor powers
m0 = [-7,-4, 3, 4, 7]
m1 = [ 7, 4, 3,-4,-7]

# Neuron inputs, intermediates and outputs
x = [0]*5
u = [0]*5
y = [0]*2

# Scale factors for sensors and motors
sensor_scale   = 100
motor_scale    =   2

# Motor bias
# bias_index is the mode:
#  0 = stop at wall, 1 = go forwards, 2 = go backwards
bias_index = 0

# The bias_index is used to select from bias_coefficients
bias_coefficients = [0,1,-2]

# motor_bias is the sum of the inputs times the bias coefficient
motor_bias = 0

# State for start and stop
state = 0

timer_period[0] = 100    # Milliseconds
nf_leds_circle(32,0,0,0,0,0,0,0)

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

# Set mode with forward button
@onevent
def button_forward():
  global bias_index
  bias_index = (bias_index+1) % 3
  if bias_index == 0: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if bias_index == 1: nf_leds_circle(0,32,0,0,0,0,0,0) 
  if bias_index == 2: nf_leds_circle(0,0,32,0,0,0,0,0) 

# Activiate neurons periodically
@onevent
def timer0():
  global motor_left_target, motor_right_target
  global x, u, y, motor_bias

  # Do nothing if stopped
  if state == 0: pass 

  # Get and scale inputs
  x[0] = prox_horizontal[0]//sensor_scale
  x[1] = prox_horizontal[1]//sensor_scale
  x[2] = prox_horizontal[2]//sensor_scale
  x[3] = prox_horizontal[3]//sensor_scale
  x[4] = prox_horizontal[4]//sensor_scale

  # Compute intermediate values
  u[0] = x[0]*w0[0]+x[1]*w0[1]+x[2]*w0[2]+x[3]*w0[3]+x[4]*w0[4] 
  u[1] = x[0]*w1[0]+x[1]*w1[1]+x[2]*w1[2]+x[3]*w1[3]+x[4]*w1[4] 
  u[2] = x[0]*w2[0]+x[1]*w2[1]+x[2]*w2[2]+x[3]*w2[3]+x[4]*w2[4] 
  u[3] = x[0]*w3[0]+x[1]*w3[1]+x[2]*w3[2]+x[3]*w3[3]+x[4]*w3[4] 
  u[4] = x[0]*w4[0]+x[1]*w4[1]+x[2]*w4[2]+x[3]*w4[3]+x[4]*w4[4] 
  # Replace negative values by zero
  for i in range(5):
    if u[i] < 0: u[i] = 0 

  # Compute outputs
  y[0] = u[0]*m0[0]+u[1]*m0[1]+u[2]*m0[2]+u[3]*m0[3]+u[4]*m0[4] 
  y[1] = u[0]*m1[0]+u[1]*m1[1]+u[2]*m1[2]+u[3]*m1[3]+u[4]*m1[4] 

  # Compute motor bias
  motor_bias = (x[0]+x[1]+x[2]+x[3]+x[4]) * \
                bias_coefficients[bias_index]

  # Set motor powers using motor_bias and motor_scale
  motor_left_target  = (y[0] + motor_bias) // motor_scale
  motor_right_target = (y[1] + motor_bias) // motor_scale
