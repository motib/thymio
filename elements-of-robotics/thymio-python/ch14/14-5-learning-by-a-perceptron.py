# Activity 14.5

# Copyright 2017, 2022 by Moti Ben-Ari
# CreativeCommons BY-SA 3.0

# Learning by a perceptron

# Touch the forward button to sample not dangerous
# Touch the back button to sample dangerous

# Export a code (1 or 2) and the acc values
#   Right click on the event "accelerometers" and select plot
#   Click the "plot of ground" tab to display the plot window
#   Click "Save as"
# To clear before next run
#   Click "Clear" below the bottom right pane 
#   Click clear in the plot window

@onevent
def button_forward():
  if button_forward == 0:
    emit("accelerometers", 1, acc[1], acc[2])
  

@onevent
def button_backward():
  if button_backward == 0:
    emit("accelerometers", 2, acc[1], acc[2])
