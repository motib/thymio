# Activity 3.6

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# When the robot detects an object, it moves forwards, colliding with the object
# When it does not detect an object, it turns to the left

state = 0

@onevent
def prox():
    global motor_left_target, motor_right_target
    global state
    if state == 0: return
    if prox_horizontal[2] > 2000:
        motor_left_target = 200
        motor_right_target = 200
    if prox_horizontal[2] < 1000:
        motor_left_target = -200
        motor_right_target = 200

@onevent
def button_center():
    global state
    global motor_left_target, motor_right_target
    if button_center == 0:
        state = 1 - state
        motor_left_target = 0
        motor_right_target = 0
