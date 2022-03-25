# Activity 9-3b

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# A robotic lawnmower with landmarks
# Center button to start, stop
# Show state in circle leds

LONG_PERIOD   = 5000   # period of initial sweep
SHORT_PERIOD  = 400    # period of other sweeps
TURN_PERIOD   = 1250   # period of turns
PERIOD_DELTA  = 500    # for making small changes in the periods
MOTOR         = 200    # motor power for moving straight
MOTOR_CHANGE  = 200    # change in motor power for turns
THRESHOLD     = 300    # detection of barriers

# Surround the lawn with barriers as shown in the book
# The first sweep is "too long" and encounters the barrier
# When the robot detects the barrier, it move backwards
#   and: changes back to the state for the sweep
# Only implemented barriers on sweeps, not on turns

# Center button to start, stop
# Show state in circle leds

# 0=off, 1=straight, 2=turn, 3=short,
#   4=return to charging station, 5=encountered barrier
state = 0

# 0=first turn, 1=second turn
turn = 0

# Direction of turn: -1=left, 1=right
direction = 1

# Count of sweeps
count = 0

timer_period[0] = 0
nf_leds_circle(0,0,0,0,0,0,0,0)
nf_leds_top(0,0,0)

# Display state in circle leds
def set_circle_leds():
  global state
  if state==0: nf_leds_circle(0,0,0,0,0,0,0,0)    
  if state==1: nf_leds_circle(32,0,0,0,0,0,0,0)   
  if state==2: nf_leds_circle(32,32,0,0,0,0,0,0)  
  if state==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if state==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if state==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Display sweep count in top leds
def set_top_leds():
  global count
  if count == 0: nf_leds_top(0,0,0)    
  if count == 1: nf_leds_top(32,0,0)   
  if count == 2: nf_leds_top(0,32,0)   
  if count == 3: nf_leds_top(0,0,32)   
  if count == 4: nf_leds_top(32,32,0) 
  if count == 5: nf_leds_top(32,32,32) 

def stop():
  global state, count, motor_left_target, motor_right_target
  state = 0
  count = 0
  motor_left_target = 0
  motor_right_target = 0
  timer_period[0] = 0
  set_circle_leds()
  set_top_leds()

@onevent
def button_center():
    global state, direction, count
    global timer_period, motor_left_target, motor_right_target
    if button_center == 0:
     if state == 0:
        state = 1
        set_circle_leds()
        direction = -1
        count = 0
        set_top_leds()
        motor_left_target = MOTOR
        motor_right_target = MOTOR
        timer_period[0] = LONG_PERIOD
     else:
        stop()

@onevent
def timer0():
  global state, direction, count, turn
  global timer_period, motor_left_target, motor_right_target
  # State 0: do nothing
  if state == 0:
    return
  # State 1:  of long arm, start turn=1
  elif state == 1:
    # Count sweeps and change direction after four sweeps
    count += 1
    set_top_leds()
    if count == 4: direction = -direction
    motor_left_target = MOTOR + direction*MOTOR_CHANGE
    motor_right_target = MOTOR - direction*MOTOR_CHANGE
    state = 2
    turn = 1
    timer_period[0] = TURN_PERIOD

  # State 2:  of turn
  #   start short arm if turn=1
  #   else start long arm if turn=2
  elif state == 2:
    if turn == 1:
      motor_left_target = MOTOR
      motor_right_target = MOTOR
      turn = 1
      # After four sweeps, return to base
      if count == 4:
        state = 4
        timer_period[0] = SHORT_PERIOD*9
      else:
        state = 3
        timer_period[0] = SHORT_PERIOD
    else:
      motor_left_target = MOTOR
      motor_right_target = MOTOR
      state = 1
      # change direction of turn
      direction = - direction
      if count == 4:
        timer_period[0] = LONG_PERIOD-PERIOD_DELTA
      else:
        timer_period[0] = LONG_PERIOD-2*PERIOD_DELTA
  
  # state 3:  of short arm, start turn=2
  elif state == 3:
    motor_left_target = MOTOR + direction*MOTOR_CHANGE
    motor_right_target = MOTOR - direction*MOTOR_CHANGE
    state = 2
    turn = 2
    timer_period[0] = TURN_PERIOD
  # Returned to base, stop
  elif state == 4:
    stop()
  
# Detect barrier in sweep state
@onevent
def prox():
  if state != 1: return 
  if prox_ground_delta[0] < THRESHOLD or \
     prox_ground_delta[1] < THRESHOLD:
     state = 5
     # Move backwards for a short period of time
     motor_left_target = -MOTOR
     motor_right_target = -MOTOR
     timer_period[1] = 2*SHORT_PERIOD

# Backwards move finished, return to sweep state
@onevent
def timer1():
  if state != 5: return 
  state = 1
  timer_period[0] = 100
