"""
  SLAM algorithm with map update
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  There are three objects
  There are 5x3 = 15 test positions of the robot
  A perception is the distance and angle to an object

  For a test position, the expected perception of
    each object can be computed
  Given a measured perception,
    the similarity of perception to each expected perception
    is computed as the sum of the absolute values of the differences
  The test position with the best similarity is displayed

  Define a new object
  Compute its perception and position from the best position
  Is it close to its actual position?
"""

import math

##########################################################
# Functions for printing
##########################################################

# Print the initial data
def print_initial():
    print("Objects")
    print(objects)
    print()
    print("Test positions of robot")
    for t in test_positions:
        print_position(t)
    print()

# Print position
def print_position(pos):
    print("(({:4.1f},{:4.1f}),{:6.1f})".format(
        pos[0][0], pos[0][1], math.degrees(pos[1])))

# Print a perception
def print_one_perception(per):
    print("({:4.1f},{:6.1f})  ".format(
        per[0], math.degrees(per[1])), end="")

# Print all perceptions of an object
#   Print similarity (< 0 means don't print)
def print_perceptions(perceptions, similarity):
    for p in perceptions:
        print_one_perception(p)
    if similarity >= 0:
        print("similarity ={:5.2f}".format(similarity), end="")
    print()

##########################################################
# Computations
##########################################################

# Given an object and a test position compute the perception
def perception_of_object(obj, pos):
    # Distance
    dx = obj[0]-pos[0][0]
    dy = obj[1]-pos[0][1]
    d = math.sqrt(dx**2 + dy**2)
    # Angle, corrected for test position angle
    theta = math.atan2(dy, dx) - pos[1]
    return (d, theta)

# Compute similarity of measured perceptions to
#   perceptions at a test position
def compute_similarity(measured, test):
    similarity = 0.0
    for i in range(len(measured)):
        similarity += abs(measured[i][0]-test[i][0]) + \
                      abs(measured[i][1]-test[i][1])
    return similarity

# Given a test position and the objects
#   return a list of the perceptions of all the objects
def get_all_perceptions(test):
    perceptions = []
    for obj in objects:
        perceptions.append(perception_of_object(obj, test))
    return perceptions

# Compute the perceptions from all test positions
#   and return the position of the one with the
#   best similarity to the measured perceptions
def get_best_position(measured_perceptions):
    print("\nExpected perceptions of the obstacles and", \
          "their similarities")
    # Initialize best similarity and position
    best_similarity = 1000
    best_position = None
    for t in test_positions:
        # Get perceptions for each test position
        perceptions_at_test = get_all_perceptions(t)
        # Compute similarity
        similarity = compute_similarity(
            perceptions_at_test, measured_perceptions)
        print_perceptions(perceptions_at_test, similarity)
        # Is this similarity better?
        if similarity < best_similarity:
            best_similarity = similarity
            best_position = t
    # Display and return best position
    print("\nBest position ", end="")
    print_position(best_position)
    print("Similarity ={:5.2f}".format(best_similarity))
    return best_position

# Compute the position of a new object from the best position
#   and its new perception
# Print the computed position and the actual position
def locate_position_of_new_object(
        best_position, new_object, new_perception):
    # Compute what the perception should be
    print("\nThe new object", new_object,
      "should have the perception ", end="")
    print_one_perception(perception_of_object(
        new_object, best_position))
    # Print what the perception actually is
    print("\nSuppose it has the perception ", end="")
    print_one_perception(new_perception)
    print()
    # Compute the position of the new object from the best position
    #   and the new perception
    theta = best_position[1] + new_perception[1]
    x = best_position[0][0]  + new_perception[0]*math.cos(theta)
    y = best_position[0][1]  + new_perception[0]*math.sin(theta)
    # Display the new position
    print("The new object is computed to be at ({:4.2},{:4.2})"
          .format(x,y))
    print("Is that close to its actual position", new_object, "?")
    print("Add it to the map")

##########################################################
# Initialization
##########################################################

objects = [(2,2),(2,0),(2,-2)]

test_positions = [
    [(x,y),theta]
    for (x,y) in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]
    for theta in [-math.pi/12, 0, math.pi/12]]

print_initial()

##########################################################
# Run the program
##########################################################

# Measured perceptions
measured_perceptions = \
             [(2.0, math.radians(32)),
              (2.6, math.radians(-20)),
              (3.0, math.radians(-30))]
print("Measured perceptions")
print_perceptions(measured_perceptions, -1)

# Get position with best similarity to the measured perceptions
best_position = get_best_position(measured_perceptions)

# Locate position of a new object
#   assuming the robot is at best_position
new_object = (3,0)
new_perception = (3.4,-math.radians(6.0))
locate_position_of_new_object(best_position, new_object, new_perception)
