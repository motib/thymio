# Activity 3-18b

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Touch center button to start and stop
# Motors connected directly to sensors
#   so that the robot turns towards the object

state = 0

@onevent
def button_center():
  global motor_left_target, motor_right_target, state
  if  button_center == 0:
    state = 1 - state
    motor_left_target  = 0
    motor_right_target = 0

@onevent
def prox():
  global motor_left_target, motor_right_target, state
  if  state != 0:
    motor_left_target = prox_horizontal[4] // 5
    motor_right_target = prox_horizontal[0] // 5
