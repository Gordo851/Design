
from cozmo.util import degrees, distance_mm, radians, speed_mmps, Vector2

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import time


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

    origin = charger
    robot.go_to_object(origin, 70)

    # on boot up show loading screen

    # locate all cubes
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    look_around.stop()

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

    robot.say_text("Ready when you are").wait_for_completed()

    # user selects which cube they want
    cube_selected = input("Which cube do you want. Options: red_cube, yellow_cube, blue_cube: ")
    robot.say_text("When you are sure that's the one you want. Press the tick, if you want to select another, \
                   just press on another object").wait_for_completed()

    # Wait for conformation
    confirmation = input("Are you sure Y/N: ")
    if confirmation == "Y":
        robot.say_text("OK, I'll be right back.").wait_for_completed()
        cube_wanted = cube_selected
    else:
        print("Fine then.")
        cube_wanted = ""

    # cozmo goes and gets cube
    action = robot.go_to_object(red_cube, distance_mm(70.0))
    action.wait_for_completed()
    action = robot.dock_with_cube(cube_wanted, approach_angle=cozmo.util.degrees(0), num_retries=2)
    action.wait_for_completed()
    action = robot.pickup_object(cube_wanted, num_retries=3)
    action.wait_for_completed()
    robot.say_text("Got it").wait_for_completed()

    # Cozmo returns cube to user
    action = robot.go_to_object(origin,  distance_mm(70))
    action.wait_for_completed()
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


cozmo.run_program(cozmo_program)

