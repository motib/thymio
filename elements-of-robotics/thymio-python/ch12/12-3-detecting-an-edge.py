# Activity 12.3

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# This program implements edge detection
# The Thymio moves over a pattern (as shown in the book)
#   and stores samples of one of the ground proximity sensors
# On a second pass, the top LEDs are lit
#   if an edge is detected using a digital derivative filter

# Experiment with the number of samples, the threshold,
#   the timer period and the sensor scale factors!!!

# Buttons:
#   Center:   start data collection (and stop)
#   Forward:  start second pass
#   Backward: apply derivative filter

SAMPLES = 20        # the number of samples taken
SAMPLES_NO_EDGES = 18 # for applying filters

# Pixel array: a for input, b for processed pixels
a = [0]*20    # Can't use variable here
b = [0]*18

power        = 100 # Motor power
scale1       = 30  # Sensor scale factors
scale2       = 120
period       = 120 # Timer period
threshold    = 30  # Threshold for detection
state        = 0   # 0 = stop, 1 = first pass, 2 = second pass
sum          = 0   # For computing histogram
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
  global threshold, timer_period, a
  if button_center == 0:
      if state == 0:
        i = 0
        nf_math_fill(a,0)
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

# Apply filter
# Be careful of edges of the sample array
# Result in b so changing a[i] doesn't affect a[i+1]
@onevent
def button_backward():
  global b
  if button_backward == 0:
      nf_math_fill(b,0)
      for j in range(1,SAMPLES_NO_EDGES+1):
         b[j] = (-a[j-1] + a[j+1]) 

# First pass timer event handler
@onevent
def timer0():
  global a
  if state == 0: return
  if i >= SAMPLES:
    stop()
    return
  a[i] = (prox_ground_delta[0] * scale1) // scale2
  i += 1

# Second pass timer event handler
# Turn LED on // off if abs derivative is above a threshold
@onevent
def timer1():
  global i
  if state != 2: return
  if i >= SAMPLES:
    stop()
    return
  if abs(b[i]) > threshold:
    nf_leds_top(32,32,32)
  else:
    nf_leds_top(0,0,0)
    i += 1
