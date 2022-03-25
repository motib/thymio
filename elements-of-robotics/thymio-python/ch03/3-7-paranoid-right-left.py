# Activity 3.7

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# When an object is detected in front of the robot,
#    the robot moves forwards.
# When an object is detected to the right of the robot,
#    the robot turns right.
# When an object is detected to the left of the robot,
#    the robot turns left.
# When no object is detected the robot does not move.

state = 0

@onevent
def prox():
    global motor_left_target, motor_right_target
    global state
    if state == 0: return
    if prox_horizontal[2] > 2000:
        motor_left_target = 200
        motor_right_target = 200
    elif prox_horizontal[0] > 2000:
        motor_left_target = -200
        motor_right_target = 200
    elif prox_horizontal[4] > 2000:
        motor_left_target = 200
        motor_right_target = -200
    elif prox_horizontal[0] < 1000 and prox_horizontal[2] < 1000 \
            and prox_horizontal[4] < 1000:
        motor_left_target = 0
        motor_right_target = 0

@onevent
def button_center():
    global state
    global motor_left_target, motor_right_target
    if button_center == 0:
        state = 1 - state
        motor_left_target = 0
        motor_right_target = 0
