# Activity 5.5

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Full power is applied to the robot if the center button is touched

state = 0    #   0 = off, 1 = drive straight
motor_left_target = 0
motor_right_target = 0

# Stop the motors and set state to 0
def stop():
  global state, motor_left_target, motor_right_target
  state = 0
  motor_left_target  = 0
  motor_right_target = 0

# When center button released
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, set state to 1 (on) and creep forward to find start tape
    if  state == 0:
      state = 1
      motor_left_target  = 500
      motor_right_target = 500
    #   else: if state is on, stop
    else:
      stop()
