"""
  Learning with a perceptron (for light/dark discrimination)
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  Input: dark.txt and light.txt
         values of right and left sensors
  Compute discriminant by perceptron learning
"""

import random

file1  = "dark.txt"
file2  = "light.txt"

x0  = 1     # Constant input
w0  = 0.1   # Weights
w1  = 0.1
w2  = 0.1
eta = 0.1   # Learning rate

def func(sum):
    return sum - 70.0

# Read each line randomly from one of the files
# Stop when even one file is empty
with open(file1) as f1:
    with open(file2) as f2:
        eof1 = False
        eof2 = False
        for i in range(50):
            r = random.randint(0,1)
            if r == 0:
                sample = f1.readline().split()
                eof1 = sample == []
            else:
                sample = f2.readline().split()
                eof2 = sample == []
            if eof1 or eof2:
                break
            # Ignore time stamp at the beginning of the line
            color  = r
            x1     = int(sample[1])
            x2     = int(sample[2])
            # Compute output of perceptron and its sign (1 or 2)
            y      = func(w0 + w1*x1 + w2*x2)
            print("x1 = {:4d}, x2 = {:4d}, color = {:2d}, y = {:6.2f}".
                  format(x1, x2, color, y))
            y = 0 if y > 0 else 1
            # If y does not agree with color code, adjust the weights
            if y != color:
                w0 = w0 + eta*x0*y
                w1 = w1 + eta*x1*y
                w2 = w2 + eta*x2*y
            print("New weights = {:4.2f}, {:4.2f}, {:4.2f}".
                  format(w0, w1, w2))

print("\nDiscriminant line = {:4.2f} + {:4.2f} x1 + {:4.2f} x2 = 0".
      format(w0, w1, w2))

