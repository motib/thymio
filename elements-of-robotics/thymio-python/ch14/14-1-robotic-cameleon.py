# Activity 14.1

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Robotic chameleon

# Run the robot for a fixed period of time over a gray area
#   sampling with the ground sensor
# Touch center button to start

# Export the values of the sensors
#   Right click on the event "ground" and select plot
#   Click the "plot of ground" tab to display the plot window
#   Click "Save as"
# To clear before next run
#   Click "Clear" below the bottom right pane 
#   Click clear in the plot window

# Run twice: once for dark area (save as dark.txt) and
#            once for light area (save as light.txt)

RUN_PERIOD = 2400    # period the robot runs
SAMPLE_PERIOD = 100  # period for sampling
MOTOR = 200          # motor power

# Use Python program to compute the discriminant 
#   with the best quality criterion

discriminant = 410  # Areas of dark and light very far apart
#discriminant = 710  # Areas of dark and light very close

state = 0  # 0 = start, 1 = run

def stop():
  global state, timer_period, motor_left_target, motor_right_target
  state = 0
  nf_leds_top(0,0,0)
  timer_period[0] = 0
  timer_period[1] = 0
  motor_left_target  = 0
  motor_right_target = 0

# Start on touch of center button
@onevent
def button_center():
    global state, timer_period, motor_left_target, motor_right_target
    if button_center == 0:
        motor_left_target = MOTOR
        motor_right_target = MOTOR
        timer_period[0] = RUN_PERIOD
        timer_period[1] = SAMPLE_PERIOD
        state = 1

# Stop the run
@onevent
def timer0():
  stop()

# Sample the ground sensors
@onevent
def timer1():
  if state == 0: return
  emit("ground", prox_ground_delta[0], prox_ground_delta[1])

@onevent
def prox():
  if state == 0: return
  if (prox_ground_delta[0]+prox_ground_delta[1]) // 2 > discriminant:
    nf_leds_top(32,32,32)
  else:
    nf_leds_top(32,0,32)
