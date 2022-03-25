# Activity 12.4

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements corner detection
# The Thymio moves over a pattern (as shown in the book)
#   and stores samples of both of the ground proximity sensors

# On the first pass, check similar neighbors and turn on top LED
#   if only one out of four samples a0[i-1],a1[i-1],a0[i],a1[i] is black
# Horizontal and vertical edge detectors can now be applied
# On a second pass, the top LEDs are lit
#   if a corner is detected: both horizontal and vertical edges

# Experiment with the number of samples, the threshold,
#   the timer period and the sensor scale factors!!!

# Buttons:
#   Center:   start data collection (and stop)
#   Forward:  start second pass
#   Backward: apply edge detectors

SAMPLES = 12          # the number of samples taken
SAMPLES_NO_EDGES = 10 # for applying filters

# Pixel array: a for input, b for processed pixels
a0 = [0]*12    # Can't use variable here
a1 = [0]*12
horizontal = [0]*12
vertical= [0]*12

power        = 100 # Motor power
scale1       = 30  # Sensor scale factors
scale2       = 120
period       = 200 # Timer period
threshold    = 100 # Threshold for detection
state        = 0   # 0 = stop, 1 = first pass, 2 = second pass
count        = 0   # Count of similar neighbors
i            = 0   # Loop index

nf_leds_top(0,0,0)
timer_period[0] = 0
timer_period[1] = 0

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
  global threshold, timer_period, a0, a1
  if button_center == 0:
      if state == 0:
        i = 0
        nf_math_fill(a0,0)
        nf_math_fill(a1,0)
        motor_left_target  = power
        motor_right_target = power
        timer_period[0] = period
        state = 1
      else:
        stop() 

# Start second pass
@onevent
def button_forward():
  global motor_left_target, motor_right_target, state, i
  if button_forward == 0:
      timer_period[1] = period
      motor_left_target = power
      motor_right_target = power
      i = 0
      state = 2

# Compute edge detectors
@onevent
def button_backward():
  global horizontal, vertical
  if button_backward == 0:
      nf_math_fill(horizontal,0)
      nf_math_fill(vertical,0)
      for j in range(1,SAMPLES_NO_EDGES+1):
         # Horizontal: diff of previous and next of each sample
         horizontal[j] = (-a0[j-1] + a0[j+1]) + (-a1[j-1] + a1[j+1])
         # Vertical: diff of left and right samples
         vertical[j] = -a0[j-1] + a1[j-1]

# First pass timer event handler
@onevent
def timer0():
  global a0, a1, i, count
  if state == 0: return
  if i >= SAMPLES:
    stop()
    return
  a0[i] = (prox_ground_delta[0] * scale1) // scale2
  a1[i] = (prox_ground_delta[1] * scale1) // scale2
  # Similar neighbors corner detector
  # Count number of samples below threshold
  # If only 1, turn on top LED
  if i > 0:
    count = 0
    if a0[i-1] < threshold: count += 1 
    if a1[i-1] < threshold: count += 1 
    if a0[i]   < threshold: count += 1 
    if a1[i]   < threshold: count += 1 
    if count == 1:
      nf_leds_top(32,0,0)
    else:
      nf_leds_top(0,0,0)
  i += 1

# Second pass timer event handler
# Turn LED on // off if both edge detectors are above a threshold
@onevent
def timer1():
  if state != 2: return
  if i >= SAMPLES:
    stop()
    return
  if abs(horizontal[i]) > threshold and \
     abs(vertical[i])   > threshold:
    nf_leds_top(32,32,32)
  else:
    nf_leds_top(0,0,0)
    i += 1
