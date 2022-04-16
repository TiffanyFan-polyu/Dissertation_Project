#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 00:24:19 2018

@author: wuyuankai
"""

from __future__ import division
import os
import sys
import numpy as np
import random

#tools = '/usr/share/sumo/tools'
tools = 'D:/Program Files (x86)/Eclipse/tools'
sys.path.append(tools)
import traci

sumoConfig = "llcd.sumocfg"
#sumoConfig = "floating_car.sumocfg"
print("111111111111111111111111111111")
class rm_vsl_co(object):
    '''ff
    this is a transportation network for training multi-lane variable speed limit and ramp metering control agents
    the simulation is running on sumo
    '''
    def __init__(self, test = False, visualization = False, control_horizon = 30, incidents = False):
        
        '''
        OD Parameters
        '''
        self.m1flow = np.round(np.array([3359+640,6007+1229,5349+1080,5563+1139,5299+1107]))
        self.r3flow = np.round(np.array([480,1153,1129,1176,1095]))
        self.m1a = [0.75,0.25]
        self.v_ratio = [0.1,0.1,0.4,0.4]
        print("init----------------------")
        self.veh_RF = []

        '''
        Network Parameters
        '''
        self.edges = ['m3 m4 m5 m6 m7 m8 m9',\
                 'm3 m4 m5 m6 m7 m8 rout1',\
                 'rlight1 rin3 m7 m8 m9']        
        self.control_section = 'm6'
        self.state_detector = ['onramp','in1','in2','myLoop1','myLoop6','myLoop11','myLoop16','myLoop21','myLoop26','myLoop31',\
                               'mainline1','mainline6','mainline11','mainline16','mainline21','mainline26','mainline31',\
                               'mostleft1','mostleft6','mostleft11','mostleft16','mostleft21','mostleft26','mostleft31']
        # self.state_detector = [ 'myLoop1', 'myLoop6', 'myLoop11', 'myLoop16', 'myLoop21',\
        #                        'mainline1', 'mainline6', 'mainline11', 'mainline16', 'mainline21',\
        #                        'mostleft1', 'mostleft6', 'mostleft11', 'mostleft16', 'mostleft21']
        self.VSLlist = ['gneE1_0','gneE1_1','gneE1_2']
        self.inID = ['onramp','in1','in2']
        self.outID = ['offramp','out1','out2']
        self.bottleneck_detector = ['myLoop6','myLoop11','myLoop16',\
                                     'mainline6','mainline11','mainline16']
        # self.bottleneck_detector = ['myLoop6','myLoop7','myLoop8']   ##auxilary lane pos=50,60,70
        
        '''
        Simulation Parameters
        '''
        self.simulation_hour = 1   #hours
        self.simulation_step = 0
        self.control_horizon = control_horizon  #seoncs
        self.test = test
        self.visualization = visualization
        if self.visualization == False:
            self.sumoBinary = "D:/Program Files (x86)/Eclipse/bin/sumo"
        else:
            #self.sumoBinary = "/usr/bin/sumo-gui"
            self.sumoBinary = "D:/Program Files (x86)/Eclipse/bin/sumo-gui"
            print("sumo-gui----------------------")
        self.incidents = incidents
        if self.incidents == False:
            self.incident_time = 2000000
            self.incident_length = 10000000  # it will never happened
        else:
            self.incident_time = np.random.randint(low = 1, high = self.simulation_hour * 3600 - 1800)
            self.incident_length = np.random.randint(low = 1, high = 600)
                
    def writenewtrips(self): 
        with open('fcd.rou.xml', 'w') as routes:
            routes.write("""<routes>""" + '\n')
            routes.write('\n')
            routes.write("""<vType id="type0" color="255,105,180" length = "8.0" speedFactor="normc(1,0.1,0.2,2)" lcSpeedGain = "1"/>""" + '\n')
            routes.write("""<vType id="type1" color="255,190,180" length = "8.0" carFollowModel = "IDM" speedFactor="normc(1,0.1,0.2,2)" lcSpeedGain = "1"/>""" + '\n')
            routes.write("""<vType id="type2" color="22,255,255" length = "3.5" speedFactor="normc(1,0.1,0.2,2)" lcSpeedGain = "1"/>""" + '\n')
            routes.write("""<vType id="type3" color="22,55,255" length = "3.5" carFollowModel = "IDM" speedFactor="normc(1,0.1,0.2,2)" lcSpeedGain = "1"/>""" + '\n')
            routes.write('\n')
            for i in range(len(self.edges)):
                routes.write("""<route id=\"""" + str(i) + """\"""" + """ edges=\"""" + self.edges[i] + """\"/> """ + '\n')
            temp = 0
            for hours in range(len(self.m1flow)):
                m_in = np.random.poisson(lam = int(self.m1flow[hours,]))
                r3_in = np.random.poisson(lam = int(self.r3flow[hours,]))
                vNum = m_in + r3_in
                dtime = np.random.uniform(0+3600*hours,3600+3600*hours,size=(int(vNum),))            
                dtime.sort()
                for veh in range(int(vNum)):
                    typev = np.random.choice([0,1,2,3], p = self.v_ratio)
                    vType = 'type' + str(typev)
                    route = np.random.choice([0,1,2], p =[m_in*self.m1a[0]/vNum, m_in*self.m1a[1]/vNum, r3_in/vNum])
                    routes.write("""<vehicle id=\"""" + str(temp+veh) + """\" depart=\"""" + str(round(dtime[veh],2)) + """\" type=\"""" + str(vType) + """\" route=\"""" + str(route) + """\" departLane=\""""'random'"""\"/>""" + '\n')        
                    routes.write('\n')
                temp+=vNum
            routes.write("""</routes>""")
        # reset incidents
            
    #####################  obtain state  #################### a
    def get_step_state(self):
        state_occu = []
        for detector in self.state_detector:
            occup = traci.inductionloop.getLastStepOccupancy(detector)
            if occup == -1:
                occup = 0
            state_occu.append(occup)
        return np.array(state_occu)

    #####################  obtain speed state  #################### a
    def get_step_state2(self):
        state_speed = []
        for detector in self.state_detector:
            speed = traci.inductionloop.getLastStepMeanSpeed(detector)
            state_speed.append(speed)
        return np.array(state_speed)

    #####################  set speed limit  #################### 
    def set_vsl(self, v):
        number_of_lane = len(self.VSLlist)
        for j in range(number_of_lane):
            traci.lane.setMaxSpeed(self.VSLlist[j], v[j])

    #####################  set vehicle speed limit  ####################
    def set_section_vsl(self, v):
        for veh in traci.vehicle.getIDList():
            #if traci.vehicle.getLanePosition(veh) <= 400:
                if traci.vehicle.getLaneID(veh)=="gneE1_0":
                    traci.vehicle.setMaxSpeed(veh, v[0])
                    #print("v[0]:",v[0])
                if traci.vehicle.getLaneID(veh) == "gneE1_1":
                    traci.vehicle.setMaxSpeed(veh, v[1])
                    #print("v[1]:", v[1])
                if traci.vehicle.getLaneID(veh) == "gneE1_2":
                    traci.vehicle.setMaxSpeed(veh, v[2])
                    #print("v[2]:", v[2])
            
    #####################  the out flow ####################
    def calc_outflow(self):
        state = []
        statef = []
        for detector in self.outID:
            veh_num = traci.inductionloop.getLastStepVehicleNumber(detector)
            state.append(veh_num)
        for detector in self.inID:
            veh_num = traci.inductionloop.getLastStepVehicleNumber(detector)
            statef.append(veh_num)
        return np.sum(np.array(state)) - np.sum(np.array(statef))
    
    #####################  the bottleneck speed ####################  
    def calc_bottlespeed(self):
        speed = []
        for detector in self.bottleneck_detector:
            dspeed = traci.inductionloop.getLastStepMeanSpeed(detector)
            if dspeed < 0:
                dspeed = 5                                              
                #The value of no-vehicle signal will affect the value of the reward
            speed.append(dspeed)
        return np.mean(np.array(speed))

    
    #####################  the CO, NOx, HC, PMx emission  #################### 
    def calc_emission(self):
        vidlist = traci.edge.getIDList()
        co = []
        hc = []
        nox = []
        pmx = []
        for vid in vidlist:
            co.append(traci.edge.getCOEmission(vid))
            hc.append(traci.edge.getHCEmission(vid))
            nox.append(traci.edge.getNOxEmission(vid))
            pmx.append(traci.edge.getPMxEmission(vid))
        return np.sum(np.array(co)),np.sum(np.array(hc)),np.sum(np.array(nox)),np.sum(np.array(pmx))
    
    #####################  a new round simulation  #################### 
    def start_new_simulation(self, write_newtrips = True):
        print("new simulation--------------------")
        self.simulation_step = 0
        if write_newtrips == True:
            self.writenewtrips()
        sumoCmd = [self.sumoBinary, "-c", sumoConfig, "--start"]
        traci.start(sumoCmd)

        # connect to omnet ##
        # sumoCmd = [self.sumoBinary, "-c", sumoConfig,"--num-clients", "2"]
        # traci.start(sumoCmd, port=9999)
        # traci.setOrder(1)

    #####################  assign a weaving length when new RF enters  s####################

    # def enter_RF(self):
    #     # veh_RF = []
    #     zone_length = [0, 100, 200, 300]
    #     prop_RF = [0, 0.4, 0.8, 1]
    #     for idveh in traci.vehicle.getIDList():
    #         if traci.vehicle.getRouteID(idveh)[0:3] == "!RF":
    #             randomNum = random.random()
    #             assigned_len = next(zone_length[i] for i in range(len(prop_RF)) if randomNum < prop_RF[i])
    #
    #
    #             # for i in [x[0] for x in self.veh_RF]:
    #             #     if i not in self.veh_RF:
    #             #         self.veh_RF.append((i, assigned_len))
    #             #         print(self.simulation_step,self.veh_RF)
    #
    #             # if assigned_len > 0 and not all(i in idveh for i in [x[0] for x in self.veh_RF]):
    #             #     print(idveh)
    #             #     self.veh_RF.append((idveh, assigned_len))
    #             #     print(self.veh_RF)
    #
    #             # if assigned_len > 0 and idveh not in ("".join([x[0] for x in self.veh_RF])):
    #             if assigned_len > 0 and idveh not in self.veh_RF:
    #
    #                 print(idveh)
    #                 self.veh_RF.append((idveh, assigned_len))
    #                 # print(self.veh_RF)
    #
    #
    #     return self.veh_RF


    #####################  run one step: reward is outflow  ####################
    def  run_step(self, v):
        state_overall = 0
        reward = 0
        oflow = 0
        bspeed = 0
        s_reward = 0
        self.set_vsl(v)  ## set max velocity per lane
        #self.set_section_vsl(v)
        #print(v)
        for i in range(self.control_horizon):
            traci.simulationStep()
            self.simulation_step += 1
            # print(self.simulation_step)

            # ### assign a fix random rumber ####
            # for veh in traci.vehicle.getIDList():
            #     if traci.vehicle.getRouteID(veh)[0:3] == "!RF":
            #         randomNum = random.random()
            #         assigned_len = next(zone_length[i] for i in range(len(prop_RF)) if randomNum < prop_RF[i])
            #         if assigned_len > 0 and veh not in [x[0] for x in self.veh_RF]:
            #             # print(randomNum)
            #             self.veh_RF.append((veh, assigned_len))
            #             # print((veh, assigned_len))
            #     for idveh, assigned_len in self.veh_RF:
            #         if veh == idveh and traci.vehicle.getLanePosition(veh) < assigned_len:
            #             traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
            #             # print(veh, assigned_len, traci.vehicle.getLanePosition(veh), "i cannot change")
            #         if veh == idveh and traci.vehicle.getLanePosition(veh) >= assigned_len:
            #             traci.vehicle.setLaneChangeMode(veh, 0b011001010101)
            #             # print(veh, assigned_len, traci.vehicle.getLanePosition(veh), "i can change lanes")
            #             # self.enter_RF().remove((idveh,assigned_len))
            #             # self.enter_RF().append((idveh,0))
            # ### assign a fix random rumber ---end ####


           #assign a random num for lane change distribution##
            # vehid = traci.vehicle.getIDList()
            # for veh in vehid:
            #     randomNum = np.random.uniform()
            #     if randomNum < 0.4 and traci.vehicle.getLanePosition(veh) < 100 and traci.vehicle.getRouteID(veh)[0:3] == "!RF":
            #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
            #         #print(randomNum, "randomNum <0.4 and traci.vehicle.getLanePosition(veh) < 100")
            #     if 0.4 <= randomNum < 0.8 and traci.vehicle.getLanePosition(veh) < 200 and traci.vehicle.getRouteID(veh)[0:3] == "!RF":
            #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
            #         #print(randomNum, "0.4<=randomNum<0.8 and traci.vehicle.getLanePosition(veh) < 200")
            #     if randomNum >= 0.8 and traci.vehicle.getLanePosition(veh) < 300 and traci.vehicle.getRouteID(veh)[0:3] == "!RF":
            #         traci.vehicle.setLaneChangeMode(veh, 0b001000000000)
            #         #print(randomNum, "randomNum>=0.8 and traci.vehicle.getLanePosition(veh) < 300")
            #     else:
            #         traci.vehicle.setLaneChangeMode(veh, 0b011001010101)
            #         #print("else")


            ## 在某一随机时刻，随机选一辆车速度设置为0 ##
            if self.simulation_step == self.incident_time:
                vehid = traci.vehicle.getIDList()
                r_tempo = np.random.randint(0, len(vehid) - 1)
                self.inci_veh = vehid[r_tempo]
                print(self.inci_veh,r_tempo)
                self.inci_edge = traci.vehicle.getRoadID(self.inci_veh) # get incident edge
            if self.simulation_step > self.incident_time and self.simulation_step < self.incident_time + self.incident_length:
                traci.vehicle.setSpeed(self.inci_veh, 0)                       # set speed as zero, to simulate incidents
            state_overall = state_overall + self.get_step_state()  ##获取state：occupancy
            oflow = oflow + self.calc_outflow()
            bspeed = bspeed + self.calc_bottlespeed()
            # print(self.simulation_step)
           # print(self.calc_bottlespeed(),bspeed)
        #print(self.calc_bottlespeed(), bspeed)
             # the reward is defined as the outflow

        #reward = reward + s_reward
        # reward = reward + oflow/80 * 0.1 + bspeed/(30*self.control_horizon)*0.9  ##why 80/30?
        #reward = reward  + bspeed / self.control_horizon
        reward = reward + oflow
        return state_overall/self.control_horizon/100, reward, self.simulation_step, oflow, bspeed/self.control_horizon
    
    def close(self):
        traci.close()


    print("222222222222222222222222222222")