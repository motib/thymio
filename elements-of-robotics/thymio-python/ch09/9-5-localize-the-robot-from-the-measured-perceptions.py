# Activity 9.5

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Demonstrate localization against a map
# The map has three objects in a line
# Touch the backwards button to initialize
# Collect database of samples for each of 15 poses of the robot
# Positions (0,0), (0,1), (0,-1), (1,0), (-1,0)
#   and for each position orientations -30, 0, 30
# Touch the center button to record the samples
#
# Place the robot at one of the 15 poses and touch the
#   forward button. The button and circle leds indicate
#   the best fit for position and orientation
#
# Tip: After recording the database of samples,
#        save it using Export memories content in the File menu
#      You can Import it so you don't have to regenerate the database

# Collect values for the left, center and right sensors
#   for each of the 15 poses
left_samples = [0]*15
center_samples = [0]*15
right_samples = [0]*15

# Save the sensors values for the pose to be tested
left = 0
right = 0
center = 0

# Compute the similarities of the test sample with all the others
# Save index of the lowest value of the similarities
# The array is not needed but it is convenient to examine its values
similarity = [0]*15
best_similarity = 0
best_index = 0

# Index over poses
index = 0

# Sample order
# Index  position   rotate
#   0      0,0        -30
#   1      0,0          0
#   2      0,0        +30
#   3      1,0        -30
#   4      1,0          0
#   5      1,0        +30
#   6     -1,0        -30
#   7     -1,0          0
#   8     -1,0        +30
#   9      0,1        -30
#  10      0,1          0
#  11      0,1        +30
#  12     0,-1        -30
#  13     0,-1          0
#  14     0,-1        +30

nf_leds_buttons(0,0,0,0)
nf_leds_circle(0,0,0,0,0,0,0,0)

# Display the position of the best index in the button leds
#   and the orientation in the circle leds
def display_result():
    if   best_index <  3: nf_leds_buttons(32,32,32,32)
    elif best_index <  6: nf_leds_buttons(0,32,0,0)
    elif best_index <  9: nf_leds_buttons(0,0,0,32)
    elif best_index < 12: nf_leds_buttons(32,0,0,0)
    else:                 nf_leds_buttons(0,0,32,0)

    if   best_index % 3 == 0: nf_leds_circle(0,32,0,0,0,0,0,0)
    elif best_index % 3 == 1: nf_leds_circle(32,0,0,0,0,0,0,0)
    else:                     nf_leds_circle(0,0,0,0,0,0,0,32)

# Compute the similarity between the test sample
#   and each sample in the database
# The similarity is the sum of the absolute value
#   of the difference for each sensor
# Choose the best one
def find_best():
    global best_similarity, best_index, index
    best_similarity = 32000
    for index in range(15):
        similarity[index] = \
          abs (left-left_samples[index]) + \
          abs (center-center_samples[index]) + \
          abs (right-right_samples[index])
        if similarity[index] < best_similarity:
            best_similarity = similarity[index]
            best_index = index
    display_result()

# Button even handler
@onevent
def button_backward():
  global left_samples, center_sample, right_samples, index
  # Backward button: zero database and set index to zero
  if button_backward == 0:
    for index in range(15):
      left_samples[index] = 0
      center_samples[index] = 0
      right_samples[index] = 0
    index = 0

@onevent
def button_center():
  global left_samples, center_sample, right_samples, index
  # Center button: save the current values of the sensors
  #   at the current place in the database
  # Sensors 1,2,3 seem to work better than 0,2,4
  if button_center == 0: 
        left_samples[index] = prox_horizontal[1]
        center_samples[index] = prox_horizontal[2]
        right_samples[index] = prox_horizontal[3]
        index += 1
  
@onevent
def button_forward():
  global left, center, right, forward
  # Forward button: sample the sensors and find_best
  if button_forward == 0:
        left = prox_horizontal[1]
        center = prox_horizontal[2]
        right = prox_horizontal[3]
        find_best()
