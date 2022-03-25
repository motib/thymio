"""
  Robotic cameleon
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  Input: dark.txt and light.txt left and right sensor
         samples from dark and light areas
  Compute discriminants from means and
    quality criteria J from means and variances
"""

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
    variance_left = sum([(i - mean_left)**2 for i in samples_left]) / (n-1)
    variance_right = sum([(i - mean_right)**2 for i in samples_right]) / (n-1)
    print("Variance {} left ={:6.1f}, variance {} right ={:6.1f}".
          format(label, variance_left, label, variance_right))
    print()

    # Return data as a four-tuple
    return (mean_left, mean_right, variance_left, variance_right)

# Get means and variances for dark and light gray areas
(m_dark_left, m_dark_right, s_dark_left, s_dark_right) = \
              means_and_variances(dark_file,'dark')
(m_light_left, m_light_right, s_light_left, s_light_right) = \
               means_and_variances(light_file,'light')

# Compute discriminants and quality criteria
discriminant_left  = int(m_dark_left  + m_light_left)  // 2
discriminant_right = int(m_dark_right + m_light_right) // 2
quality_left  = (m_dark_left - m_light_left)**2 / \
                (s_dark_left**2 + s_light_left**2)
quality_right = (m_dark_right - m_light_right)**2 / \
                (s_dark_right**2 + s_light_right**2)

# Print and choose discriminant
print("Left  sensor: discriminant ={:5d}, quality criteria = {:7.3f}".
      format(discriminant_left, quality_left))
print("Right sensor: discriminant ={:5d}, quality criteria = {:7.3f}".
      format(discriminant_right, quality_right))
if quality_left > quality_right:
    print("Use left discriminant")
else:
    print("Use right discriminant")
