# Activity 3.10
# Also for 3.11, 3.12

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Line following with two sensors
# Left, right buttons set motor power
# Center button to start, stop

CHANGE = 50       # percentage change of motors for steering
INCREMENT = 100   # change in motor power for each touch of button
THRESHOLD = 300   # for sensing tape
motor = 0
motor_change = 0
state = 0
nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_top(0,0,0)

# Set the circle leds to indicate the motor power
def set_circle_leds():
  if motor//100==0: nf_leds_circle(0,0,0,0,0,0,0,0)
  if motor//100==1: nf_leds_circle(32,0,0,0,0,0,0,0)
  if motor//100==2: nf_leds_circle(32,32,0,0,0,0,0,0)
  if motor//100==3: nf_leds_circle(32,32,32,0,0,0,0,0)
  if motor//100==4: nf_leds_circle(32,32,32,32,0,0,0,0)
  if motor//100==5: nf_leds_circle(32,32,32,32,32,0,0,0)

# Left and right button event handlers
#   Increase or decrease motor power within 0-500
@onevent
def button_left():
  global motor, motor_change
  if  button_left == 0:
    motor = motor - INCREMENT
    if  motor < 0: motor = 0
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

@onevent
def button_right():
  global motor, motor_change
  if  button_left == 0:
    motor = motor + INCREMENT
    if  motor > 500: motor = 0
    motor_change = (motor * CHANGE)//100
    set_circle_leds()

# When center button released
#   If off, set state to 1 (on) and dirve forwards
#   else if state is on, stop the motors
@onevent
def button_center():
  global state, motor_left_target, motor_right_target, motor_change
  if  button_center == 0:
    if  state == 0:
      state = 1
      motor_left_target  = motor
      motor_right_target = motor
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0

# Proximity event occurs, turn if necessary
@onevent
def prox():
  global motor_left_target, motor_right_target
  if  state != 0:
      # If both sensors detect the tape, go straight
      if  prox_ground_delta[0] < THRESHOLD and \
          prox_ground_delta[1] < THRESHOLD:
        motor_left_target  = motor
        motor_right_target = motor
        nf_leds_top(32,0,0)
      # If left detects and right doesn't, turn left
      elif prox_ground_delta[0] < THRESHOLD and \
             prox_ground_delta[1] >= THRESHOLD:
         motor_left_target  = motor - motor_change
         motor_right_target = motor + motor_change
         nf_leds_top(0, 0, 32)
      # If right detects and left doesn't, turn right
      elif prox_ground_delta[0] >= THRESHOLD and \
             prox_ground_delta[1] < THRESHOLD:
        motor_left_target  = motor + motor_change
        motor_right_target = motor - motor_change
        nf_leds_top(0, 32, 0)
      else:
        motor_left_target  = 0
        motor_right_target = 0
        nf_leds_top(32, 32, 32)
