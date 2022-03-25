# Activiy 2.5c

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Touch forward to start the robot
# Stop on an incline up or down

@onevent
def button_forward():
  global motor_left_target, motor_right_target
  motor_left_target = 200
  motor_right_target = 200

# Stop if pitching forward
@onevent
def acc():
  global motor_left_target, motor_right_target
  if abs(acc[1]) > 10:
    motor_left_target = 0
    motor_right_target = 0
