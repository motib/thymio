# Activity 8.2
# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Determining distance from an angle and a distance

"""
The sensors are on the front panel of the robot which forms an arc of a
circle whose center is the hole.
Place a protractor with its center over the hole and use a thread to form
a line from the center to a sensor. Read the angle from the protractor.
Since the sensors are spaced uniformly define a constant \p{THETA}
to be the angle between two sensors.
The angle to the object is determined by the horizontal sensor that
returns the highest value.

The Thymio is at the origin of a coordinate
system with (0,0) defined as the hole. The x-axis goes through the
axis of the wheels, while the y-axis points forwards. Given the angle
theta to the object as defined by the horizontal proximity sensor
with the highest value, and the distance d to the object defined by the
value returned by that sensor, the coordinates can be computed using
elementary trigonometry.

When the forward button is released, sense, compute and
display the distance and angle When the backward button is released,
compute and display the x and y coordinates
"""

THETA = 20 # The angle between two sensors.
OFFSET = 8 #The distance from the hole in the Thymio to the front panel.

# Values of the horizontal proximity sensor for an object at
# 2 .. 16 cm in increments of 2 cm
# -1 is a sentinel to stop the search
proximity = [4300, 4200, 3800, 3500, 3300, 3000, 2600, 2300, -1]

# Index for searching the proximity sensors and array
index = 0

# Index of sensor with maximum value and the maximum value
max_prox = 0
max_value = 0

# Distance in cm computed from proximity sensor values
# Uses constant OFFSET: distance from center hole to the sensors
distance = 0

# Angle to object: -2*THETA, -THETA, 0, THETA, 2*THETA
angle = 0

# x, y coordinates and variables for their computation
x = 0
y = 0
theta = 0

# Arcs of the circle leds to show relative x coordinate
arcs = 0

#################################################################

# Subroutines for displaying data on the leds

# Clear all leds
def clear_leds():
    nf_leds_circle(0,0,0,0,0,0,0,0)
    nf_leds_bottom_left(0,0,0)
    nf_leds_bottom_right(0,0,0)

# Set the circle leds to indicate the index into the array proximity
#   Use 31 instead of 32 so as not to overflow
def set_distance_leds():
    nf_leds_circle( \
        (index//1)*31, (index//2)*31, (index//3)*31, (index//4)*31, \
        (index//5)*31, (index//6)*31, (index//7)*31, (index//8)*31)

# The angle is displayed as a color in the top leds
#   and the sign in the bottom leds
def set_angle_leds():
    if angle < 0: nf_leds_bottom_left(32,0,0)
    elif angle > 0: nf_leds_bottom_right(32,0,0)
    
    if abs(angle) == THETA: nf_leds_top(0,32,0)
    elif abs(angle) == 2*THETA: nf_leds_top(0,0,32)
    else: nf_leds_top(0,32,32)
    

# Display the coordinates
#   x: leds 1,2,3 indicate higher x, leds 7,6,5 higher negative x
#   y: the brighter the top leds, the larger the y coordinate
def set_coordinate_leds():
    global arcs
    nf_leds_top(y*2,0,0)
    arcs = 0
    if abs(x) > 1: arcs = 2 
    if abs(x) > 4: arcs = 4 
    if abs(x) > 8: arcs = 8 
    if x < 0: arcs = 256 // arcs 
    nf_leds_circle( \
        (arcs & 1)*31, (arcs & 2)*31, (arcs & 4)*31, (arcs & 8)*31, \
        (arcs & 16)*31, (arcs & 32)*31, (arcs & 64)*31, (arcs & 128)*31)

#################################################################

# Computations of distance, angle, coordinates

# Get the angle to the object by finding the sensor
#   with the highest value
def get_angle():
    global angle, max_value, max_prox
    max_value = -1
    for i in range(5):
        if prox_horizontal[i] > max_value:
            max_value = prox_horizontal[i]
            max_prox = i
    angle = (2 - max_prox) * THETA

# Get the distance by searching the proximity array
#   for the first item greater than the sensor value
# Distance takes into account OFFSET of hole from sensors
def get_distance():
    global distance, index
    index = 0
    while proximity[index] > prox_horizontal[max_prox]:
        index += 1
    distance = OFFSET + index * 2

# Compute the coordinates as:
#   x = distance * sin(angle), y = distance * cos(angle)
# Aseba sin//cos use radians in the full 16-bit integer range
def compute_coordinates():
    global theta, dsin, dcos, x, y
    theta = math_muldiv(314, angle, 180) * 100
    dsin = math_sin(theta)
    dcos = math_cos(theta)
    x = math_muldiv(dsin, distance, 32767)
    y = math_muldiv(dcos, distance, 32767)
    y = y - OFFSET

#################################################################

# Button event handlers

# When the forward button is released,
#   sense, compute and display the distance and angle
@onevent
def button_forward():
    if button_forward == 0:
        clear_leds()
        get_angle()
        get_distance()
        set_angle_leds()
        set_distance_leds()

# When the backward button is released,
#   compute and display the x and y coordinates
@onevent
def button_backward():
    if button_backward == 0:
        clear_leds()
        compute_coordinates()
        set_coordinate_leds()
