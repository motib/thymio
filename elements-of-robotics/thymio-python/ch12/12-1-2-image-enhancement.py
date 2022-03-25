# Activities 12.1, 12.2

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Image enhancement: smoothing and histogram manipulation

# This program implements two algorithms for image enhancement
# The Thymio moves over a pattern (as shown in the book)
#   and stores samples of one of the ground proximity sensors
# On a second pass, the top LEDs are lit
#   if the light is below a threshold

# Smoothing: an averaging filter is applied
# Histogram manipulation: a specified fraction of the bins
#   is used to determine the threshold

# Experiment with the number of samples, the threshold,
#   the timer period, the histogram fraction and
#   the sensor scale factors!!!

# Buttons:
#   Center:   start data collection (and stop)
#   Forward:  start second pass
#   Backward: apply averaging filter
#   Left:     compute threshold from histogram

SAMPLES = 32        # the number of samples taken
SAMPLES_NO_EDGES = 30 # for applying filters

# Pixel array: a for input, b for processed pixels
a = [0]*32    # Can't use variable here
b = [0]*32

# Histogram: 10 bins for intensities normalized to 0--99
hist = [0]*10

power        = 100 # Motor power
scale1       = 30  # Sensor scale factors
scale2       = 120
fraction     = 40  # Histogram fraction
period       = 120 # Timer period
thresh_fixed = 50  # Fixed threshold
threshold    = 0   # Fixed threshold or after histogram
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
  global threshold, timer_period
  if button_center == 0:
      if state == 0:
        i = 0
        threshold = thresh_fixed
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

# Apply averaging filter
# Be careful of edges of the sample array
# Result in b so changing a[i] doesn't affect a[i+1]
@onevent
def button_backward():
  global b
  if button_backward == 0:
      # Copy a to b for compatibility with timer1 event handler
      nf_math_copy(b,a)
      for j in range(1,SAMPLES_NO_EDGES+1):
         b[j] = (a[j-1] + a[j] + a[j+1]) // 3
  

# Compute the histogram
@onevent
def button_left():
  global a, b, hist, sum, i, threshold
  if button_left == 0:
      # Copy a to b for compatibility with timer1 event handler
      nf_math_copy(b,a)
      # Zero bin array
      nf_math_fill(hist,0)

      # Compute histogram
      for i in range(1,SAMPLES+1):
         # Sample values over 100 placed in last bin
         if a[i-1] > 100: a[i-1] = 99 
         # Divide value by 10 to get bin number
         hist[a[i-1] // 10] += 1

      # Compute sum of bins, stopping when the
      #   sum is greater than a specified fraction
      sum = 0
      i = 0
      while sum < SAMPLES*10 // fraction:
         sum += hist[i]
         i += 1
      
      # Use the index of that bin to set the threshold
      threshold = i * 10 + 5

# Timer for first pass
@onevent
def timer0():
  global a, b, i
  if state == 0: return 
  # Stop when sample array is filled
  if i >= SAMPLES:
    stop()
    # Copy a to b for compatibility with timer1 event handler
    nf_math_copy(b,a)
    return
  
  # Scale the sample and store in the array
  a[i] = (prox_ground_delta[0] * scale1) // scale2
  i += 1

# Timer for second pass
@onevent
def timer1():
  global i
  if state != 2: return
  if i >= SAMPLES:
      stop()
      return 
  # Turn LED on // off if below // above threshold
  if b[i] < threshold:
  	 nf_leds_top(32,32,32)
  else:
  	 nf_leds_top(0,0,0)
  i += 1
