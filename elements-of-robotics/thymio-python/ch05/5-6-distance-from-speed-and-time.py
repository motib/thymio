# Activity 5.6

# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Estimate distance traveled for a fixed time
# Run for several values of motor
# Motor power set by left/right buttons
# Start/stop by center button

motor = 0      # motor target speed
time  = 500    # time between samples in milliseconds
count = 8      # number of samples
scale = 600    # set to a value that gives distance in cm

state   = 0     # 0 = off, 1 = on
samples = 0     # Counter for sampling

set_circle_leds()

timer_period[0] = time

# Stop the motors and set state to 0
def stop():
    global state, motor_left_target, motor_right_target
    state = 0
    motor_left_target = 0
    motor_right_target = 0
    set_circle_leds()

# On timer event, sample speed
# Terminate if count samples have been taken
@onevent
def timer0():
    global state, deltaD, samples
    if  state == 0: return
    if  samples < count:
        samples += 1
    else:
        distance = (motor*count*time)//scale
        print(distance)
        stop()

# Touch center button to start and stop
@onevent
def button_center():
    global state, samples
    global motor_left_target, motor_right_target
    if  button_center == 0:
        if  state == 0:
            samples = 0
            motor_left_target = motor
            motor_right_target = motor
            state = 1
        else:
            stop()

# Set the circle leds to indicate the motor power
def set_circle_leds():
    if motor // 100 == 0: nf_leds_circle(0,0,0,0,0,0,0,0) 
    if motor // 100 == 1: nf_leds_circle(32,0,0,0,0,0,0,0) 
    if motor // 100 == 2: nf_leds_circle(32,32,0,0,0,0,0,0) 
    if motor // 100 == 3: nf_leds_circle(32,32,32,0,0,0,0,0) 
    if motor // 100 == 4: nf_leds_circle(32,32,32,32,0,0,0,0) 
    if motor // 100 == 5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Button event handlers
#   Left//right: increase or decrease motor power within 0-500
@onevent
def button_left():
    global motor
    if  button_left == 0:
        motor = motor - 100
        if  motor < 0: motor = 0 
        set_circle_leds()

@onevent
def button_right():
    global motor
    if  button_right == 0:
        motor = motor + 100
        if  motor > 500: motor = 500 
        set_circle_leds()
