# Activity 2.5a

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0
 
# Display the attitude of in the three axes
# Select axis by touching forward, center, backwards buttons
 
axis = 0 
nf_leds_circle(0,0,0,0,0,0,0,0)
timer_period[0] = 500 # Milliseconds

# Set the circle leds to indicate the sample
# Make positive for display on leds
def set_circle_leds(sample):
  if sample < 0: sample = -sample
  nf_leds_circle( \
    (sample//1)*31, (sample//2)*31, (sample//6)*31, (sample//10)*31, \
    (sample//14)*31, (sample//18)*31, (sample//22)*31, (sample//26)*31)

# roll
@onevent
def button_forward():
  global axis
  axis = 0

# pitch
@onevent
def button_center():
  global axis
  axis = 1

# yaw
@onevent
def button_backward():
  global axis
  axis = 2

# Sample the chosen accelerometer
@onevent
def acc():
  sample = acc[axis]
  set_circle_leds(sample)

# Print the accelerometer value for current axis
@onevent
def timer0():
    global acc
    print(acc[axis])
