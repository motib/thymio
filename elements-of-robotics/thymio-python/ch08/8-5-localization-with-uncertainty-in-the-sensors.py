# Activity 8.3

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Localization with uncertainty in the sensors
# See Section 8.4 of Elements of Robotics

LED = 32        # scale factor for displaying beliefs in leds
THRESHOLD = 250 # value below black is detected
P_HIT = 9       # probability of detecting black if on black
                #   or white if on white
P_MISS = 1      # probability of detecting black if on white
                #   or white if on black

# The world: 2 black, 2 white, 3 black, 1 white
world  = [1, 1, 0, 0, 1, 1, 1, 0]

# Beliefs where the black squares are
beliefs = [0,0,0,0,0,0,0,0]

state  = 0  # 0 = sense, 1 = move
hit    = 0  # 1 = on black, 0 = on white
sum    = 0  # Sum of beliefs for normalization

# Display the beliefs in the circle leds
def display_beliefs():
    nf_leds_circle(
      beliefs[0]//LED, beliefs[1]//LED, beliefs[2]//LED, beliefs[3]//LED,
      beliefs[4]//LED, beliefs[5]//LED, beliefs[6]//LED, beliefs[7]//LED)

# Initialize if center button is touched
@onevent
def button_center():
  global state, beliefs
  if button_center == 0:
    nf_math_fill(beliefs, 1000//8)
    display_beliefs()
    state = 0

# Sense
def sense():
  global hit, sum, beliefs
  # Check if on black (1) or not (0)
  if  prox_ground_delta[0] < THRESHOLD and \
      prox_ground_delta[1] < THRESHOLD:
    hit = 1
  else:
    hit = 0

  # If hit matches world at each position
  #   multiply the beliefs by the hit//miss probabilities
  for i in range(8):
    if  (hit == 1 and world[i] == 1) or \
        (hit == 0 and world[i] == 0):
      beliefs[i] = math_muldiv(beliefs[i], P_HIT, 10)
    else:
      beliefs[i] = math_muldiv(beliefs[i], P_MISS, 10)

  # Compute the sum of the beliefs
  sum = 0
  for i in range(8):
    sum += beliefs[i]

  # Normalize
  for i in range(8):
    beliefs[i] = math_muldiv(beliefs[i], 1000, sum)

# Move right cyclic
def move():
  global beliefs
  temp = beliefs[7]
  for i in range(7,-1,-1):
    beliefs[i] = beliefs[i-1]
  beliefs[0] = temp

# Touch button forward to repeat sense -> move -> ...
@onevent
def button_forward():
  global state
  if button_forward == 0:
    if state == 0:
      sense()
      state = 1
    else:
      move()
      state = 0
    display_beliefs()
