# Activity 5.9

# Copyright 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Combined effect of odometry errors

# This program has the robot move about 1 m rather than 2

# Adjuct the motor powers and periods to implement
#   the requirements

# Center button to start / stop
# Left button for mode 1: straight, then 360
# Right button for mode 2: 360, then straight
# Forward button for mode 3: straight, 180, back
# Mode 4 for the return drive in mode 3

# Top leds  show modes: 1=red, 2=green, 3=blue

period_straight  = 8000  # period to go 2 m
period_360       = 4600  # period to turn 360
period_180       = 2300  # period to turn 180

motor_straight = 400    # motor power for going straigh
motor_turn     = 200    # change to L/R motors to turn

mode           = 0      # Three modes
state          = False  # False = off, True = on

timer_period[0] = 0
set_top_leds()

# Stop everything
def stop():
    global state, timer_period
    global motor_right_target, motor_left_target
    state = False
    motor_left_target = 0
    motor_right_target = 0
    timer_period[0] = 0

# Check if tape found and process according to state
@onevent
def timer0():
    global state, timer_period, mode
    global motor_left_target, motor_right_target
    if not state: return
    if mode == 1:
        if timer_period[0] == period_straight:
            timer_period[0] = period_360
            motor_left_target  =  motor_turn
            motor_right_target = -motor_turn
        else:
            stop()
    elif mode == 2:
        if timer_period[0] == period_360:
            timer_period[0] = period_straight
            motor_left_target  = motor_straight
            motor_right_target = motor_straight
        else:
            stop()
    elif mode == 3:
        if timer_period[0] == period_straight:
            timer_period[0] = period_180
            motor_left_target  =  motor_turn
            motor_right_target = -motor_turn
            mode = 4
            set_top_leds()
        else:
            stop()
    elif mode == 4:
        if timer_period[0] == period_180:
            timer_period[0] = period_straight
            motor_left_target  = motor_straight
            motor_right_target = motor_straight
        else:
            stop()

@onevent
def button_center():
    global state, motor_left_target, motor_right_target
    if  button_center == 0:
        if mode == 0:
            print("Set mode (1,2,3) before running")
            return
        if not state:
            state = True
            set_top_leds()
            if mode == 1:
                timer_period[0] = period_straight
                motor_left_target  = motor_straight
                motor_right_target = motor_straight
            elif mode == 2:
                timer_period[0] = period_360
                motor_left_target  =  motor_turn
                motor_right_target = -motor_turn
            elif mode == 3:
                timer_period[0] = period_straight
                motor_left_target  = motor_straight
                motor_right_target = motor_straight
        else:
            stop()

# Set mode 1
@onevent
def button_left():
    global mode
    if button_left == 0: mode = 1

# Set mode 2
@onevent
def button_right():
    global mode
    if button_right == 0: mode = 2

# Set mode 3
@onevent
def button_forward():
    global mode
    if button_forward == 0: mode = 3

# Set top leds: red if found but green if going backwards
def set_top_leds():
    global mode
    if mode == 0: nf_leds_top(0,0,0)
    if mode == 1: nf_leds_top(32,0,0)
    if mode == 2: nf_leds_top(0,32,0)
    if mode == 3: nf_leds_top(0,0,32)
    if mode == 4: nf_leds_top(32,32,32)
