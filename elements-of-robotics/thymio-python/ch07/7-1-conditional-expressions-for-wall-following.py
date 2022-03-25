# Activity 7.1

# Copyright 2014, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Follow a wall on the right of the Thymio
# Doesn't work very well because of the difficulty
#   of setting the timer correctly
# State machine defined below
# Display state on circle leds

THRESHOLD = 1500
CORNER1 = 14
CORNER2 = 3
CORNER3 = 3
DURATION = 200

# States
#  0 - off
#  1 - no wall on right, go straight
#  2 - wall on right, go straight
#  3 - wall on right, but too close, turn left
#  4 - wall _no longer_ on right, go straight for about 1.5 sec
#  5 - turn left for about .5 sec
#      if still wall on right, go to state 2
#      if no longer wall on right, turn left (state 6)
#  6 - turn left for about .5 sec

state = 0    # For state machine
count = 0    # Count of timer expirations of DURATION sec

nf_leds_circle(0,0,0,0,0,0,0,0)
timer_period[0] = 0

@onevent
def button_center():
  global state, count, timer_period
  global motor_left_target, motor_right_target
  if button_center == 0:
      if state == 0:
        state = 1
        nf_leds_circle(32,0,0,0,0,0,0,0)
        motor_left_target = 150
        motor_right_target = 150
      else:
        state = 0
        nf_leds_circle(0,0,0,0,0,0,0,0)
        motor_left_target = 0
        motor_right_target = 0
      count = 0
      timer_period[0] = 0

@onevent
def timer0():
  global count
  count += 1

@onevent
def prox():
  global state, count, timer_period
  global motor_left_target, motor_right_target
  if state != 0:
      if state == 5:
        if count >= CORNER2:
          if prox_horizontal[4] > THRESHOLD:
            state = 2
            nf_leds_circle(0,32,0,0,0,0,0,0)
            motor_left_target = 150
            motor_right_target = 150
          else:
            state = 6
            nf_leds_circle(0,0,0,0,0,6,0,0)
            count = 0
            timer_period[0] = DURATION
            motor_left_target = -400
            motor_right_target = 400
      elif prox_horizontal[4] > 2*THRESHOLD:
        state = 3
        nf_leds_circle(0,0,32,0,0,0,0,0)
        motor_left_target = 150
        motor_right_target = 250
      elif prox_horizontal[4] > THRESHOLD:
        state = 2
        nf_leds_circle(0,32,0,0,0,0,0,0)
        motor_left_target = 150
        motor_right_target = 150
      elif state == 2 or state == 3:
        state = 4
        nf_leds_circle(0,0,0,32,0,0,0,0)
        count = 0
        timer_period[0] = DURATION
      elif state == 4:
        if count >= CORNER1:
          state = 5
          nf_leds_circle(0,0,0,0,32,0,0,0)
          count = 0
          timer_period[0] = DURATION
          motor_left_target = 400
          motor_right_target = -400  
      elif state == 6:
        if  count >= CORNER3:
          state = 1
          nf_leds_circle(32,0,0,0,0,0,0,0)
          motor_left_target = 150
          motor_right_target = 150
      else:
        state = 1
        nf_leds_circle(32,0,0,0,0,0,0,0)
        motor_left_target = 150
        motor_right_target = 150
