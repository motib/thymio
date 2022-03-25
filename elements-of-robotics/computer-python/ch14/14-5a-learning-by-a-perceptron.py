"""
  Learning with a perceptron
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  Input: slope.txt
         code: 1 = not dangerous, 2 = dangerous
         values of forward/backward and up/down accelerometers
  Compute discriminant by perceptron learning
"""

file_name  = "slope.txt"

x0  = 1     # Constant input
w0  = 0.1   # Weights
w1  = 0.1
w2  = 0.1
eta = 0.1   # Learning rate

def func(sum):
    return sum - 3.0

# Read each line
with open(file_name) as file:
    for line in file:
        sample = line.split()
        # Ignore time stamp at the beginning of the line
        danger = int(sample[1])
        x1     = int(sample[2])
        x2     = int(sample[3])
        # Compute output of perceptron and its sign (1 or 2)
        y      = func(w0 + w1*x1 + w2*x2)
        print("x1 = {:4d}, x2 = {:4d}, danger = {:2d}, y = {:6.2f}".
              format(x1, x2, danger, y))
        y = 1 if y > 0 else 2
        # If y does not agree with danger code, adjust the weights
        if y != danger:
            w0 = w0 + eta*x0*y
            w1 = w1 + eta*x1*y
            w2 = w2 + eta*x2*y
        print("New weights = {:4.2f}, {:4.2f}, {:4.2f}".
              format(w0, w1, w2))

print("\nDiscriminant line = {:4.2f} + {:4.2f} x1 + {:4.2f} x2 = 0".
      format(w0, w1, w2))

