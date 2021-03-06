# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19990)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import math
import numpy as np

from car import Car


try:
    from api import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')
    


import time

#==========================================================================================================================================================================================================

#==========================================================================================================================================================================================================
#


print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19990,True,True,5000,5) # Connect to CoppeliaSim

while(clientID == -1):
    print("waiting for cimulation to start ...")
    time.sleep(1)
    clientID=sim.simxStart('127.0.0.1',19990,True,True,5000,5) # Connect to CoppeliaSim

if clientID!=-1:
    print ('Connected to remote API server')

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(clientID,'Hello from python!',sim.simx_opmode_oneshot)


    

    return_value, leftWheelFront = sim.simxGetObjectHandle(clientID, 'leftMotor', sim.simx_opmode_blocking)
    return_value, leftWheelBack = sim.simxGetObjectHandle(clientID, 'leftMotor_back', sim.simx_opmode_blocking)
    return_value, rightWheelFront = sim.simxGetObjectHandle(clientID, 'rightMotor', sim.simx_opmode_blocking)
    return_value, rightWheelBack = sim.simxGetObjectHandle(clientID, 'rightMotor_back', sim.simx_opmode_blocking)
    
    return_value, carBody = sim.simxGetObjectHandle(clientID, 'RobotBase', sim.simx_opmode_blocking)

    wheels = [leftWheelFront, rightWheelFront, leftWheelBack, rightWheelBack]

    return_value, leftSensorFront = sim.simxGetObjectHandle(clientID, 'Proximity_sensor_front_left', sim.simx_opmode_blocking)
    return_value, leftSensorBack = sim.simxGetObjectHandle(clientID, 'Proximity_sensor_back_left', sim.simx_opmode_blocking)

    return_value, rightSensorFront = sim.simxGetObjectHandle(clientID, 'Proximity_sensor_front_right', sim.simx_opmode_blocking)
    return_value, rightSensorBack = sim.simxGetObjectHandle(clientID, 'Proximity_sensor_back_right', sim.simx_opmode_blocking)

    return_value, rightSensor = sim.simxGetObjectHandle(clientID, 'Proximity_sensor_right', sim.simx_opmode_blocking)
    return_value, leftSensor = sim.simxGetObjectHandle(clientID, 'Proximity_sensor_left', sim.simx_opmode_blocking)
    
    sensors = [leftSensorFront, leftSensorBack, rightSensorFront, rightSensorBack, rightSensor, leftSensor]

    return_value, detectionState, detectionPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, leftSensorFront, sim.simx_opmode_streaming)
    
    car = Car(sensors, wheels, carBody, clientID)


    #car.square()
    #car.run()
    #car.test_ride()
    #car.map.set_map_for_testing()
    #car.ride_from_point_to_point(car.map.currentPosition, [1, 8])



    car.mapping_run()
    print("======================================================")
    print("============        MAPPING FINISHED         =========")
    print("======================================================")
    while True:

        print("what should car do now?")
        print(" [1] - travel to random point on map")
        print(" [2] - let me decide where car will travel")
        print(" [3] - die")
        print(" [4] - (print map again)")

        menu_choice = input("> ")
        print("your choice is: " + str(menu_choice))

        if menu_choice == 1:
            print("brr picking random point from map ...")
            car.ride_from_point_to_point(car.map.currentPosition, car.map.randomDiscoveredPosition())
            
        if menu_choice == 2:
            print("input desired point coordinates: ")
            x = input("x => ")
            y = input("y => ")
            print("choosen point: x={0}, y={1} ".format(x, y))
            car.ride_from_point_to_point(car.map.currentPosition, [y, x])

        if menu_choice == 3:
            print("car is dead :c")
            break

        if menu_choice == 4:
            car.map.print_pretty(car.direction)

        else:
            print("come again?")
            continue
    


    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')





