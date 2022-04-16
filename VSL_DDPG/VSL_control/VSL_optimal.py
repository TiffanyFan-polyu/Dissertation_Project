#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import traci.constants as tc


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step=0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        #print(step)
        veh_id= traci.vehicle.getIDList()
        while step in range(20,30):
            print(step)

         
            

        
            #print(veh_id)
            #traci.vehicle.setSpeed(veh_id, 0)

         
    #traci.vehicle.subscribe(1, (tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION))
    #print(traci.vehicle.getSubscriptionResults(1))
    #for step in range(3):
        #print("step", step)
        #traci.simulationStep()
        #print(traci.vehicle.getSubscriptionResults(1))

    traci.close()

#!/usr/bin/python3 
"""
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(step) 
        
        det_vehs = traci.inductionloop.getLastStepVehicleIDs("myLoop10")
        #for veh in det_vehs:
            #print(veh)
            #traci.vehicle.setSpeed(veh, 0)

        if step == 20:
             traci.vehicle.setSpeed(flow_0.7, 0)
             traci.vehicle.setSpeed(flow_2.0, 0)
             #traci.vehicle.changeTarget("3", "e9")

        step += 1

    traci.close()
    sys.stdout.flush()
"""

 
# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "llcd.sumocfg",])
    run()