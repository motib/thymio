timer_period[1] = 500

def print_horizontal():
    print('prox_horizontal',
          prox_horizontal[0], prox_horizontal[1],
          prox_horizontal[2], prox_horizontal[3],
          prox_horizontal[4],
          prox_horizontal[5], prox_horizontal[6])

def print_ground():
    print('prox_ground_delta',
          prox_ground_delta[0], prox_ground_delta[1])

def print_accelerometers():
    print('acc: roll = ', acc[0],
          'pitch = ', acc[1],
          'vertical = ', acc[2])

@onevent
def timer1():
    print_horizontal()
    print_ground()
    print_accelerometers()
