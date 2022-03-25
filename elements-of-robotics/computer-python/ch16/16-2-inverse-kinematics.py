import math
"""
  Inverse kinematics (offline computations)
  Copyright 2017 Moti Ben-Ari and Francesco Mondada
  CreativeCommons BY-SA

  This program computes the inverse kinematics of a two-link
  two-dimensional robotic arm.
  Input:  link1, link2 the lengths of the links
          (x,y) coordinates of the goal.
  Output: alpha, beta angles of the arms
"""

# For the example in the book, link1=1, link2=1, x=y=1.366

# Get link lengths
link1 = float(input("link 1: "))
link2 = float(input("link 2: "))

# Get goal coordinates
x = float(input("x coordinate: "))
y = float(input("y coordinate: "))

# Compute in order: r, beta, gamma, alpha
r = math.sqrt(x**2 + y**2)
beta = math.pi - math.acos(
    (link1**2 + link2**2 - r**2) / (2 * link1 * link2)
    )
gamma = math.acos(r/2.0)
alpha = math.atan2(y,x) + gamma

print("alpha ={:5.1f}, beta ={:5.1f}, gamma ={:5.1f}".
      format(math.degrees(alpha),
             math.degrees(beta),
             math.degrees(gamma)))
