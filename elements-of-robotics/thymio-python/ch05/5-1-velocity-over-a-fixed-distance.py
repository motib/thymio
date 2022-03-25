# Activity 5.1
# Also Activity 5.2, 5.10

# Velocity over a fixed distance
# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# A rectangle of a known length made of black tape.
# Place the Thymio before the start tape and touch the center button 
# The Thymio approaches the start tape and if it reaches its 
# it moves rapidly, stopping if it detects the  tape.
# The side tapes ensure that the Thymio moves straight.
# Time in 4-second intervals is shown on the circle leds,
# or measure with a stopwatch.
# Compute the velocity as distance / time.

#   ||--------------------------------||
# * ||                                ||
#   ||--------------------------------||
#  Start                             End

# Alternatively, touch the back button before the center button 
# The Thymio will stop 5 seconds after the  of the start tape
# Measure the distance and compute velocity as distance / 5.

THRESHOLD = 150    # for sensing the tapes
MOTOR = 299        # motor power
CHANGE = 40        # percentage change of motor power for steering
STOP = 50          # count of timer ticks until stop

state = 0      # 0 = off, 1 = find start of tape, 2 = skip start tape, 3 = drive straight
time = 0       # Timer events

nf_leds_circle(0,0,0,0,0,0,0,0)
timer_period[0] = 100
motor_left_target = 0
motor_right_target = 0

# Stop the motors and set state to 0
def stop():
  global state, motor_left_target, motor_right_target
  state = 0
  motor_left_target  = 0
  motor_right_target = 0

# When center button released
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, set state to 1 (on) and creep forward to find start tape
    if  state == 0:
      state = 1
      nf_leds_circle(0,0,0,0,0,0,0,0)
      motor_left_target  = MOTOR - (MOTOR * CHANGE)//100
      motor_right_target = MOTOR - (MOTOR * CHANGE)//100
    # else if state is on, nf_stop
    else:
      stop()

# Display time in 4-second intervals
#  Use 31 instead of 32 to prevent overflow
def set_circle_leds():
    global time
    nf_leds_circle((time//4)*32, (time//8)*32, (time//12)*32, (time//16)*32, \
                   (time//20)*32, (time//24)*32, (time//28)*32, (32//4)*32, )

# Drive straight between the tapes
def drive_straight():
  global motor_left_target, motor_right_target
  # Display time
  set_circle_leds()
  # If both sensors find black, this is the stop tape
  if  prox_ground_delta[0] < THRESHOLD and \
      prox_ground_delta[1] < THRESHOLD:
     stop()
  # If one of the ground sensors finds the tape
  #   turn the robot in the appropriate direction
  elif  prox_ground_delta[0] < THRESHOLD:
     motor_left_target  = MOTOR + (MOTOR * CHANGE)//100
     motor_right_target = MOTOR - (MOTOR * CHANGE)//100
  elif prox_ground_delta[1] < THRESHOLD:
     motor_left_target  = MOTOR - (MOTOR * CHANGE)//100
     motor_right_target = MOTOR + (MOTOR * CHANGE)//100
  else:
  # Otherwise, drive straight
     motor_left_target  = MOTOR
     motor_right_target = MOTOR

# Start tape found
def start_found():
  global state
  # Change state to look for  of start tape
  if  prox_ground_delta[0] < THRESHOLD and \
      prox_ground_delta[1] < THRESHOLD:
    state = 2

# End of start tape found
def _of_start_found():
  global state, time, motor_left_target, motor_right_target
  if  prox_ground_delta[0] > THRESHOLD and \
      prox_ground_delta[1] > THRESHOLD:
    # Change state to 3 (straight)
    state = 3
    # Initialize time counter to 0 and drive forward
    time = 0
    motor_left_target  = MOTOR
    motor_right_target = MOTOR

# Proximity event occurs, nf_subroutine deping on the state
@onevent
def prox():
  # Check if the start tape has been found
  if  state == 1:
    start_found()
  # Check if the  of the start tape has been found
  elif state == 2:
    _of_start_found()
  # Drive straight until stop tape sets state to 0
  elif state == 3:
    drive_straight()

# Timer event: increment the time counter
@onevent
def timer0():
  global time
  if state == 3: time += 1
