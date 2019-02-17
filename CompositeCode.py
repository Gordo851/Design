'''
Created on 17 Feb 2019

@author: gordo
'''

import cozmo
import asyncio
from tkinter import *

from cozmo.util import degrees, distance_mm, radians, speed_mmps, Vector2

from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id, Charger
import time
from cozmo import robot

global red_cube
global yellow_cube
global blue_cube
global robot 
robot = cozmo.robot.Robot

# create the code for interaction
def find_charger(robot):
    # create an origin point where Cozmo's charger is. When he picks up objects he will return here.
    # If the robot was on the charger, drive them forward and clear of the charger

    if robot.is_on_charger:
        robot.DriveOffChargerContacts.wait_for_completed()
    if not robot.is_on_charger:
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
        robot.move_lift(-3)
        robot.turn_in_place(degrees(180)).wait_for_completed()
        robot.set_head_angle(degrees(0)).wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()
        time.sleep(0.5)
        
def light_cubes(robot):
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
    
def go_get_cube(robot, cube_selected):
    # look around and try to find a cube
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    if len(cubes) < 3:
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        look_around.stop()
    
    # cozmo goes and gets cube
    if len(cubes) == 3:
        robot.dock_with_cube(cube_selected, approach_angle=cozmo.util.degrees(0), num_retries=2).wait_for_completed
    

    # Cozmo returns cube to user
    robot.go_to_object(Charger,  distance_mm(100)).wait_for_completed()
    robot.say_text("Is ?").wait_for_completed()
    action = robot.place_object_on_ground_here(red_cube).wait_for_completed()
    print("got action", action)
    result = action.wait_for_completed(timeout=30)
    print("got action result", result)
    

    # Object is confirmed
    confirmation1 = input("Is this the right one? Y/N: ")
    if confirmation1 == "Y":
        robot.say_text("Yay")
    else:
        robot.say_text("Well you're getting it anyway.")

    
    # get dat fist bump
    robot.say_text("Do you want me to fetch anything else")

    # user says no

    # cozmo returns to base

    # wait for five minutes of inactivity

    robot.say_text("I'm going to have a nap now, let me know if you need anything?")

    # cozmo returns to cradle and sleeps


def cozmo_program(robot, cube_selected):
    find_charger(robot)
    light_cubes(robot)
    go_get_cube(robot, cube_selected)
    cozmo.run_program(cozmo_program)


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
    label1.config(text=cube_picked)


def yellow_clicked():
    global cube_picked
    cube_picked = "yellow_cube"
    print("yellow")
    label1.config(text=cube_picked)


def blue_clicked():
    global cube_picked
    cube_picked = "blue_cube"
    print("blue")
    label1.config(text=cube_picked)


def confirm_clicked():
    cube_confirmed = cube_picked
    print(cube_confirmed)
    cozmo_program(robot, cube_confirmed)

def create_buttons():
    button1 = Button(root_window, text="      ", bg="yellow", command=yellow_clicked)
    button2 = Button(root_window, text="      ", bg="red", command=red_clicked)
    button3 = Button(root_window, text="      ", bg="blue", command=blue_clicked)
    button4 = Button(root_window, text="Confirm?", command=confirm_clicked)
    global label1
    label1 = Label(root_window, text="Nothing selected yet.")


    button1.grid(row=1, column=2)
    button2.grid(row=3, column=2)
    button3.grid(row=5, column=2)
    label1.grid(row=3, column=4)
    button4.grid(row=3, column=6)

def run_Gui():
    createGui()
    create_buttons()
    red_clicked()
    yellow_clicked()
    blue_clicked()
    label1.config(text="Nothing selected yet.")
    root_window.mainloop()

run_Gui()
"""
    robot.say_text("Ready").wait_for_completed()
    
    # user selects which cube they want
    cube_selected_input = input("Which cube do you want. Options: red_cube, yellow_cube, blue_cube: ")
    cube_selected = cube_selected_input
    print(cube_selected)
    robot.say_text("press").wait_for_completed()

    # Wait for conformation
    confirmation = input("Are you sure Y/N: ")
    if confirmation == "Y":
        robot.say_text("OK.").wait_for_completed()
        robot.move_lift(-3)
        robot.set_head_angle(degrees(0)).wait_for_completed()
        
    else:
        print("Fine")
        cube_wanted = ""
"""



      
    
