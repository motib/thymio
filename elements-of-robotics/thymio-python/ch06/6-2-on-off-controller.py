# Activity 6.2

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# On-off controller for approaching an object

TARGET = 4000       # Highest value of the proximity sensor
TARGET_ERROR = 500  # Stop if error is below this value
MOTOR = 400         # Power setting for the motor

# Center button to start and stop
# Robot approaches object detected by center sensor

state = 0       # The state 0 = off, 1 = on
error = 0       # Difference between sensor and target values
motor_left_target  = 0
motor_right_target = 0
nf_leds_circle(0,0,0,0,0,0,0,0)

# Stop the algorithm and the motors
def stop():
  global state
  global motor_left_target, motor_right_target
  state = 0
  motor_left_target  = 0
  motor_right_target = 0
  nf_leds_circle(0,0,0,0,0,0,0,0)

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
  global state, error
  # Do nothing in state 0
  if state != 0:
      # Compute the error
      error = abs (TARGET - prox_horizontal[2])
      # If it is less than the target error, stop
      if error < TARGET_ERROR:
        stop()
      #   otherwise, set motors to full power
      else:
        nf_leds_circle(32,0,0,0,0,0,0,0)
        motor_left_target  =  MOTOR
        motor_right_target =  MOTOR
