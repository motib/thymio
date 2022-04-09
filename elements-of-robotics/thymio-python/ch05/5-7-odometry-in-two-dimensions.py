# Activity 5.7

# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Odometry in two dimensions

run_time = 30     # Duration of run (tenths of seconds)
baseline = 95     # Distance between wheels (millimeters)
left     = 200    # Power setting of left wheel
right    = 300    # Power setting of right wheel
speed    = 32     # Speed of robot per 100 power setting (*10)

state    = False  # False = off, True = on
time     = 0      # Counter of tenths of seconds

# Set timer to expire every tenth of a second
timer_period[0] = 100

def stop():
    global state, motor_left_target, motor_right_target
    state = False
    motor_left_target = 0
    motor_right_target = 0

# Compute the odometry
def odometry():
    # dleft, dright: distance traveled by the left/right wheel
    # dcenter: distance traveled by the center of the robot
    # theta: change of heading
    # dx, dy: change of x, y
    # tcos, tsin: cos and sin of theta
    
    # Distances traveled by left and right motors
    # Center distance is the average of the left and right
    # Factor is:
    #    100 for motor powers
    #    10  for power to speed (3.2 cm/sec)
    #    10  for time in tenths of a second
    
    dleft =  math_muldiv(
        motor_left_speed,  speed*run_time, 100*10*10)
    dright = math_muldiv(
        motor_right_speed, speed*run_time, 100*10*10)
    dcenter = (dleft+dright) // 2
    print('dleft =', dleft, ', dright =', dright,
          ', dcenter = ',dcenter)
    
    # Change of heading and its sine and cosine
    # Factor is:
    #    10 for axle width in mm
    #    100 for hundredths of radians
    theta = ( (dright-dleft) * 10*100) // baseline
    
    # The parameter to the trigonometric functions is in the
    #    range -32768--32767
    #    representing the range -pi to pi radians
    # Multiply the angle by 100 so range of positive 0--314
    #    becomes 0--31400 approximately
    #    the range of the positive angles in 16-bits
    tcos = math_cos(theta*100)
    tsin = math_sin(theta*100)
    print('theta =', theta, ', tcos =', tcos, ', tsin =', tsin)
    
    # Compute the change in the x- and y-positions:
    #    Divide by 32767 because the result
    #    of the trigonometric functions
    #    is in the range -32768--32767
    dx = math_muldiv(dcenter, -tsin, 32767)
    dy = math_muldiv(dcenter,  tcos, 32767)
    print('dx =', dx, ', dy =', dy)

# Every tenth of a second, increment the counter time
# When time = run_time, compute the odometry and stop the motors
@onevent
def timer0():
    global state, time, motor_left_target, motor_right_target
    if  not state: return
    time += 1
    if  time == run_time:
        odometry()
        stop()

# Touch center button to start and stop run
@onevent
def button_center():
    global state, motor_left_target, motor_right_target, time
    if button_center == 0:
        if not state:
            state = True
            time = 0
            motor_left_target =  left
            motor_right_target = right
        else:
            stop()
