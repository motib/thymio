"""
  Robotic crane
  Copyright 2017, 2022 Moti Ben-Ari
  CreativeCommons BY-SA

  Given a goal distance and the accelerations of the
    mobile robot and the winch, the program calculates
    the amount of time for each component to reach
    the distance on its own.
  Then it computes the time for the robot to get as close
    as possible followed by the movement of the winch.
  The computation locates positions whose absolute value
    is as close to the goal as possible.
"""

print("Robotic crane with one degree of freedom and two actuators")

debug = False

# Set parameters
distance_to_move   = 50
acceleration_robot = 4.3
acceleration_winch = 0.8

# Given an acceleration, compute the time and distance
#  to get as close as possible to distance_to_move
# For robot then winch, start_distance is where the winch starts
# Sign is -1 if the winch needs to pull back
def time_to_distance(acceleration, start_distance, sign):
    distance = start_distance
    time = 0
    # Compute distance from acceleration until distance is
    #   greater than distance_to_move (or less if pulling back)
    while sign*distance < sign*distance_to_move:
        time += 1
        previous_distance = distance
        distance = start_distance + sign * 0.5 * acceleration * time**2
        if debug:
            print("Time ={:3d}, previous distance = {:5.1f}, distance ={:5.1f}".\
                  format(time, previous_distance, distance))
    # Check if previous distance was closer
    if abs(distance_to_move - previous_distance) < \
       abs(distance - distance_to_move):
        distance = previous_distance
        time -= 1
    return (time, distance)

print("Distance to move = {:4.1f} cm".format(distance_to_move))
print("Accelerations: robot = {:4.1f} cm/s, winch = {:4.1f} cm/s".
      format(acceleration_robot, acceleration_winch))

# Robot alone
time_robot, distance_robot = \
      time_to_distance(acceleration_robot, 0, 1)
print("Robot alone reaches {:5.1f} cm in {:3d} seconds".\
      format(distance_robot, time_robot))

# Winch alone
time_winch, distance_winch = \
      time_to_distance(acceleration_winch, 0, 1)
print("Winch alone reaches {:5.1f} cm in {:3d} seconds".\
      format(distance_winch, time_winch))

# Is robot beyond distance?
beyond = 1 if distance_robot < distance_to_move else -1

# Robot then winch
time_winch, distance_both = \
      time_to_distance(acceleration_winch, distance_robot, beyond)
print("Robot + winch reach {:5.1f} cm in {:3d} seconds".\
      format(distance_both, time_robot + time_winch))
