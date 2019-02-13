from cozmo.util import degrees, distance_mm, radians, speed_mmps, Vector2
from cozmo.lights import Color, Light

import cozmo


def go_get_cube(robot: cozmo.robot.Robot):
    # cozmo will go get a cube
    robot.say_text("I'll go get that cube")

