# Activity 14.3

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Obstacle avoidance with two sensors

# Touch right and left buttons to sample
#   when the wall is detected on the right side, turn left
#   when the wall is detected on the left side, turn right
# Export:
#   button touched (1=left, 2=right)
#   average of two left sensors
#   average of the two right sensors

# Export the average values of the left and right sensors
#   Right click on the event "left_right" and select plot
#   Click the "plot of ground" tab to display the plot window
#   Click "Save as"
# To clear before next run
#   Click "Clear" below the bottom right pane 
#   Click clear in the plot window

@onevent
def button_left():
  if button_left == 0:
    emit("left_right", 1, \
                     (prox_horizontal[0]+prox_horizontal[1])//2, \
                     (prox_horizontal[3]+prox_horizontal[4])//2 )

@onevent
def button_right():
  if button_right == 0:
    emit("left_right", 2, \
                     (prox_horizontal[0]+prox_horizontal[1])//2, \
                     (prox_horizontal[3]+prox_horizontal[4])//2 )
  