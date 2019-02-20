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
def find_charger(robot: cozmo.robot.Robot):
    # create an origin point where Cozmo's charger is. When he picks up objects he will return here.
    # If the robot was on the charger, drive them forward and clear of the charger
    if robot.is_on_charger:
        robot.DriveOffChargerContacts.wait_for_completed()
    if not robot.is_on_charger:
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
        robot.move_lift(-3).wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()
        robot.set_head_angle(degrees(0)).wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()
        time.sleep(0.5)
        robot.SayText("Ready").wait_for_completed()
        
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
    x = 0
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    if len(cubes) < 3:
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    
    # cozmo goes and gets cube
    if len(cubes) == 3:
        look_around.stop()
        robot.abort_all_actions()
        robot.pickup_object(cube_selected, num_retries=3).wait_for_completed()
        x + 1
    
    if x == 1:
        # Cozmo returns cube to user
        robot.abort_all_actions()
        robot.go_to_object(Charger,  distance_mm(100)).wait_for_completed()
        robot.say_text("Is this the right object?").wait_for_completed()
        final_confirmation_of_cube(robot)

def final_confirmation_of_cube(robot: cozmo.robot.Robot):
    # Object is confirmed
    robot.abort_all_actions()
    robot.say_text("Is this the right one?")
    createConfirmationGUI()

def yes_command(robot: cozmo.robot.Robot):
    robot.abort_all_actions()
    robot.move_lift(-5).wait_for_completed()
    robot.say_text("Horray", play_excited_animation=True).wait_for_completed()
    robot.drive_straight(distance_mm(-200), speed_mmps(50)).wait_for_completed()

def no_command(robot: cozmo.robot.Robot):
    robot.abort_all_actions()
    robot.drive_straight(distance_mm(-200), speed_mmps(50)).wait_for_completed()
    robot.move_lift(-5).wait_for_completed()
    robot.say_text("Select something else and I'll get it.").wait_for_completed()

def createConfirmationGUI():
    confirmationWindow = Tk()
    confirmationWindow.geometry("300x100")
    buttonYES = Button(confirmationWindow, text="YES", bg="green", command=yes_command, height = 4, width = 17)
    buttonNO = Button(confirmationWindow, text="NO", bg="red", command=no_command, height = 4, width = 17)
    buttonNO.grid(row = 2, column = 1)
    buttonYES.grid(row = 2, column = 2)
    confirmationWindow.mainloop()

def cozmo_stuff(robot: cozmo.robot.Robot, cube_selected):
    find_charger(robot)
    go_get_cube(robot, cube_selected)

def dropoff_point(robot: cozmo.robot.Robot):
    robot.abort_all_actions()


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
    print("red")
    label1.config(text="selected TV remote (red)")


def yellow_clicked():
    global cube_picked
    cube_picked = "yellow_cube"
    print("yellow")
    label1.config(text="selected phone (yellow)")
    
def blue_clicked():
    global cube_picked
    cube_picked = "blue_cube"
    print("blue")
    label1.config(text="selected medication (blue)")

def confirm_clicked():
    cube_confirmed = cube_picked
    print(cube_confirmed)

def create_buttons():
    button1 = Button(root_window, text="", bg="yellow", command=yellow_clicked, height = 4, width = 17)
    button2 = Button(root_window, text="", bg="red", command=red_clicked, height = 4, width = 17)
    button3 = Button(root_window, text="", bg="blue", command=blue_clicked, height = 4, width = 17) 
    button5 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button6 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button7 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button8 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button9 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button10 = Button(root_window, text="", bg="grey", height = 4, width = 17)
    button4 = Button(root_window, text="confirm?", command=confirm_clicked, height = 4, width = 17)
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
    robot.SayText("Getting ready")
    
def run_Gui():
    cozmo.run_program(cozmo_program)
    light_cubes(cozmo.robot.Robot)
    createGui()
    create_buttons()
    red_clicked()
    yellow_clicked()
    blue_clicked()
    label1.config(text="Nothing selected yet.")
    root_window.mainloop()

run_Gui()
