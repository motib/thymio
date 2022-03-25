# Activity 7.7

#Not tested  ####

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Locating the nest

SEARCH= 1 
TURNING_SPEED= 200
MOVE_FORWARD= 2
FORWARD_SPEED= 200
THRESHOLD_EXPLORE= 500 
FOLLOW_LINE=3
TURN_RANDOM= 4
WALL_DETECT= 3500 
GO_TO_LIGHT= 5
PREPARE_GO_TO_LIGHT= 6 
LOOK_FOR_LIGHT= 7
TURN_TO_LIGHT= 8
BLACK_COLOR= 400 
THRESHOLD_FOLLOW= 600
SEARCH_BLACK= 9
NEST= 10
SEARCH_BLACK_TWO= 11
GOTO_SEARCH_BLACK= 12 

time_100ms = 0
time_target = 0
turning = 0

accTampon0 = [0,0,0,0]
accTamponPos0 = 0
accTampon1 = [0,0,0,0]
accTamponPos1 = 0
sumacc0 = 0
sumacc1 = 0

#variable for searching the light
acc_max = 0
max_index = 0

#variable for searching the black
_black = 0
start_black = 0

myrand_min = 0   #input for random numbers
myrand_max = 0   #input for random numbers
myrand_res  = 0  #output for random numbers

timer_period[0] = 100 #100ms between each state check of timer0
timer_period[1] = 100 #100ms between each sampling of timer1 

# declaring pseudorandom function myrand
def myrand():
    global myrand_res
    myrand_res = abs(myrand_res % (myrand_max+1 - myrand_min)) + myrand_min

# To start, put robot in front of the light in the nest, front toward the wall
@onevent
def button_forward():
    global status, time_100ms, time_target
    global motor_left_target, motor_right_target
    global myrand_res, myrand_max, myrand_min
    status = NEST
    nf_leds_top(32, 32, 32)
    time_100ms = 0
    motor_left_target = TURNING_SPEED
    motor_right_target = -TURNING_SPEED
    #turning between 90 and 270
    myrand_min=90
    myrand_max=270
    myrand()
    time_target = myrand_res//8  # time to turn

@onevent
def go():
    global status, time_100ms, time_target
    global motor_left_target, motor_right_target
    global myrand_res, myrand_max, myrand_min
    status = NEST
    nf_leds_top(32, 32, 32)
    time_100ms = 0
    motor_left_target = TURNING_SPEED
    motor_right_target = -TURNING_SPEED
    #turning between 90 and 270
    myrand_min=90
    myrand_max=270
    myrand()
    time_target = myrand_res//8  # time to turn

@onevent
def timer1():
    global time_100ms
    time_100ms += 1

