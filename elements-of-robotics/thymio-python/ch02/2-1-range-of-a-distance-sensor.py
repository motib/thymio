# Activity 2.1
# Also for 2.2 and 2.3

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Measure the range of the distance sensor
# Display computed distance in the circle leds

# The array contains the values of the horizontal proximity sensor
# You need to calibrate the array for 2, 4, ..., 16 centimetrs

proximity = [4550, 4400, 3900, 3400, 3000, 2700, 2400, 2100, 0]

leds_circle = [0,0,0,0,0,0,0,0]

# A timer event will be used to print out the value of the sensor
timer_period[0] = 500 # Milliseconds = 1/2 second

# Set the circle leds to indicate the distance
def set_circle_leds(distance):
  nf_leds_circle((distance//1)*31, (distance//2)*31, (distance//3)*31, (distance//4)*31, \
                 (distance//5)*31, (distance//6)*31, (distance//7)*31, (distance//8)*31)

# Search the array until a value is found
#   that is not greater than the measured value
#   of the horizontal sensor
# Call set_circle_leds to display the distance
@onevent
def prox():
  distance = 0
  while proximity[distance] > prox_horizontal[2]:
    distance += 1
  set_circle_leds(distance)

# Print the center sensor periodically
@onevent
def timer0():
    print(prox_horizontal[2])
