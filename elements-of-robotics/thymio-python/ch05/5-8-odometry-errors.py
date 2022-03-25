# Activity 5.8

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Left, right buttons set motor power (by +//- 100)
# Forward, backward buttons to set difference
#   between left and right motors (by +//- 10)
# Center button to start, stop

motor  = 0        # Motor power
motor_diff = 0    # Difference between motors
state      = 0    # 0 = off, 1 = on

nf_leds_circle(0,0,0,0,0,0,0,0)

# Set the circle leds to indicate the motor power
def set_circle_leds():
  if motor//100==0: nf_leds_circle(0,0,0,0,0,0,0,0) 
  if motor//100==1: nf_leds_circle(32,0,0,0,0,0,0,0) 
  if motor//100==2: nf_leds_circle(32,32,0,0,0,0,0,0) 
  if motor//100==3: nf_leds_circle(32,32,32,0,0,0,0,0) 
  if motor//100==4: nf_leds_circle(32,32,32,32,0,0,0,0) 
  if motor//100==5: nf_leds_circle(32,32,32,32,32,0,0,0) 

# Button event handlers
#   Left//right: increase or decrease motor power within 0-500
@onevent
def button_left():
  global motor
  if  button_left == 0:
    motor = motor - 100
    if  motor < 0: motor = 0 
    set_circle_leds()

@onevent
def button_right():
  global motor
  if  button_right == 0:
    motor = motor + 100
    if  motor > 500: motor = 500 
    set_circle_leds()

#   forwards, backwards: increase or decrease diff within 0-100
@onevent
def button_forward():
  global motor_diff
  if  button_forward == 0:
    motor_diff = motor_diff + 10
    if  motor_diff > 100: motor_diff = 100 

@onevent
def button_backward():
  global motor_diff
  if  button_backward == 0:
    motor_diff = motor_diff - 10
    if  motor_diff < 0: motor_diff = 0 

# When center button released
@onevent
def button_center():
  global motor_diff, state, motor, motor_left_target, motor_right_target
  if  button_center == 0:
    # If off, set state to 1 (on) and dirve forwards
    if  state == 0:
      state = 1
      motor_left_target  = motor + motor_diff
      motor_right_target = motor
    #   else: if state is on, stop the motors
    else:
      state = 0
      motor_left_target  = 0
      motor_right_target = 0
      motor = 0
      motor_diff = 0
      set_circle_leds()
