"""
  Braitenberg vehicle: dogged behavior

  When the robot detects an object in front it moves backwards
  When the robot detects an object in back it moves forwards

  The robot is turned on and off using the center button
    When turned on, initially the robot moves forward
    When turned off, the robot stops
"""

# State: False = off, True = on
state = False

# Timer period (0.5 seconds) for displaying variables
timer_period[1] = 500

# Function for setting top leds RGB
def top(r,g,b):
    nf_leds_top(r,g,b)

# Function for setting circle leds
# Called with:
#   0 = turn off leds
#   1 = turn on led  0
#   2 = turn on leds 0, 1
#   3 = turn on leds 0, 1, 2
def circle(motion):
    nf_leds_circle(32*(motion % 4 > 0),
                   32*(motion % 4 > 1),
                   32*(motion % 4 > 2),
                   0,0,0,0,0)

# Event handler for the center button
# Set state False = off, True = on
# Set motor power forward or stop
# Turn on appropriate top and circle leds
@onevent
def button_center():
    # Global declarations
    global state
    global motor_left_target, motor_right_target

    # The variable button_center is False if the button is released
    if not button_center:
        if state:
            state = False
            # Turn top leds off
            top(0,0,0)
            circle(0)
            motor_left_target = 0
            motor_right_target = 0
            timer_period[1] = 0
        else:  # not state
            state = True
            # Turn top leds red
            top(32,0,0)
            circle(1)
            motor_left_target = 200
            motor_right_target = 200
            timer_period[1] = 500

# Event handler for proximity sensors
@onevent
def prox():
    # Global declarations
    global motor_left_target, motor_right_target

    # If state is off don't do anything
    if not state: return
    
    # If front central sensor detects an obstacle
    #   set motors to move backwards
    if prox_horizontal[2] > 2000:
        # Turn top leds green
        top(0,32,0)
        circle(2)
        motor_left_target = -200
        motor_right_target = -200
    # If both back sensors detect an obstacle
    #   set motors to move forwards
    elif prox_horizontal[5] > 2000 and \
         prox_horizontal[6] > 2000:
        # Turn top leds blue
        top(0,0,32)
        circle(3)
        motor_left_target = 200
        motor_right_target = 200

# Print values for horizontal proximity sensors
def print_horizontal():
    print('prox_horizontal',
          prox_horizontal[0], prox_horizontal[1],
          prox_horizontal[2], prox_horizontal[3],
          prox_horizontal[4],
          prox_horizontal[5], prox_horizontal[6])

@onevent
def timer1():
    print_horizontal()
