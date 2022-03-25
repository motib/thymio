# Activity 6.3

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Proportional controller for approaching an object

TARGET = 4000       # Highest value of the proximity sensor
TARGET_ERROR = 500  # Stop if error is below this value
MOTOR = 400         # Power setting for the motor
GAIN_P = 6          # Power is error times gain
SCALE = 50          # Scale the error

# Center button to start and stop
# Robot approaches object detected by center sensor
# Motor power is displayed in the circle leds

state  = 0       # The state 0 = off, 1 = on
error  = 0       # Difference between sensor and target values
motor_power = 0  # Motor power setting deping on error

motor_left_target  = 0
motor_right_target = 0
nf_leds_circle(0,0,0,0,0,0,0,0)

def set_circle_leds():
  if motor_power//100==0: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor_power//100==1: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if motor_power//100==2: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if motor_power//100==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if motor_power//100==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if motor_power//100==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Stop the algorithm and the motors
def stop():
  global motor_left_target, motor_right_target
  global state
  state = 0
  motor_left_target  = 0
  motor_right_target = 0

# Center button event handler
@onevent
def button_center():
  global state
  if button_center == 0:
      if state == 0:
        state = 1
      else:
        stop()

# Proximity event handler
@onevent
def prox():
  global motor_left_target, motor_right_target
  global state, error, motor_power
  # Compute error and divide by a factor
  error = abs (TARGET - prox_horizontal[2])
  scaled_error = error // SCALE
  # Add the scaled error times the gain to the base motor power
  motor_power = MOTOR + scaled_error * GAIN_P
  # Do nothing in state 0
  if state != 0:
      # If it is less than the target error, stop
      if error <  TARGET_ERROR:
        stop()
      #   otherwise, set the motor power
      else:
        motor_left_target  =  motor_power
        motor_right_target =  motor_power
        set_circle_leds()
