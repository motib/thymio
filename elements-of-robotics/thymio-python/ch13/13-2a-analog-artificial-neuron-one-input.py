# Activity 13.2

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

#   Analog artificial neuron with one input

# This program implements a artificial neuron with one input
# The input x is taken from the center proximity sensor
# The input is multiplied by the weight w and the
#   result (suitably scaled, if necessary) is used
#   to control the intensity of the top leds
#   and the speed at which the Thymio retreats
#   from the object detected by the center sensor
# Larger weights cause the change in intensity
#   and motor power to change more rapidly

w = 10       # Weight of neuron input
x = 0        # Neuron input
y = 0        # Neuron output
intensity= 0 # Intensity of light
power = 0    # Motor power
scale = 100  # Scale factor for sensor

timer_period[0] = 100    # Milliseconds

# Activiate neuron periodically
@onevent
def timer0():
  global x, y, power, intensity
  global motor_left_target, motor_right_target
  # Get inputs
  x = prox_horizontal[2]//scale
  y = x * w
  intensity = y // 15
  power = y
  nf_leds_top(intensity,0,0)
  motor_left_target  = -power
  motor_right_target = -power