@onevent
def timer0():
    global status, time_100ms, time_target, max_index, acc_max
    global motor_left_target, motor_right_target
    global myrand_res, myrand_max, myrand_min, prox_ground_delta
    global accTampon0, accTamponPos0, accTampon1, accTamponPos1
    global sumacc0, sumacc1
    
    if status == NEST:
        if time_100ms > time_target:
            motor_left_target = FORWARD_SPEED
            motor_right_target = FORWARD_SPEED
            status = MOVE_FORWARD
            #moving between 2 and 10s
            myrand_min=20
            myrand_max=100
            myrand()
            time_100ms = 0
            time_target = myrand_res  # time to move
        
        if prox_ground_delta[0]<THRESHOLD_EXPLORE or \
           prox_ground_delta[1]<THRESHOLD_EXPLORE:
            status = FOLLOW_LINE
            nf_leds_top(0, 32, 0)
            motor_left_target = 0
            motor_right_target = 0
            time_100ms = 0

    if status == MOVE_FORWARD:
        if time_100ms > time_target:
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            status = TURN_RANDOM
            #turning between 0 and 360 degrees
            myrand_min=0
            myrand_max=360
            myrand()
            time_100ms = 0
            time_target = myrand_res//8  # time to move
        
        if prox_ground_delta[0]<THRESHOLD_EXPLORE or \
           prox_ground_delta[1]<THRESHOLD_EXPLORE:
            status = FOLLOW_LINE
            nf_leds_top(0, 32, 0)
            motor_left_target = 0
            motor_right_target = 0
            time_100ms = 0
       
        if prox_horizontal[0] > WALL_DETECT or \
           prox_horizontal[1] > WALL_DETECT or \
           prox_horizontal[2] > WALL_DETECT or \
           prox_horizontal[3] > WALL_DETECT or \
           prox_horizontal[4] > WALL_DETECT:
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            status = TURN_RANDOM
            #turning between 90 and 270 degrees
            myrand_min=90
            myrand_max=270
            myrand()
            time_100ms = 0
            time_target = myrand_res//8  # time to move	

    if status == TURN_RANDOM:
        if time_100ms > time_target:
            motor_left_target = FORWARD_SPEED
            motor_right_target = FORWARD_SPEED
            status = MOVE_FORWARD
            #moving between 2 and 10s
            myrand_min=20
            myrand_max=100
            myrand()
            time_100ms = 0
            time_target = myrand_res  # time to move
        
        if prox_ground_delta[0] < THRESHOLD_EXPLORE or \
           prox_ground_delta[1] < THRESHOLD_EXPLORE:
            status = FOLLOW_LINE
            nf_leds_top(0, 32, 0)
            motor_left_target = 0
            motor_right_target = 0
            time_100ms = 0

    if status == FOLLOW_LINE:
       if prox_ground_delta[0] < BLACK_COLOR and \
          prox_ground_delta[1] < BLACK_COLOR:   # it got the food source
          if status < status:
            status = GOTO_SEARCH_BLACK
            nf_leds_top(0, 0, 32)
            motor_left_target = FORWARD_SPEED
            motor_right_target = FORWARD_SPEED
            #move forward a bit
            time_100ms = 0
            time_target = 6  # time to move	(0.6 second)
          elif prox_ground_delta[0] < THRESHOLD_FOLLOW:
            time_100ms = 0
            motor_left_target = 50
            motor_right_target = 120
          elif prox_ground_delta[1]<THRESHOLD_FOLLOW :
            time_100ms = 0
            motor_left_target = 120
            motor_right_target = 50
          elif time_100ms > 50:  #timout -> back in turning
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            status = TURN_RANDOM
            #turning between 0 and 360 degrees
            myrand_min=0
            myrand_max=360
            myrand()
            time_100ms = 0
            time_target = myrand_res//8  # time to move	
            nf_leds_top(32, 32, 32)
        

          if prox_horizontal[0] > WALL_DETECT or \
           prox_horizontal[1] > WALL_DETECT or \
           prox_horizontal[2] > WALL_DETECT or \
           prox_horizontal[3] > WALL_DETECT or \
           prox_horizontal[4] > WALL_DETECT:
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            status = NEST
            nf_leds_top(32, 32, 32)
            #turning between 450 and 630 degrees
            myrand_min=450
            myrand_max=630
            myrand()
            time_100ms = 0
            time_target = myrand_res//8  # time to move	

    if status == GOTO_SEARCH_BLACK:
        if time_100ms > time_target:  #we are turned toward the center of the black
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            time_100ms = 0
            time_target = 48  # time to move (360 degrees)
            status = SEARCH_BLACK
            nf_leds_top(32, 0, 0)

    if status == SEARCH_BLACK:
        if time_100ms > time_target:
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            status = SEARCH_BLACK_TWO
            nf_leds_top(32, 0, 0)
            time_100ms = 0
            time_target = start_black + (46 - start_black + _black)//2 - 3

    if status == SEARCH_BLACK_TWO:
        if time_100ms > time_target:  #we are turned toward the center of the black
            motor_left_target = FORWARD_SPEED
            motor_right_target = FORWARD_SPEED
            status = PREPARE_GO_TO_LIGHT
            nf_leds_top(32, 0, 0)

    # stops if  of the black
    if status == PREPARE_GO_TO_LIGHT:
        if prox_ground_delta[0]>BLACK_COLOR and \
           prox_ground_delta[1]>BLACK_COLOR:
            motor_left_target = 47
            motor_right_target = -47
            time_100ms = 0
            time_target = 360//2  # time to move
            status = LOOK_FOR_LIGHT
            acc_max=0
            max_index = 0

    # turns and records the max value of accelerometers
    if status == LOOK_FOR_LIGHT:
        if time_100ms > time_target:
            motor_left_target = TURNING_SPEED
            motor_right_target = -TURNING_SPEED
            status = TURN_TO_LIGHT
            nf_leds_top(32, 0, 0)
            time_100ms = 0
            time_target = max_index//(TURNING_SPEED//50)
        elif acc[1] >= acc_max:
            acc_max = acc[1]
            max_index = time_100ms

    if status == TURN_TO_LIGHT:
        if time_100ms > time_target:
            motor_left_target = 0
            motor_right_target = 0
            time_100ms = 0
            status = GO_TO_LIGHT

    if status == GO_TO_LIGHT:
            accTampon0[accTamponPos0] = acc[0]-2  #measure lateral tilt
            accTamponPos0 = (accTamponPos0 + 1) % 4
            sumacc0 = accTampon0[0] + accTampon0[1] + accTampon0[2] + accTampon0[3]
            accTampon1[accTamponPos1] = acc[1]     #measure front tilt
            accTamponPos1 = (accTamponPos1 + 1) % 4
            sumacc1 = accTampon1[0] + accTampon1[1] + accTampon1[2] + accTampon1[3]

            if (0<=time_100ms and time_100ms<=12) or \
               (20<=time_100ms and time_100ms<=32) or \
               (40<=time_100ms and time_100ms<=52): 
                # acc0 gives rotation, acc1 gives forward movement	
                motor_left_target=sumacc0*10+sumacc1*10    
                motor_right_target=-sumacc0*10+sumacc1*10
            else:
                motor_left_target=-sumacc0*10-sumacc1*10    
                motor_right_target=sumacc0*10-sumacc1*10
            
            if time_100ms>60:
                time_100ms=0

            if prox_horizontal[0]>WALL_DETECT or \
               prox_horizontal[1]>WALL_DETECT or \
               prox_horizontal[2]>WALL_DETECT or \
               prox_horizontal[3]>WALL_DETECT or \
               prox_horizontal[4]>WALL_DETECT:
                motor_left_target = TURNING_SPEED
                motor_right_target = -TURNING_SPEED
                status = NEST
                nf_leds_top(32, 32, 32)
                #turning between 450 and 630 degrees
                myrand_min=450
                myrand_max=630
                myrand()
                time_100ms = 0
                time_target = myrand_res//8  # time to move	
    