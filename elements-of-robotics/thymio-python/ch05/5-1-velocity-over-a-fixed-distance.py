# Activity 5.1
# Also Activity 5.2, 5.10

# Velocity over a fixed distance
# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# A rectangle of a known length made of black tape
# Place the Thymio before the start tape and
#   touch the center button 
# The Thymio approaches the start tape and
#   moves rapidly, stopping if it detects the  tape
# The side tapes ensure that the Thymio moves straight.
# Time in .5-second intervals is shown on the circle leds,
# or measure with a stopwatch.
# Compute the velocity as distance / time.

#   ||--------------------------------||
# * ||                                ||
#   ||--------------------------------||
#  Start                             End

# Alternatively, touch the back button before the center button 
# The Thymio will stop 5 seconds after the  of the start tape
# Measure the distance and compute velocity as distance / 5.

threshold  = 150   # for sensing the tapes
motor      = 300   # motor power
motor_init = 200   # motor_init power
change     = 50    # change of motor power for steering
stop       = 50    # count of timer ticks until stop

state      = 0     # 0 = off, 1 = find start of tape,
                   # 2 = skip start tape, 3 = drive straight
time       = 0     # Timer events
stop_timer = 0     # Stop after a fixed number of counts


timer_period[0]    = 100
motor_left_target  = 0
motor_right_target = 0
set_circle_leds()

# Stop the motors and set state to 0
def stop():
  global state, motor_left_target, motor_right_target
  state = 0
  motor_left_target  = 0
  motor_right_target = 0
  print(time)
  set_circle_leds()

# Drive straight between the tapes
def drive_straight():
  global motor_left_target, motor_right_target
  # Display time
  set_circle_leds()
  # If both sensors find black, this is the stop tape
  if  prox_ground_delta[0] < threshold and \
      prox_ground_delta[1] < threshold:
     stop()
  # If one of the ground sensors finds the tape
  #   turn the robot in the appropriate direction
  elif  prox_ground_delta[0] < threshold:
     motor_left_target  = motor + change
     motor_right_target = motor - change
  elif prox_ground_delta[1] < threshold:
     motor_left_target  = motor - change
     motor_right_target = motor + change
  else:
  # Otherwise, drive straight
     motor_left_target  = motor
     motor_right_target = motor

# Start tape found
def start_found():
  global state
  # Change state to look for  of start tape
  if  prox_ground_delta[0] < threshold and \
      prox_ground_delta[1] < threshold:
    state = 2

# End of start tape found
def end_of_start_found():
  global state, time, motor_left_target, motor_right_target
  if  prox_ground_delta[0] > threshold and \
      prox_ground_delta[1] > threshold:
    # Change state to 3 (straight)
    state = 3
    # Initialize time counter to 0 and drive forward
    time = 0
    motor_left_target  = motor
    motor_right_target = motor

# Proximity event occurs, nf_subroutine deping on the state
@onevent
def prox():
  # Check if the start tape has been found
  if  state == 1:
    start_found()
  # Check if the  of the start tape has been found
  elif state == 2:
    end_of_start_found()
  # Drive straight until stop tape sets state to 0
  elif state == 3:
    drive_straight()

# Timer event: increment the time counter
@onevent
def timer0():
  global time
  if state == 3:
      time += 1
      # If stop_timer is non-zero, stop when time expired
      if time == stop_timer:
        stop()

# When center button released
@onevent
def button_center():
  global state, time, motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, set state to 1 (on) and creep forward to find start tape
    if  state == 0:
      state = 1
      time = 0
      set_circle_leds()
      motor_left_target  = motor_init
      motor_right_target = motor_init
    else:
      stop()

# Toggle the value of stop_timer when back button is touched
@onevent
def button_backward():
    global stop_timer
    if button_backward == 0:
        if stop_timer == stop:
            stop_timer = 0
        else:
            stop_timer = stop

# Display time in .5-second intervals
def set_circle_leds():
    global time
    nf_leds_circle(
        (time// 5)*32, (time//10)*32,
        (time//15)*32, (time//20)*32,
        (time//25)*32, (time//30)*32,
        (time//35)*32, (time//40)*32
        )
