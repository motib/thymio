# Activity 8.2

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Determining distance by triangulation
# Measure the angles from two different places and:
#   compute the distances using the law of sines
# See Figure 8.2 in "Elements of Robotics"

THETA = 20
DISTANCE = 24

# Index of sensor with maximum value and the maximum value
max_prox = 0
max_value = 0

# Index for searching
index = 0

# Side of the triangle (distance to the object)
distance = 0

# Angle to object: -2*THETA, -THETA, 0, THETA, 2*THETA
# Use angle for defroutine and store in alpha and beta
alpha = 0
beta = 0
angle = 0

#################################################################

# Subroutines for displaying data on the leds

# Clear all leds
def clear_leds():
    nf_leds_circle(0,0,0,0,0,0,0,0)
    nf_leds_bottom_left(0,0,0)
    nf_leds_bottom_right(0,0,0)

# Set the circle leds to indicate the distance to the object
#   Use 31 instead of 32 so as not to overflow
def set_distance_leds():
    distance1 = (distance - 10) // 2
    nf_leds_circle( \
        (distance1//1)*31, (distance1//2)*31, \
        (distance1//3)*31, (distance1//4)*31, \
        (distance1//5)*31, (distance1//6)*31, \
        (distance1//7)*31, (distance1//8)*31)

# The angle is displayed as a color in the top leds
#   and the sign in the bottom leds
def set_angle_leds():
    if angle < 0: nf_leds_bottom_left(32,0,0)
    elif angle > 0: nf_leds_bottom_right(32,0,0)
    
    if abs(angle) == THETA: nf_leds_top(0,32,0)
    elif abs(angle) == 2*THETA: nf_leds_top(0,0,32)
    else: nf_leds_top(0,32,32)
    
#################################################################

# Computations of distance, angle, coordinates

# Get the angle to the object by finding the sensor
#   with the highest value
def get_angle():
    global max_value, max_prox, angle
    max_value = -1
    for i in range(5):
        if prox_horizontal[i] > max_value:
            max_value = prox_horizontal[i]
            max_prox = i    
    angle = (2 - max_prox) * THETA

# Compute the coordinates as:
#   x = distance * sin(angle), y = distance * cos(angle)
# Aseba sin//cos use radians in the full 16-bit integer range
def compute_distance():
    global distance
    beta1 = math_muldiv(314, beta, 180) * 100
    dcos = math_cos(beta1)
    gamma = math_muldiv(314, alpha+beta, 180) * 100
    dsin = math_sin(gamma)
    distance = math_muldiv(DISTANCE, dcos, dsin)

#################################################################

# Button event handlers

# When the forward button is released,
#   sense, compute and display the distance and angle
@onevent
def button_forward():
    global alpha
    if button_forward == 0:
        clear_leds()
        get_angle()
        set_angle_leds()
        alpha = abs(angle)
    
# When the backward button is released,
#   compute and display the x and y coordinates
@onevent
def button_backward():
    global beta
    if button_backward == 0:
        clear_leds()
        get_angle()
        set_angle_leds()
        beta = abs(angle)
        compute_distance()
        set_distance_leds()
