# Activity 5.6

# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Estimate distance traveled for a fixed time
# Run for several values of MOTOR

MOTOR = 450    # motor target speed
TIME  = 500    # time between samples in milliseconds
COUNT = 8      # number of samples
SCALE = 600    # set to a value that gives distance in cm

state = 0     # State variable
count = 0     # Counter for sampling

timer_period[0] = TIME

# Stop the motors and set state to 0
def stop():
    global state, motor_left_target, motor_right_target
    state = 0
    motor_left_target = 0
    motor_right_target = 0

# Touch center button to start and stop
@onevent
def button_center():
  global state, motor_left_target, motor_right_target
  global button_center, count
  if  button_center == 0:
    if  state == 0:
      count = 0
      motor_left_target = MOTOR
      motor_right_target = MOTOR
      state = 1
    else:
      stop()

# On timer event, sample speed
# Terminate if COUNT samples have been taken
@onevent
def timer0():
  global state, deltaD
  if  state == 0: return
  if  count < COUNT:
    count += 1
  else:
    distance = (MOTOR*COUNT*TIME)//SCALE
    print(distance)
    stop()
