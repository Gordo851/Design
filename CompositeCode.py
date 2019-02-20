'''
Created on 17 Feb 2019

@author: gordo
'''

import cozmo
from tkinter import *

from cozmo.util import degrees, distance_mm, speed_mmps

from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id, Charger
import time

global red_cube
global yellow_cube
global blue_cube
# create the code for interaction
def light_cubes(robot: cozmo.robot.Robot):
    # define light colours
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
    
def go_get_cube(robot: cozmo.robot.Robot, cube_selected):
    # look around and try to find a cube
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()
    for cube in cubes:
        if cube == cube_selected:            
            robot.abort_all_actions()
            robot.pickup_object(cube_selected, num_retries=3).wait_for_completed()
    robot.go_to_object(Charger,  distance_mm(100)).wait_for_completed()
    robot.say_text("Is this the right object?").wait_for_completed()
    final_confirmation_of_cube(robot)

def final_confirmation_of_cube(robot: cozmo.robot.Robot):
    # Object is confirmed
    robot.say_text("Is this the right one?")
    createConfirmationGUI()

def yes_command(robot: cozmo.robot.Robot):
    confirmationWindow.destroy()
    robot.abort_all_actions()
    robot.say_text("Horray", play_excited_animation=True).wait_for_completed()
    robot.move_lift(-5).wait_for_completed()
    robot.drive_straight(distance_mm(-200), speed_mmps(80)).wait_for_completed()

def no_command(robot: cozmo.robot.Robot):
    confirmationWindow.destroy()
    robot.abort_all_actions()
    robot.drive_straight(distance_mm(-200), speed_mmps(50)).wait_for_completed()
    robot.move_lift(-5).wait_for_completed()
    robot.say_text("Select something else and I'll get it.").wait_for_completed()

def createConfirmationGUI():
    global confirmationWindow
    confirmationWindow = Tk()
    confirmationWindow.geometry("255x70")
    buttonYES = Button(confirmationWindow, text="YES", bg="green", command=yes_command, height = 4, width = 17)
    buttonNO = Button(confirmationWindow, text="NO", bg="red", command=no_command, height = 4, width = 17)
    buttonNO.grid(row = 2, column = 1)
    buttonYES.grid(row = 2, column = 2)
    confirmationWindow.mainloop()

def createGui():
# create the GUI for interaction
    global root_window;
    root_window = Tk()
    global cube_colour_picked;
    cube_colour_picked = "Nothing selected yet"
    global cube_colour_confirmed;
    cube_colour_confirmed = "Nothing selected yet"
    global a_string;
    global cube_confirmed
    global cube_picked

def red_clicked():
    global cube_picked
    cube_picked = "red_cube"
    label1.config(text="selected TV remote (red)")
    button4.config(text="Press to confirm")
    button4.config(bg="red")

def yellow_clicked():
    global cube_picked
    cube_picked = "yellow_cube"
    label1.config(text="selected phone (yellow)")
    button4.config(text="Press to confirm")
    button4.config(bg="yellow")
    
def blue_clicked():
    global cube_picked
    cube_picked = "blue_cube"
    label1.config(text="selected medication (blue)")
    button4.config(text="Press to confirm")
    button4.config(bg="light blue")

def back_soon(robot: cozmo.robot.Robot):
    robot.say_text("Just give me a minute", True)

def confirm_clicked():
    cube_confirmed = cube_picked
    button4.config(text="Cozmo will be back soon!")
    back_soon()
    button4.config(bg="white")
    print(cube_confirmed)
    go_get_cube(cube_confirmed)

def create_buttons():
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

def cozmo_program(robot: cozmo.robot.Robot):
    if robot.is_on_charger:
        robot.DriveOffChargerContacts.wait_for_completed()
    if not robot.is_on_charger:
        robot.SayText("Getting ready")
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
        robot.move_lift(-3).wait_for_completed()
        time.sleep(0.5)
        robot.SayText("Ready").wait_for_completed()

def run_Gui():
    cozmo.run_program(cozmo_program)
    light_cubes(cozmo.robot.Robot)
    createGui()
    create_buttons()
    root_window.mainloop()

run_Gui()

