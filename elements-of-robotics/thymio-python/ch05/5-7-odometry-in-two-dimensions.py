# Activity 5.7

# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Odometry in two dimensions

TIME = 30       # Duration of run (tenths of seconds)
BASELINE = 95   # Distance between wheels (millimeters)
LEFT = 200      # Power setting of left wheel
RIGHT = 300     # Power setting of right wheel
SPEED = 32      # speed of robot per 100 power setting (*10)

state = 0    # 0 = off, 1 = on
time  = 0    # Counter of tenths of seconds

# Set timer to expire every tenth of a second
timer_period[0] = 100

# Touch center button to start and stop run
@onevent
def button_center():
  global state, motor_left_target, motor_right_target, time
  if button_center == 0:
      if state == 0:
        state = 1
        time = 0
        motor_left_target =  LEFT
        motor_right_target = RIGHT
      else:
        state = 0
        motor_left_target = 0
        motor_right_target = 0

# Compute the odometry
def odometry():
  # dleft, dright: distance traveled by the left/right wheel
  # dcenter: distance traveled by the center of the robot
  # theta: change of heading, dx: change of x, dy: change of y
  # tcos, tsin: cos and sin of theta

  # Distances traveled by left and right motors
  # Factor is: 100 for motor powers and
  #   10 each for power to speed and time in tenths of a second
  # Center distance is the average of the left and right
  # The result is divided by a factor of 100 for the motor powers,
  # 10 for the power to speed conversion (3.2 cm/sec) and again by 10
  # because the time is tenths of a second.

  dleft =  math_muldiv(motor_left_speed, SPEED*TIME, 100*10*10)
  dright = math_muldiv(motor_right_speed, SPEED*TIME, 100*10*10)
  dcenter = (dleft+dright)//2

  # Change of heading and its sine and cosine
  # Factor is 10 for axle width in millimeters and 100 for hundredths of radians
  # transforming the real range 0--3.14 to the integer range 0--314.
  # (For simplicity we consider only positive angles.)
  theta = ((dright-dleft)*10*100)//BASELINE

  # The parameter to the trigonometric functions is within
  # the entire 16-bit range -32768--32767, which represents the range
  # from -pi to pi radians.
  # Multiplying the angle by 100 will cause the range of positive
  # angles 0--314 to become 0--31400, approximately the range
  # of the positive angles as 16-bit integers.
  tcos = math_cos(theta*100)
  tsin = math_sin(theta*100)

  # We can now compute the change in the x- and y-positions:
  # The result is divided by 32767 because the result of the trigonometric
  # functions is within the entire 16-bit range -32768--32767,
  # instead of the normal range of real numbers $-1.0$--$1.0$.
  dx = math_muldiv(dcenter, -tsin, 32767)
  dy = math_muldiv(dcenter, tcos, 32767)

# Every tenth of a second, increment the counter time
# When time = TIME, compute the odometry and stop the motors
@onevent
def timer0():
  global state, time, motor_left_target, motor_right_target
  if  state == 0: return
  time += 1
  if  time == TIME:
    odometry()
    state = 0
    motor_left_target = 0
    motor_right_target = 0
