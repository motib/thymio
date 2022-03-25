# Activity 11.1

# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Fuzzy logic algorithm for approaching

# See Chapter 11 of "Elements of Robotics"

FAR_LOW = 3000
FAR_HIGH = 3600
CLOSING_LOW = 3300
CLOSING_HIGH = 4300
NEAR_LOW =4100
NEAR_HIGH = 4350

premises = [0,0,0]         # Certainties of premises: far, closing, near
consequents = [0,0,0,0,0]   # Certainties of consequents: very fast, fast, cruise, slow, stop
centers = [4, 3, 2, 1, 0]  # Centers of output membership functions

state = 0      # The state 0 = off, 1 = on
height = 0     # Height (certainty) of an output membership function
width =  200   # Width of triangular membership function
area = 0       # Area under a consequent membership function
mid = 0        # Middle of membership function

accum_weighted = 0 # Accumulated weighted area over all rules
accum_areas    = 0 # Accumulated area over all rules
crisp          = 0 # Crisp output

# Stop the algorithm and the motors
def stop():
  global state, motor_left_target, motor_right_target
  state = 0
  motor_left_target  = 0
  motor_right_target = 0

# Forward button to start
@onevent
def button_forward():
  global state
  nf_leds_circle(0,0,0,0,0,0,0,0)
  state = 1

# Center button to stop
@onevent
def button_center():
  stop()

# Fuzzification of the sensor input value
#   Outputs for each linguistic variable are in "premises"
#   Input membership functions: far, closing, near
#   Certainties are scaled in the range 0 .. 100
def fuzzify():
  global mid, premises
  # Store center sensor value in a variable with a short name
  value = prox_horizontal[2]

  # "far" uses a saturated membership function
  if value <= FAR_LOW: premises[0] = 100
  elif value >= FAR_HIGH: premises[0] = 0
  else: 
    temp = math_muldiv((value - FAR_LOW), 100, (FAR_HIGH - FAR_LOW))
    premises[0] = 100 - temp

  # "closing" uses a triangular membership function
  mid = CLOSING_LOW + (CLOSING_HIGH-CLOSING_LOW)//2
  if value < CLOSING_LOW: premises[1] = 0
  elif value > CLOSING_HIGH: premises[1] = 0
  elif value < mid:
    temp = math_muldiv((value - CLOSING_LOW), 100, (mid - CLOSING_LOW))
    premises[1] = temp
  else:
    temp = math_muldiv((value - mid), 100, (CLOSING_HIGH - mid))
    premises[1] = 100 - temp

  # "near" uses a saturated membership function
  if value >= NEAR_HIGH: premises[2] = 100
  elif value <= NEAR_LOW: premises[2] = 0
  else:
    temp = math_muldiv((value - NEAR_LOW), 100, (NEAR_HIGH - NEAR_LOW))
    premises[2] = temp

# Apply inference rules
def apply_rules():
  global consequents
  nf_math_fill(consequents, 0)

# Rule 1: if far: motor = very fast
  if premises[0] != 0:
    consequents[0] = premises[0]

  # Rule 2: if far and closing: motor = fast
  if premises[0] != 0 and premises[1] != 0:
    consequents[1] = math_min(premises[0], premises[1]) 

  # Rule 3: if closing: motor = cruise
  if premises[1] != 0:
    consequents[2] = premises[1]

  # Rule 4: if closing and near: motor = slow
  if premises[1] != 0 and premises[2] != 0:
    consequents[3] = math_min(premises[1], premises[2])

  # Rule 5: if near: motor = stop
  if premises[2] != 0:
    consequents[4] = premises[2]

#  area = width * (height - height*height//2) 
def compute_area():
   global area
   area = math_muldiv(width, height, 1)
   temp = math_muldiv(area, height, 200)
   area -= temp
   area //= 100

# Defuzzify by computing the center of gravity
#   Compute sum of areas of fuzzy output membership functions
#     weighted by the centers of the functions
#   Divide by sum of unweighted areas
def defuzzify():
  global crisp, accum_areas, accum_weighted, height
  accum_weighted = 0
  accum_areas = 0
  for  i in range(5):
      height = consequents[i]
      compute_area()
      accum_weighted += centers[i] * area
      accum_areas += area
  if accum_areas == 0: accum_areas = 1 

  # Compute crisp output value
  crisp = math_muldiv(accum_weighted, 100, accum_areas)

# Proximity event handler
@onevent
def prox():
  global motor_left_target, motor_right_target
  if state == 0: return
  fuzzify()
  apply_rules()
  nf_leds_circle( \
      premises[0]//3, premises[1]//3, premises[2]//3, \
      consequents[0]//3, consequents[1]//3, consequents[2]//3, \
      consequents[3]//3, consequents[4]//3)
  defuzzify()
  motor_left_target  =  crisp
  motor_right_target =  crisp
