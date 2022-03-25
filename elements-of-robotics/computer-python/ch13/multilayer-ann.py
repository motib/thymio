"""
  Multilayer ANNs
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  This program computes the output values of a two-layer ANN
"""

# Weights
w11 =  1.0
w12 =  0.5
w21 =  1.0
w22 = -1.0

# Function to limit output to range -1.0 .. 1.0
def output_function(a):
    return -1.0 if a < -1.0 else (1.0 if a > 1.0 else a)

print("w11 =", w11)
print("w12 =", w12)
print("w21 =", w21)
print("w22 =", w22)

# Print values for at 0.2 increments in -2.0 to 2.0
print("  x      u1     u2     y")
for i in range(-10,11):
    x = i*0.2
    # Intermediate outputs are linear (limited to -1.0 .. 1.0
    u1 = output_function(x*w11)
    u2 = output_function(x*w12)

    # Output is linear descending for inputs -2.0 .. -1.0
    #   and 1.0 .. 2.0 and zero for inputs -1.0 .. 1.0
    y = output_function(u1*w21 + u2*w22)
    print("{:5.2f}  {:5.2f}  {:5.2f}  {:5.2f}".format(x, u1, u2, y))
