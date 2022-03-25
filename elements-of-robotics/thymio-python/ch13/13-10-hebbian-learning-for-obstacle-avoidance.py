# Activity 13.10

# Copyright 2017, 2022 by Francesco Mondada and Moti Ben-Ari and Yves Piguet
# CreativeCommons BY-SA 3.0

# Hebbian learning for obstacle avoidance

# Remarks:
# - since button_center has the same effect as button_forward, couldn't it be used to start/stop?
# - toggle between on/off as long as black is detected
# - button events are emitted on touchdown and touchup (twice)

# Initially, the robot does not move or moves forward very slowly
# To train the robot to move forwards if an object is not
#   detected, touch the center button
# When the center / rear / left / right sensor detects your
#   finger, touch the back / front / right / left button
# Do the training one or more times
# The robot will update the ANN weights
#   and avoid an obstacle or move forwards if no obstacle

# Since all buttons are used, black paper or tape pushed
#   under a ground sensor starts and stops the robot
# Top leds indicate on or off

# Scale factors for sensors, outputs and motors
sensor_scale = 100
output_scale = 20
motor_scale  = 15

# Constant input to move forwards
constant_input = 25

# Threshold for start/stop with ground sensors
start_stop_threshold = 300

# Learning rate
alpha = 2

# Speed increment for each learning episode
speed = 10

# global variables
x = [0, 0, 0, 0, 0, 0, 0, 0]
w_left = [0, 0, 0, 0, 0, 0, 0, 0]
w_right = [0, 0, 0, 0, 0, 0, 0, 0]

# Time period (millisecconds) to compute motor outputs from inputs
timer_period[0] = 100

# Start in off state and not moving
state = False
leds_top = [0, 0, 0]
motor_left_target = 0
motor_right_target = 0

# Toggle start and stop with ground sensors
@onevent
def prox():
    global motor_left_target, motor_right_target, state
    if (prox_ground_delta[0] <= start_stop_threshold or \
        prox_ground_delta[1] <= start_stop_threshold):
        motor_left_target = 0
        motor_right_target = 0
        if state:
            nf_leds_top(0, 0, 0)
            state = False
        else:
            # Reset weights to zero
            for i in range(8):
                w_left[i] = 0
                w_right[i] = 0
            nf_leds_top(32, 32, 32)
            state = True

# Change weights according to Hebbian rule
def change_weights(y_left, y_right):
    for i in range(8):
        w_left[i] += alpha * y_left * x[i] // output_scale
        w_right[i] += alpha * y_right * x[i] // output_scale

# For each button change weights according to y_left, y_right

@onevent
def button_center():
    change_weights(speed, speed)

@onevent
def button_left():
    change_weights(-speed, speed)

@onevent
def button_right():
    change_weights(speed, -speed)

@onevent
def button_forward():
    change_weights(speed, speed)

@onevent
def button_backward():
    change_weights(-speed, -speed)

@onevent
def timer0():
    global motor_left_target, motor_right_target
    if state:
        # Read and scale inputs
        for i in range(7):
            x[i] = prox_horizontal[i] // sensor_scale
        x[7] = constant_input

        # Compute dot product of inputs and weights
        y = [0, 1]
        for i in range(8):
            y[0] += x[i] * w_left[i]
            y[1] += x[i] * w_right[i]

        # Scale and set motor speeds
        motor_left_target = y[0] // motor_scale
        motor_right_target = y[1] // motor_scale
