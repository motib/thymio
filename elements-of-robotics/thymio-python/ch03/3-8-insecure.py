# Activity 3.8

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# If an object is not detected to the left of the robot,
#    set the right motor to rotate forwards and set the left motor off.
# If an object is detected to the left of the robot,
#   set the right motor off and set the left motor to rotate forwards.

state = 0

@onevent
def prox():
    global motor_left_target, motor_right_target
    global state
    if state == 0: return
    if prox_horizontal[0] < 1000:
        motor_left_target = 0
        motor_right_target = 400
    elif prox_horizontal[0] > 2000:
        motor_left_target = 400
        motor_right_target = 0

@onevent
def button_center():
    global state
    global motor_left_target, motor_right_target
    if button_center == 0:
        state = 1 - state
        motor_left_target = 0
        motor_right_target = 0
        