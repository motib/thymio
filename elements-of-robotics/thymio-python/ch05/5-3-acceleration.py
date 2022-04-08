# Activity 5.3

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# A rectangle of a known length made of black tape.
# Place the Thymio before the start tape and touch the center button 
# The Thymio approaches the start tape and if it reaches its 
# it moves rapidly.
# The side tapes ensure that the Thymio moves straight.
# Every accel ms the motor power is increased.
# After the motor power has run at maximum (500) for accel
# seconds, the motor stops.
# The circle leds display the motor power.

#   ||--------------------------------
#   ||
#   ||--------------------------------
#  Start

threshold  = 120   # for sensing the tapes
change     = 40    # percentage change of motor power for steering
accel      = 750   # time between power increases
motor_init = 200   # motor_init power

motor        = 0   # The base value of the motor power
motor_delta  = 100 # For maintaining straight path

state = 0          # 0 = off, 1 = find start of tape,
                   # 2 = skip start tape, 3 = drive straight
time  = 0          # Timer events

timer_period[0] = 100     # Time period for measuring time
timer_period[1] = accel   # Time period for accelerating

set_circle_leds()

# Stop the motors and set state to 0
def stop():
    global state, motor_left_target, motor_right_target
    state = 0
    motor_left_target  = 0
    motor_right_target = 0
    set_circle_leds()
    print(time)

# Drive straight between the tapes
def drive_straight():
    global motor_left_target, motor_right_target
    # If one of the ground sensors finds the tape
    #   turn the robot in the appropriate direction
    if  prox_ground_delta[0] < threshold:
        motor_left_target  = motor + motor_delta
        motor_right_target = motor - motor_delta
    elif  prox_ground_delta[1] < threshold:
        motor_left_target  = motor - motor_delta
        motor_right_target = motor + motor_delta
    else:
        # Otherwise, drive straight
        motor_left_target  = motor
        motor_right_target = motor
 
# Start tape found
def start_found():
    global state
    # change state to look for  of start tape
    if prox_ground_delta[0] < threshold and \
       prox_ground_delta[1] < threshold:
        state = 2

# End of start tape found
def end_of_start_found():
    global state, motor, motor_left_target, motor_right_target
    if prox_ground_delta[0] > threshold and \
       prox_ground_delta[1] > threshold:
        # change state to 3 (drive straight)
        motor = 0
        motor_left_target  = 0
        motor_right_target = 0
        set_circle_leds()
        state = 3
        timer = 0
  
# Proximity event occurs, call function depending on state
@onevent
def prox():
    global state
    # Check if the start tape has been found
    if  state == 1:
        start_found()
    # Check if the  of the start tape has been found
    elif state == 2:
        end_of_start_found()
    # Drive straight until stop tape sets state to 0
    elif state == 3:
        drive_straight()
  
# Timer0 event: increment the time counter
@onevent
def timer0():
    global time
    if state == 3: time += 1

# Timer1 event: increase power
@onevent
def timer1():
    global motor, time
    # When in state 3 (straight)
    if  state == 3:
        if motor < 500:
            motor = motor + 100
            set_circle_leds()
        elif motor == 500:
            stop()

# When center button released
@onevent
def button_center():
    global state, motor, motor_left_target, motor_right_target
    if  button_center == 0:
      # If off, set state to 1 (on) and creep forward to find start tape
        if  state == 0:
            state = 1
            # Creep forward to find the starting line
            motor = motor_init
            motor_left_target  = motor
            motor_right_target = motor
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
