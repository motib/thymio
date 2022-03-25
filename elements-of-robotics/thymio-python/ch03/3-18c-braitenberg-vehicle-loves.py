# Activity 3.18c

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Touch center button to start and stop
# Motors connected directly to sensors but negated
#   so that the robot turns towards the object

state = 0

@onevent
def button_center():
  global motor_left_target, motor_right_target, state
  if  button_center == 0:
    state = 1 - state
    motor_left_target  = 0
    motor_right_target = 0

# Proximity event handler:
#   set left/right motor speeds to value of negative right/left sensors
@onevent
def prox():
  global motor_left_target, motor_right_target, state
  MOTOR_BIAS = 250
  if  state != 0:
    motor_left_target = MOTOR_BIAS - prox_horizontal[0] // 5
    motor_right_target = MOTOR_BIAS - prox_horizontal[4] // 5
