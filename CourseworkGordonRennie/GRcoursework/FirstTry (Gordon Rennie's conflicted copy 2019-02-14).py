import cozmo
import asyncio
from tkinter import *

from cozmo.util import degrees, distance_mm, radians, speed_mmps, Vector2

from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import time
"""
# create the GUI for interaction
root_window = Tk()
cube_colour_picked = "Nothing selected yet"
cube_colour_confirmed = "Nothing selected yet"
a_string = "Nothing selected yet"


def red_clicked():
    global cube_picked
    cube_picked = red_cube
    print("red")
    label1.config(text=cube_colour_picked)


def yellow_clicked():
    global cube_picked
    cube_picked = "yellow_cube"
    print("green")
    label1.config(text=cube_colour_picked)


def blue_clicked():
    global cube_picked
    cube_picked = "blue_cube"
    print("blue")
    label1.config(text=cube_colour_picked)


def confirm_clicked():
    global cube_confirmed
    global cube_picked
    cube_confirmed = cube_picked
    print(cube_confirmed)


button1 = Button(root_window, text="      ", bg="yellow", command=yellow_clicked)
button2 = Button(root_window, text="      ", bg="red", command=red_clicked)
button3 = Button(root_window, text="      ", bg="blue", command=blue_clicked)
button4 = Button(root_window, text="Confirm?", command=confirm_clicked)
label1 = Label(root_window, text="Nothing selected yet.")

button1.grid(row=1, column=0)
button2.grid(row=2, column=0)
button3.grid(row=3, column=0)
label1.grid(row=2, column=1)
button4.grid(row=2, column=2)

root_window.mainloop()
"""


# create the code for interaction
def cozmo_program(robot: cozmo.robot.Robot):
    # create an origin point where Cozmo's charger is. When he picks up objects he will return here.
    # If the robot was on the charger, drive them forward and clear of the charger
    if robot.is_on_charger:
        robot.drive_off_charger_contacts().wait_for_completed()
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
        robot.move_lift(-3)
        robot.turn_in_place(degrees(180)).wait_for_completed()
        robot.set_head_angle(degrees(0)).wait_for_completed()
        time.sleep(0.5)

    # try to find the charger
    charger = None

    if robot.world.charger:
        if robot.world.charger.pose.is_comparable(robot.pose):
            # Cozmo knows where the charger is
            charger = robot.world.charger
        else:
            pass

    if not charger:
        # Tell Cozmo to look around for the charger
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try:
            charger = robot.world.wait_for_observed_charger(timeout=30)
        except asyncio.TimeoutError:
            print("Didn't see the charger")
        finally:
            look_around.stop()



    # on boot up show loading screen


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

    # Pass found objects to GUI for selection

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
        cube_wanted = cube_selected
    else:
        print("Fine")
        cube_wanted = ""

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # look around and try to find a cube
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    look_around.start()
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
        
    look_around.stop()
    
    # cozmo goes and gets cube
    robot.pickup_object(yellow_cube, num_retries=3).wait_for_completed
    
    robot.say_text("Got it").wait_for_completed()


    # Cozmo returns cube to user
    robot.go_to_object(charger,  distance_mm(100)).wait_for_completed()
    robot.say_text("Is this one the right one?").wait_for_completed()

    # Object is confirmed
    confirmation1 = input("Is this the right one? Y/N: ")
    if confirmation1 == "Y":
        robot.say_text("Yay")
    else:
        robot.say_text("Well you're getting it anyway.")

    action = robot.place_object_on_ground_here(cube_wanted)
    action.wait_for_completed()

    # get dat fist bump
    robot.say_text("Do you want me to fetch anything else")

    # user says no

    # cozmo returns to base

    # wait for five minutes of inactivity

    robot.say_text("I'm going to have a nap now, let me know if you need anything?")

    # cozmo returns to cradle and sleeps

"""
cozmo.connect(run)
cozmo.run_program(cozmo_program)
