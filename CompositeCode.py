'''
Created on 17 Feb 2019

@author: gordo
'''

import cozmo
from tkinter import *

from cozmo.util import degrees, distance_mm, speed_mmps, Pose

from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id, Charger
import time
from cozmo import robot
from time import sleep

global red_cube
global yellow_cube
global blue_cube
global cube_picked
global x
global y

# create the code for interaction
def light_cubes(robot: cozmo.robot.Robot):
    robot.say_text("I'm just getting ready").wait_for_completed()
    global x 
    global cube_picked
    global y
    x = ""
    y = ""
    robot.say_text("Ok I'm looking for your stuff. When it lights up I've found it").wait_for_completed()
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()
    red_light = cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 0, 0)))
    blue_light = cozmo.lights.Light(cozmo.lights.Color(rgb=(0, 0, 255)))
    yellow__light = cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 255, 0)))
    
    # tag each cube found as a different colour
    red_cube = robot.world.get_light_cube(LightCube1Id)
    blue_cube = robot.world.get_light_cube(LightCube2Id)
    yellow_cube = robot.world.get_light_cube(LightCube3Id)

    red_cube.set_lights(red_light)
    blue_cube.set_lights(blue_light)
    yellow_cube.set_lights(yellow__light)   
    
    robot.say_text("Ok, pick one and then press confirm and I'll get it for you").wait_for_completed()
    
    global root_window;
    root_window = Tk()
    
    button1 = Button(root_window, text="Phone", bg="yellow", command=yellow_clicked, height = 4, width = 17)
    button2 = Button(root_window, text="TV Remote", bg="red", command=red_clicked, height = 4, width = 17)
    button3 = Button(root_window, text="Medication", bg="light blue", command=blue_clicked, height = 4, width = 17) 
    button5 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button6 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button7 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button8 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button9 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button10 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    global button4
    button4 = Button(root_window, text="Cozmo is waiting", command=confirm_clicked, height = 4, width = 20)
    global label1
    label1 = Label(root_window, text="Nothing selected yet.",height = 4, width = 25)
    button1.grid(row = 1, column = 1)
    button2.grid(row = 1, column = 2)
    button3.grid(row = 1, column = 3)
    button5.grid(row = 2, column = 1)
    button6.grid(row = 2, column = 2)
    button7.grid(row = 2, column = 3)
    button8.grid(row = 3, column = 1)
    button9.grid(row = 3, column = 2)
    button10.grid(row = 3, column = 3)
    label1.grid(row = 2, column = 4)
    button4.grid(row = 2, column = 5)
    root_window.mainloop()
    while x == "":
        sleep(1)
    
    if x == "Blue":
        cube_picked = blue_cube
    
    elif x == "Red":
        cube_picked = red_cube
    
    elif x == "Yellow":
        cube_picked = yellow_cube
    
    targ = cube_picked

    if len(cubes) < 3:
        print("Error")
    else:
        robot.pickup_object(targ, num_retries=3).wait_for_completed()
        robot.go_to_pose(Pose(0, 0, 0, angle_z=degrees(180)), relative_to_robot=False).wait_for_completed()
        robot.say_text("Is this the right one?").wait_for_completed()
        global confirmationWindow
        confirmationWindow = Tk()
        confirmationWindow.geometry("255x70")
        buttonYES = Button(confirmationWindow, text="YES", bg="green", command=yes_command, height = 4, width = 17)
        buttonNO = Button(confirmationWindow, text="NO", bg="red", command=no_command, height = 4, width = 17)
        buttonNO.grid(row = 2, column = 1)
        buttonYES.grid(row = 2, column = 2)
        confirmationWindow.mainloop()
        
    while y == "":
        sleep(1)
        
    if y == "yes":
        robot.say_text("YAY", play_excited_animation=True).wait_for_completed()
        robot.move_lift(-3)
        robot.drive_straight(distance_mm(-200), speed_mmps(80)).wait_for_completed()

    elif y == "no":
        robot.drive_straight(distance_mm(-200), speed_mmps(50)).wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()
        robot.move_lift(-5)
        robot.go_to_pose(Pose(0, 0, 0, angle_z=degrees(180)), relative_to_robot=False).wait_for_completed()
        robot.say_text("Select something else and I'll get it.").wait_for_completed()
        exit

