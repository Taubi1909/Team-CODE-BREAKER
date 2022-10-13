from djitellopy import TelloSwarm
from queue import Queue
import time

def s_movement(command: str, swarm_contol):  # handling commands send by the GUI
    if command == "up":
        swarm_contol.move_up(50)
    elif command == "down":
        swarm_contol.move_down(50)
    elif command == "forward":
        swarm_contol.move_forward(50)
    elif command == "backward":
        swarm_contol.move_back(50)
    elif command == "left":
        swarm_contol.move_left(50)
    elif command == "right":
        swarm_contol.move_right(50)
    elif command == "rotate_l":
        swarm_contol.rotate_counter_clockwise(90)
    elif command == "rotate_r":
        swarm_contol.rotate_clockwise(90)
    elif command == "land":
        swarm_contol.land()
    elif command == "flip_back":
        swarm_contol.streamoff()
        time.sleep(1)
        swarm_contol.flip_back()
        time.sleep(1)
        swarm_contol.streamon()
    elif command == "flip_forward":
        swarm_contol.streamoff()
        time.sleep(1)
        swarm_contol.flip_forward()
        time.sleep(1)
        swarm_contol.streamon()
    elif command == "flip_right":
        swarm_contol.streamoff()
        time.sleep(1)
        swarm_contol.flip_right()
        time.sleep(1)
        swarm_contol.streamon()
    elif command == "flip_left":
        swarm_contol.streamoff()
        time.sleep(1)
        swarm_contol.flip_left()
        time.sleep(1)
        swarm_contol.streamon()
    elif command == "start":
        swarm_contol.takeoff()
    elif command == "dance":
        swarm_contol.move_left(50)
        swarm_contol.move_right(100)
        swarm_contol.move_left(50)
        swarm_contol.rotate_clockwise(360)
    elif command == "emergency":
        swarm_contol.emergency()
    elif command == "jump":
        swarm_contol.move_up(50)
        swarm_contol.move_down(50)
