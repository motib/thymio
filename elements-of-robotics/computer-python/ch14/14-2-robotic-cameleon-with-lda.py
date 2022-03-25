"""
  Robotic cameleon with LDA
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  Input: dark.txt and light.txt left and right sensor
         samples from dark and light areas
  Compute linear discriminant analysis equation
    w1x1 + w2x2 = c
"""

###########################################################
# Functions for computations on 2x2 matrices and vectors

# Print a matrix is two rows of two columns
def print_matrix(m):
    print("{:10.4f} {:10.4f} ".format(m[0][0], m[0][1]))
    print("{:10.4f} {:10.4f} ".format(m[1][0], m[1][1]))
    print()

# Print a column vector
def print_vector(v):
    print("{:10.5f} ".format(v[0]))
    print("{:10.5f} ".format(v[1]))
    print()

# Add two matrices
def add_matrix(m1, m2):
    return [[m1[0][0]+m2[0][0], m1[0][1]+m2[0][1]],
            [m1[1][0]+m2[1][0], m1[1][1]+m2[1][1]]]

# Multiply a matrix by a scalar
def scalar_multiply_matrix(c, m):
    return [[c*m[0][0], c*m[0][1]], [c*m[1][0], c*m[1][1]]]

# Multiply a matrix by a vector
def matrix_vector_multiply(m,v):
    return [m[0][0]*v[0]+m[0][1]*v[1], m[1][0]*v[0]+m[1][1]*v[1]]

# Invert a matrix
def invert_matrix(m):
    det = m[0][0] * m[1][1] - m[0][1] * m[0][1]
    return scalar_multiply_matrix(
        1.0/det,
        [[m[1][1], -m[0][1]], [-m[1][0], m[0][0]]])

###########################################################

dark_file  = "dark.txt"
light_file = "light.txt"

# Compute means and variances from samples
def means_and_variances(file_name,label):
    # Open file and initialize lists of samples
    print("Data from", label, "samples")
    samples_left = []
    samples_right = []

    # Read each line and separate into first and second samples
    with open(file_name) as f:
        for line in f:
            sample = line.split()
            # Ignore time stamp at the beginning of the line
            samples_left.append(int(sample[1]))
            samples_right.append(int(sample[2]))

    # Compute number of samples
    n = len(samples_left)

    # Compute means
    mean_left = sum(samples_left) // n
    mean_right = sum(samples_right) // n
    print("Mean {} left     ={:6d}, mean {} right     ={:6d}".
          format(label, mean_left, label, mean_right))

    # Compute variances
    variance_left  = sum([(i - mean_left)**2 for i in samples_left]) / (n-1)
    variance_right = sum([(i - mean_right)**2 for i in samples_right]) / (n-1)
    print("Variance {} left ={:6.1f}, variance {} right ={:6.1f}".
          format(label, variance_left, label, variance_right))

    # Compute the covariance
    pairs = list(zip(samples_left,samples_right))
    covariance = sum([(p[0] - mean_left)*(p[1] - mean_right)
                      for p in pairs]) / (n-1)
    print("Covariance {} = {:10.4f}".format(label, covariance))

    # Construct the covariance matrix
    covariance_matrix  = [
        [variance_left, covariance],
        [covariance, variance_right]]
    print("Covariance matrix {}:".format(label)) 
    print_matrix(covariance_matrix)

    # Return means and covariance matrix
    return ([mean_left, mean_right], covariance_matrix)

###########################################################

# Get means and covariance matrices for dark and light gray areas
(mean_dark,  cv_dark)  = means_and_variances(dark_file,'dark')
(mean_light, cv_light) = means_and_variances(light_file,'light')

# Compute the average of the covariance matrices
average_cv = scalar_multiply_matrix(0.5,
                                    add_matrix(cv_dark,cv_light))
print("Average of covariance matrices:")
print_matrix(average_cv)

# Invert the average of the covariance matrices
inverse_cv = invert_matrix(average_cv)
print("Inverse of average of covariance matrices:")
print_matrix(inverse_cv)

# Compute weights from inverse corvariance average and
#   difference of means
diff_mean = [mean_light[0] - mean_dark[0],
             mean_light[1] - mean_dark[1]]
w = matrix_vector_multiply(inverse_cv, diff_mean)
print("W:")
print_vector(w)

# Compute constant term from the average of the means
average_mean = [0.5*(mean_light[0] + mean_dark[0]),
                0.5*(mean_light[1] - mean_dark[1])]
print("Average mean:")
print_vector(average_mean)

c = w[0]*average_mean[0] + w[1]*average_mean[1]
print("C = {:6.2f}\n".format(c))

# Print the equation for the discriminant line
print("Discriminant line:")
print("{:8.4f} x1  +{:8.4f} x2  =  {:8.4f}".
      format(w[0], w[1],c))
