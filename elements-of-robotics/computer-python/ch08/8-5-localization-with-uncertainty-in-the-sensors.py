"""
  Probablistic localization
  Copyright 2017 by Moti Ben-Ari
  CreativeCommons BY-SA

  Computes the tables in Section 9.3 of
  Ben-Ari and Mondada, Elements of Robotics, Springer
"""

#  Initial belief array:
#    uniform distribution of the robot's location
uniform = [1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8]

#  There are doors at positions 0,1,4,5,6
#    but with uncertainty in sensing
p = [.9, .9, .1, .1, .9, .9, .9, .1]

#  Uncertainty in motion:
#    [Remains in place, moves 1 position right, moves 2 positions right
q = [.1, .8, .1]

#  Multiply belief array a by the uncertainty of sensing p
def multiply_prob(a):
    for i in range(len(p)):
        a[i] = round(a[i]*p[i], 4)
    return a

#  Move belief array a right (cyclic)
def move_right(a):
    temp = a[len(a)-1];
    for i in reversed(range(1, len(a))):
        a[i] = a[i-1]
    a[0] = temp
    return a

#  Move belief array a right (cyclic) with uncertaity of motion q
def move_right_uncertain(a):
    temp1 = a[len(a)-1];
    temp2 = a[len(a)-2];
    for i in reversed(range(1, len(a))):
        a[i] = a[i]*q[0] + a[i-1]*q[1] + a[i-2]*q[2]
    a[0] = a[0]*q[0] + temp1*q[1] + temp2*q[2]
    return a

#  Normalize probabilities in believe array a
def normalize(a):
    sum = 0
    for i in range(len(a)):
        sum = sum + a[i]
    for i in range(len(a)):
        a[i] = round(a[i] / sum, 4)
    return a

#  Print belief array a with prefix label s
def print_array(s, a):
    print (s,end='')
    for i in range(len(a)):
        print (round(a[i], 2), '', end='')
    print ()
    
#  Print out tables
#  Initialize belief array b with uniform distribution
b = uniform
print_array ("uniform  ", b)
print ()

#  Three moves of the robot:
#  Mulitply by probability, normalize, move right
print ("Sensors with uncertainty, move without uncertainty")
for i in range(3):
    b = multiply_prob(b)
    print_array("multiply ", b)
    b = normalize(b)
    print_array("norm     ", b)
    b = move_right(b)
    print_array("right    ", b)
    print ()

#  Three moves of the robot:
#  Mulitply by probability, normalize, move right with uncertainty
print ("Sensors with uncertainty, move with uncertainty")
for i in range(3):
    b = multiply_prob(b)
    print_array("multiply ", b)
    b = normalize(b)
    print_array("norm     ", b)
    b = move_right_uncertain(b)
    print_array("right    ", b)
    print ()
