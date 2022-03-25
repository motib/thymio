# Activity 5.13

# NOT TESTED - MBA

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

@onevent
def rc5():
    global motor_left_target, motor_right_target
    if rc5_command == 1:
      motor_left_target = 250
    if  rc5_command == 7:
      motor_left_target = -250
    if  rc5_command == 4:
      motor_left_target = 0
    if  rc5_command == 3:
      motor_right_target = 250
    if rc5_command == 9:
      motor_right_target = -250
    if  rc5_command == 6:
      motor_right_target = 0
