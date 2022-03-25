# Activity 2-5b

# Copyright 2013, 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Compose music on-the-fly using the robot as a controller

# Touch the center button to start sampling
# Touch again to start music
# Store the left-right and front-back acceleration and
#   generate sound from the results:
# Left-right for the note and front-back for the duration

save0 = [0,0,0,0,0,0,0,0]  # array to store left-right samples
save1 = [0,0,0,0,0,0,0,0]  # array to store front-back samples
index = 0     # array index
state = 0     # state

# The notes middle C to high C in hertz
notes = [261, 294, 330, 349, 392, 440, 494, 523]

# milliseconds between samples
timer_period[1] = 500
 
# When the center button is released, start sampling
@onevent
def button_center():
  global index, state
  if  button_center == 0:
    if  state == 0:
      index = 0
      state = 1
    elif  state == 2:
      state = 3
      index = 0
      nf_sound_freq(0,1)
    elif  state == 3:
      state = 0
      nf_sound_freq(0,-1)

# On timer expiration, save left-right and front-back samples
# When all samples are saved, initiate the sounds
@onevent
def timer1():
  global index, state, save0, save1
  if  state == 1:
    if  index < len(save0):
      save0[index] = acc[0]
      save1[index] = acc[1]
      index += 1
    else:
      state = 2
      print("Composition finished")
 
# When a sound is finished, start the next one
@onevent
def sound_finished():
  global state, index
  if  state == 3:
    if  index < len(save0):
      nf_sound_freq(notes[(save0[index]+32) % 8], save1[index]+33)
      index += 1
    else:
      state = 0

# Correlate state and top leds
# Use prox event just to have it occur frequently
@onevent
def prox():
  if  state == 0:
    nf_leds_top(0,0,0)
  if  state == 1:
    nf_leds_top(32,0,0)
  if  state == 2:
    nf_leds_top(0,32,0)
  if  state == 3:
    nf_leds_top(0,0,32)

  if  acc[0] >= 0:
    left = 32
  else:
    left = 0
  if  acc[1] >= 0:
    down = 32
  else:
    down = 0

  nf_leds_circle(32-down, 0, 32-left, 0, down, 0, left, 0)
