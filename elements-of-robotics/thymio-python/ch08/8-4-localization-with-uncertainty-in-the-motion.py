# Activity 8.4

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Localization with uncertainty in the motion
# See Section 8.5 of Elements of Robotics

LED = 32        # scale factor for displaying beliefs in leds
THRESHOLD = 250 # value below black is detected
P_HIT = 9       # probability of detecting black if on black
                #   or white if on white
P_MISS = 1      # probability of detecting black if on white
                #   or white if on black
P_0 = 1
P_1 = 8
P_2 = 1
MOTOR = 200
TIMER = 1600

# The world: 2 black, 2 white, 3 black, 1 white
world  = [1, 1, 0, 0, 1, 1, 1, 0]

# Beliefs where the black squares are
beliefs = [0,0,0,0,0,0,0,0]

state  = 0  # 0 = sense, 1 = move
hit    = 0  # 1 = on black, 0 = on white
sum    = 0  # Sum of beliefs for normalization

# Temporary array for computing motion with uncertainty
save = [0,0,0,0,0,0,0,0]

# Display the beliefs in the circle leds
def display_beliefs():
    nf_leds_circle( \
      beliefs[0]//LED, beliefs[1]//LED, beliefs[2]//LED, beliefs[3]//LED, \
      beliefs[4]//LED, beliefs[5]//LED, beliefs[6]//LED, beliefs[7]//LED)

# Initialize if center button is touched
@onevent
def button_center():
  global motor_left_target, motor_right_target, state
  if button_center == 0:
    motor_left_target = 0
    motor_right_target = 0
    nf_math_fill(beliefs, 1000//8)
    display_beliefs()
    state = 0

# Touch button forward to start
@onevent
def button_forward():
  global motor_left_target, motor_right_target, state, timer_period
  if button_forward == 0:
    if state == 0:
      state = 1
      display_beliefs()
      timer_period[0] = TIMER
      motor_left_target = MOTOR
      motor_right_target = MOTOR
    else:
      state = 0
      motor_left_target = 0
      motor_right_target = 0  

# Normalize
def normalize():
  global sum
  sum = 0
  for i in range(8):
    sum += beliefs[i]

  for  i in range(8):
    beliefs[i] = math_muldiv(beliefs[i], 1000, sum)

# Sense
def sense():
  global hit
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
  normalize()

# Move right cyclic with uncertainty 0, 1, 2 positions
def move():
  # Save current beliefs and initialize beliefs to 0
  nf_math_copy(save, beliefs)
  nf_math_fill(beliefs, 0)

  # From positions 0,1,2, the robot can move to 2
  # ...
  # From positions 7,8=0,9=1, the robot can move to 1
  for i in range(2,10):
    temp = math_muldiv(save[(i-2)%8], P_2, 10)
    beliefs[i%8] += temp
    temp = math_muldiv(save[(i-2)%8], P_1, 10)
    beliefs[i%8] += temp
    temp = math_muldiv(save[(i-2)%8], P_0, 10)
    beliefs[i%8] += temp
  normalize()

@onevent
def timer0():
  global state
  if state == 1:
    sense()
    move()
    display_beliefs()
    nf_sound_freq(1000,10)
