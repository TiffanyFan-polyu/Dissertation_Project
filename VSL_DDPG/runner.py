from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import numpy as np
import random


SUMO_HOME = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", SUMO_HOME), "tools"))
import traci  # noqa
import sumolib  # noqa

sumoCmd = ["D:/Program Files (x86)/Eclipse/bin/sumo", "-c", "llcd.sumocfg", "--num-clients", "2"]
traci.start(sumoCmd, port=9999)
traci.setOrder(1)
#traci.start([sumolib.checkBinary('sumo-gui'), "-c", "llcd.sumocfg"] + sys.argv[1:])
simulationSteps=0
# VSLlist = ['gneE1_0','gneE1_1','gneE1_2']
# v = 30 *np.ones(3,)
# control_step=1
# with open('vsl_control.txt', 'r') as f:  # 打开文件
#     lines = f.readlines()  # 读取所有行
#     for control_step in range(1,360):
#         v = lines[control_step]
#         v_float = list(map(float, v.split()))
#         # print(control_step, v_float)
#         # print(v_float[1])


while simulationSteps < 3600:

    # set max velocity per lane
    # number_of_lane = len(VSLlist)
    #
    # for j in range(number_of_lane):
    #     traci.lane.setMaxSpeed(VSLlist[j], v_float[j])

    # vehid_new = traci.vehicle.getIDList()
    # vehid = vehid_new
    # for veh in vehid:
    #     randomNum = np.random.uniform()
    #     if randomNum < 0.4 and traci.vehicle.getLanePosition(veh) < 100 and traci.vehicle.getRouteID(veh)[0:3] == "!RF":
    #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
    #         # print(randomNum, "randomNum <0.4 and traci.vehicle.getLanePosition(veh) < 100")
    #     if 0.4 <= randomNum < 0.8 and traci.vehicle.getLanePosition(veh) < 200 and traci.vehicle.getRouteID(veh)[
    #                                                                                0:3] == "!RF":
    #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
    #         # print(randomNum, "0.4<=randomNum<0.8 and traci.vehicle.getLanePosition(veh) < 200")
    #     if randomNum >= 0.8 and traci.vehicle.getLanePosition(veh) < 300 and traci.vehicle.getRouteID(veh)[
    #                                                                          0:3] == "!RF":
    #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
    #         # print(randomNum, "randomNum>=0.8 and traci.vehicle.getLanePosition(veh) < 300")
    #     else:
    #         traci.vehicle.setLaneChangeMode(veh, 0b011001010101)
    # vehid_old = vehid_new

    # for i in range(1,10):
    #     # control_step += 1
    traci.simulationStep()
    simulationSteps += 1
    #print(simulationSteps)


        ############## assign a random num for lane change diistribution #################

    # vehid = traci.vehicle.getIDList()
    # for veh in vehid:
    #     randomNum = random.random()
    #     # print(randomNum)
    #     if randomNum < 0.4 and traci.vehicle.getLanePosition(veh) < 100 and traci.vehicle.getRouteID(veh)[
    #                                                                         0:3] == "!RF":
    #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
    #         # print(randomNum,"randomNum <0.4 and traci.vehicle.getLanePosition(veh) < 100")
    #     if 0.4 <= randomNum < 0.8 and traci.vehicle.getLanePosition(veh) < 200 and traci.vehicle.getRouteID(veh)[
    #                                                                                0:3] == "!RF":
    #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
    #         # print(randomNum,"0.4<=randomNum<0.8 and traci.vehicle.getLanePosition(veh) < 200")
    #     if randomNum >= 0.8 and traci.vehicle.getLanePosition(veh) < 300 and traci.vehicle.getRouteID(veh)[
    #                                                                          0:3] == "!RF":
    #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
    #         # print(randomNum,"randomNum>=0.8 and traci.vehicle.getLanePosition(veh) < 300")
    #     else:
    #         traci.vehicle.setLaneChangeMode(veh, 0b011001010101)
    #         # print("else")



traci.close()
fname = 'output_sumo.xml'
print("with lane change control")
with open(fname, 'r') as f:  # 打开文件
   lines = f.readlines()  # 读取所有行
   last_line = lines[-2]  # 取最后一行
nPos=last_line.index('meanTravelTime=')
aat_tempo = float(last_line[nPos+16:nPos+21])
# 打开“laneData.xml"
laneData = 'laneData.xml'
with open(laneData, 'r') as f:  # 打开文件
    lines = f.readlines()  # 读取所有行
    for lane in range(3):
        mainlane = lines[lane+51]  # 取gne1那三行
        traveltimePos = mainlane.index('traveltime=')
        waitingTimePos = mainlane.index('waitingTime=')
        speedPos = mainlane.index('speed=')
        lane_traveltime = mainlane[traveltimePos + 12:traveltimePos + 17]
        lane_waitingTime = mainlane[waitingTimePos + 13:waitingTimePos + 19]
        lane_speed = mainlane[speedPos + 7:speedPos + 12]
        print('mainlane', lane, ': traveltime=', lane_traveltime, 'waitingTime=', lane_waitingTime, 'speed=',
              lane_speed)
print('Average Travel Time: %.4f' % aat_tempo)




# print("vehicletypes", traci.vehicletype.getIDList())
# print("vehicletype count", traci.vehicletype.getIDCount())
# typeID = "DEFAULT_VEHTYPE"
# print("examining", typeID)
# vehID=traci.vehicle.getIDList()
# print(vehID)
# print("vehicletype", traci.vehicle.getTypeID(vehID[0]))
# traci.vehicle.setType(vehID[0],'vType_0')
# print("vehicletype", traci.vehicle.getTypeID(vehID[0]))
# print("...................>>>>>>>>>>>>>>.........................")

"""
print("inductionloops", traci.inductionloop.getIDList())
print("inductionloop count", traci.inductionloop.getIDCount())
loopID = "myLoop10"
print("examining", loopID)
for step in range(20,32):
    print("step", step)
    traci.simulationStep()

print("step=%s detVehs=%s vehData=%s" % (traci.simulation.getTime(),traci.inductionloop.getLastStepVehicleIDs(loopID),traci.inductionloop.getVehicleData(loopID),))
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
LastID=traci.inductionloop.getLastStepVehicleIDs(loopID)
print(LastID)
print("vehicletype", traci.vehicle.getTypeID(LastID[0]))
traci.vehicle.setType(LastID[0],'vType_0')
print("vehicletype", traci.vehicle.getTypeID(LastID[0]))
traci.simulationStep()
"""

#traci.vehicletype.setParameter(typeID,"lcStrategic","100")
#print("laneChangeMode", traci.vehicle.getLaneChangeMode())
 
"""
traci.vehicletype.subscribe(typeID)
print(traci.vehicletype.getSubscriptionResults(typeID))
for step in range(3, 6):
    print("step", step)
    traci.simulationStep()
    print(traci.vehicletype.getSubscriptionResults(typeID))
traci.vehicletype.setLength(typeID, 1.0)
print("length", traci.vehicletype.getLength(typeID))
traci.vehicletype.setMaxSpeed(typeID, 1.0)
print("maxSpeed", traci.vehicletype.getMaxSpeed(typeID))
"""

# traci.simulationStep()

