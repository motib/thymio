"""
  Neural network for spatial filtering
  Copyright 2017 Moti Ben-Ari and Francesco Mondada
  CreativeCommons BY-SA

  This program simulates a neural network with five
  inputs for the sensors and five outputs obtaining
  after using weights. Then the outputs are weighted
  to compute power settings for the left and right motors.

  Compute for constant sensor value detected by:
    one sensor, all five sensors, three center sensors.
  For one sensor, the robot turns in the direction of
    the sensor.
  For three or five sensors, the robot moves backwards.
"""

# Declare lists for neuron inputs and outputs
inputs   = [0,0,0,0,0]
outputs  = [0,0,0,0,0]

# Declare and initialize lists for neuron weights
neuron_weights = [
    [4,-4,0,0,0],
    [-2,4,-2,0,0],
    [0,-2,4,-2,0],
    [0,0,-2,4,-2],
    [0,0,0,-4,4]
  ]

# Declare and initialize lists for left and right motor weights
motor_weights = [
    [-7,-4,3,4,7],
    [7,4,3,-4,-7]
  ]

# Declare bias for motor powers to obtain backwards motion
motor_bias = 0

# Scale factors
neuron_scale     = 8
motor_scale      = 3
motor_bias_scale = 6

# Print the neuron and motor weights
def print_weights():
    global neuron_weights, motor_weights
    print("****************************")
    print("Neural network configuration")
    print("****************************")
    print("Neuron weights")
    for i in range(len(neuron_weights)):
        print(neuron_weights[i])
    print("Left  motor weights\n",   motor_weights[0],
          "\nRight motor weights\n", motor_weights[1],
          sep='', end='\n\n')

# Dot product of lists a and b divided by scale
def dot(a,b,scale):
    c = 0
    for i in range(len(a)):
        c += a[i]*b[i]
    return c // scale

# Compute the output of the neurons:
#   dot product of inputs and neuron weights
# Outputs must not be negative
def compute_outputs():
    global neuron_weights, inputs, outputs
    print("Inputs  = ", inputs)
    for i in range(len(inputs)):
        outputs[i] = dot(inputs, neuron_weights[i], neuron_scale)
        if outputs[i] < 0: outputs[i] = 0
    print("Outputs = ", outputs)

# Compute the motor powers:
#   dot product of neuron outputs and motor weights
# Apply motor_bias to decrease the motor powers
#   so that the robot can move backwards
def compute_motors():
    global outputs, motor_weights, motor_bias
    left = dot(outputs, motor_weights[0], motor_scale)
    left -= motor_bias
    right = dot(outputs, motor_weights[1], motor_scale)
    right -= motor_bias
    print("Motor left =", left, ", motor right =", right, '\n')

# Compute neuron outputs and then motor powers
# Motor bias is the sum of the inputs divided by a scale factor
def compute_outputs_and_motors():
    global inputs, motor_bias, motor_bias_scale
    outputs = compute_outputs()
    motor_bias = sum(inputs) // motor_bias_scale
    print("Motor bias = ", motor_bias)
    compute_motors()

# Compute outputs and motor powers for each detection possibility
def run(sensor_value):
    global inputs
    print("*********************************")
    print("Motor outputs for a single sensor")
    print("Sensor value = ", sensor_value)
    print("*********************************")

    inputs = [sensor_value,0,0,0,0]
    compute_outputs_and_motors()

    inputs = [0,sensor_value,0,0,0]
    compute_outputs_and_motors()

    inputs = [0,0,sensor_value,0,0]
    compute_outputs_and_motors()

    inputs = [0,0,0,sensor_value,0]
    compute_outputs_and_motors()

    inputs = [0,0,0,0,sensor_value]
    compute_outputs_and_motors()

    print("**********************************")
    print("Motor outputs for multiple sensors")
    print("Sensor value = ", sensor_value)
    print("**********************************")

    inputs = [sensor_value,sensor_value,sensor_value,sensor_value,sensor_value]
    compute_outputs_and_motors()

    inputs = [0,sensor_value,sensor_value,sensor_value,0]
    compute_outputs_and_motors()

# Run for different sensor values
print_weights()
run(400)
run(200)