def light_cubes2(robot: cozmo.robot.Robot):
    global x 
    global cube_picked
    global y
    x = ""
    y = ""
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()
    red_light = cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 0, 0)))
    blue_light = cozmo.lights.Light(cozmo.lights.Color(rgb=(0, 0, 255)))
    yellow__light = cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 255, 0)))
    
    # tag each cube found as a different colour
    red_cube = robot.world.get_light_cube(LightCube1Id)
    blue_cube = robot.world.get_light_cube(LightCube2Id)
    yellow_cube = robot.world.get_light_cube(LightCube3Id)

    red_cube.set_lights(red_light)
    blue_cube.set_lights(blue_light)
    yellow_cube.set_lights(yellow__light)   
    
    robot.say_text("Ok, pick one and then press confirm and I'll get it for you").wait_for_completed()
    
    global root_window;
    root_window = Tk()
    
    button1 = Button(root_window, text="Phone", bg="yellow", command=yellow_clicked, height = 4, width = 17)
    button2 = Button(root_window, text="TV Remote", bg="red", command=red_clicked, height = 4, width = 17)
    button3 = Button(root_window, text="Medication", bg="light blue", command=blue_clicked, height = 4, width = 17) 
    button5 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button6 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button7 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button8 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button9 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button10 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    global button4
    button4 = Button(root_window, text="Cozmo is waiting", command=confirm_clicked, height = 4, width = 20)
    global label1
    label1 = Label(root_window, text="Nothing selected yet.",height = 4, width = 25)
    button1.grid(row = 1, column = 1)
    button2.grid(row = 1, column = 2)
    button3.grid(row = 1, column = 3)
    button5.grid(row = 2, column = 1)
    button6.grid(row = 2, column = 2)
    button7.grid(row = 2, column = 3)
    button8.grid(row = 3, column = 1)
    button9.grid(row = 3, column = 2)
    button10.grid(row = 3, column = 3)
    label1.grid(row = 2, column = 4)
    button4.grid(row = 2, column = 5)
    root_window.mainloop()
    while x == "":
        sleep(1)
    
    if x == "Blue":
        cube_picked = blue_cube
    
    elif x == "Red":
        cube_picked = red_cube
    
    elif x == "Yellow":
        cube_picked = yellow_cube
    
    targ = cube_picked

    if len(cubes) < 3:
        print("Error")
    else:
        robot.pickup_object(targ, num_retries=3).wait_for_completed()
        robot.go_to_pose(Pose(0, 0, 0, angle_z=degrees(180)), relative_to_robot=False).wait_for_completed()
        robot.say_text("Is this the right one?").wait_for_completed()
        global confirmationWindow
        confirmationWindow = Tk()
        confirmationWindow.geometry("255x70")
        buttonYES = Button(confirmationWindow, text="YES", bg="green", command=yes_command, height = 4, width = 17)
        buttonNO = Button(confirmationWindow, text="NO", bg="red", command=no_command, height = 4, width = 17)
        buttonNO.grid(row = 2, column = 1)
        buttonYES.grid(row = 2, column = 2)
        confirmationWindow.mainloop()
        
    while y == "":
        sleep(1)
        
    if y == "yes":
        robot.say_text("ay", play_excited_animation=True).wait_for_completed()
        robot.move_lift(-5)
        robot.drive_straight(distance_mm(-200), speed_mmps(80)).wait_for_completed()

    elif y == "no":
        robot.drive_straight(distance_mm(-200), speed_mmps(50)).wait_for_completed()
        robot.move_lift(-5)
        robot.say_text("Select something else and I'll get it.").wait_for_completed()
        exit

        
def yes_command():
    global y
    confirmationWindow.destroy()
    y = "yes"
    return y

def no_command():
    global y
    confirmationWindow.destroy()
    y = "no"
    return y

def red_clicked():
    label1.config(text="selected TV remote (red)")
    button4.config(text="Press to confirm")
    button4.config(bg="red")
    global x
    x = "Red"
    return x

def yellow_clicked():
    label1.config(text="selected phone (yellow)")
    button4.config(text="Press to confirm")
    button4.config(bg="yellow")
    global x
    x = "Yellow"
    return x

def blue_clicked():
    label1.config(text="selected medication (blue)")
    button4.config(text="Press to confirm")
    button4.config(bg="light blue")
    global x
    x = "Blue"
    return x

def confirm_clicked():
    button4.config(text="Cozmo will be back soon!")
    button4.config(bg="white")
    
def run_Gui():
    #cozmo.run_program(cozmo_program)
    cozmo.run_program(light_cubes)

def run_Gui2():
    cozmo.run_program(light_cubes2)
    
run_Gui()
run_Gui2()
