# Activity 3.5

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# When an object approaches the robot from behind
# it runs away until it is out of range.

state = 0

@onevent
def prox():
    global motor_left_target, motor_right_target
    global state
    if state == 0: return
    if (prox_horizontal[5] > 1000) and (prox_horizontal[6] > 1000):
        motor_left_target = 300
        motor_right_target = 300
    elif (prox_horizontal[5] < 1000) and (prox_horizontal[6] < 1000):
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
