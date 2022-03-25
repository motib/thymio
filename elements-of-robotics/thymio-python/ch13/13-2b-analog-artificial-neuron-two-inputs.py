# Activity 13.2

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements an analog artificial neuron
#   with two inputs
# The inputs x1 and x2 are taken from the rear proximity sensors
# The input are multiplied by the weights w1, w2 and the
#   result (suitably scaled, if necessary) is used
#   to control the intensity of the top leds
#   and the speed and direction at which the Thymio runs away
#   from the object detected by the center sensor
# The weights determine the relative control that each
#   input has on the output
# The sensor with the larger weight has more effect on the output

w1 = 10      # Weight of neuron input
w2 = 20      # Weight of neuron input
x1 = 0       # Neuron input
x2 = 0       # Neuron input
y  = 0       # Neuron output
intensity = 0# Intensity of light
power = 0    # Motor power
scale = 100  # Scale factor for sensor

timer_period[0] = 100    # Milliseconds

# Activiate neuron periodically
@onevent
def timer0():
  global x1, x2, y, power, intensity
  global motor_left_target, motor_right_target
  # Get inputs
  x1 = prox_horizontal[5]//scale
  x2 = prox_horizontal[6]//scale
  y = x1*w1 + x2+w2
  intensity = y // 15
  power = y
  nf_leds_top(intensity,0,0)
  motor_left_target  = -power
  motor_right_target = -power
