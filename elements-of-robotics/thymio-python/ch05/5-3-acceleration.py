# Activity 5.3

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# A rectangle of a known length made of black tape.
# Place the Thymio before the start tape and touch the center button 
# The Thymio approaches the start tape and if it reaches its 
# it moves rapidly.
# The side tapes ensure that the Thymio moves straight.
# Every ACCEL ms the motor power is increased.
# After the motor power has run at maximum (500) for ACCEL
# seconds, the motor stops.
# The circle leds display the motor power.

#   ||--------------------------------||
# * ||                                ||
#   ||--------------------------------||
#  Start                             End

THRESHOLD = 120  # for sensing the tapes
CHANGE = 40      # percentage change of motor power for steering
ACCEL = 500      # time between power increases
MOTOR = 300      # motor power

motor  = 0        # The base value of the motor power
motor_change = 0  # The amount to change if approaching and turning

state = 0      # 0 = off, 1 = find start of tape, 2 = skip start tape, 3 = drive straight

time = 0       # Timer events

timer_period[0] = 100  # 100 ms = 0.1 seconds
timer_period[1] = ACCEL
motor = MOTOR
motor_change = (motor * CHANGE)//100
nf_leds_circle(0,0,0,0,0,0,0,0)

# Set the circle leds to indicate the motor power
def set_circle_leds():
  if motor//100==0: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor//100==1: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if motor//100==2: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if motor//100==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if motor//100==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if motor//100==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Stop the motors and set state to 0
def stop():
  global state, motor, motor_change, motor_left_target, motor_right_target
  state = 0
  motor = 0
  motor_change = (motor * CHANGE)//100
  motor_left_target  = motor
  motor_right_target = motor
  set_circle_leds()

# When center button released
@onevent
def button_center():
  global state, motor, motor_change, motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, set state to 1 (on) and creep forward to find start tape
    if  state == 0:
      state = 1
      # Creep forward to find the starting line
      motor = MOTOR
      motor_change = (motor * CHANGE)//100
      motor_left_target  = motor - motor_change
      motor_right_target = motor - motor_change
    #   else: if state is on, stop
    else:
      stop()

# Drive straight between the tapes
def drive_straight():
  global motor_left_target, motor_right_target
  # If one of the ground sensors finds the tape
  #   turn the robot in the appropriate direction
  if  prox_ground_delta[0] < THRESHOLD:
    motor_left_target  = motor + motor * motor_change
    motor_right_target = motor - motor * motor_change
  elif  prox_ground_delta[1] < THRESHOLD:
    motor_left_target  = motor - motor * motor_change
    motor_right_target = motor + motor * motor_change
  else:
  # Otherwise, drive straight
     motor_left_target  = motor
     motor_right_target = motor
 
# Start tape found
def start_found():
  global state
  # Change state to look for  of start tape
  if  prox_ground_delta[0] < THRESHOLD and \
      prox_ground_delta[1] < THRESHOLD:
    state = 2

# End of start tape found
def _of_start_found():
  global state, motor, motor_change, motor_left_target, motor_right_target
  if  prox_ground_delta[0] > THRESHOLD and \
      prox_ground_delta[1] > THRESHOLD:
    state = 3
    # Change state to 3 (straight)
    state = 3
    # Initialize motor power to 0
    motor = 0
    motor_change = (motor * CHANGE)//100
    motor_left_target  = motor
    motor_right_target = motor
    set_circle_leds()

# Proximity event occurs, defroutine deping on the state
@onevent
def prox():
  global state
  # Check if the start tape has been found
  if  state == 1:
    start_found()
  # Check if the  of the start tape has been found
  elif state == 2:
    _of_start_found()
  # Drive straight until stop tape sets state to 0
  elif state == 3:
    drive_straight()
  
# Timer0 event: increment the time counter
@onevent
def timer0():
  global time
  if state == 3: time += 1

# Timer1 event
@onevent
def timer1():
  global motor, motor_change, time
  # When in state 3 (straight)
  if  state == 3:
    # If motor = 0, initialize time counter and set motor to 100
    if  motor == 0:
      time = 0
      motor = 100
    # If motor < 500, increment by 100
    elif motor < 500:
      motor = motor + 100
    # If motor == 500, stop
    elif motor == 500:
      stop()
    motor_change = (motor * CHANGE)//100
    set_circle_leds()
