//
// Copyright (C) 2016 David Eckhoff <david.eckhoff@fau.de>
//
// Documentation for these modules is at http://veins.car2x.org/
//
// SPDX-License-Identifier: GPL-2.0-or-later
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//

#include "veins/modules/application/traci/MyVeinsAppRSU.h"
#include "veins/modules/application/traci/BeaconRSU_m.h"
#include <fstream>
#include<iostream>
#include<string>

using namespace veins;

Define_Module(veins::MyVeinsAppRSU);

void MyVeinsAppRSU::initialize(int stage)
{
    numSent = 0;
    count= 0;
    WATCH(numSent);

    DemoBaseApplLayer::initialize(stage);
    if (stage == 0) {
        sendBeacon= new cMessage("send Beacon");
        EV << "Initializing " << par("appName").stringValue() << std::endl;

//        std::cout<<"读取 vsl_control.txt"<<endl;
//        std::ifstream infile("vsl_control.txt", std::ios::in);
//        while(getline(infile,s));
//        std::cout<<s<<endl;
//        std::string s;
//        if (!infile.fail())
//        {
//            while(count<=10)
//            {
//                count++;
//                getline(infile,s);
//                std::cout<<count<<endl;
//                std::cout<<s<<endl;
//            }
//            getline(infile,s);
//            std::cout<<s<<endl;

//        }

//        infile.close();

    }
    else if (stage == 1) {
        // Initializing members that require initialized other modules goes here
        if (sendBeacon->isScheduled())
        {
            cancelEvent(sendBeacon);
        }
        scheduleAt(simTime(),sendBeacon);
    }
}

void MyVeinsAppRSU::handleSelfMsg(cMessage* msg)
{
    // read "vsl_control.txt", and get one line every control step.
    std::ifstream infile("vsl_control.txt", std::ios::in);
    std::cout<<count<<endl;
    if (count%30==0)
    {
    for(i=0;i<=count/30;i++)
        {
            getline(infile,s);
        }
    }
    std::cout<<s<<endl;
    count++;
    const char * speedLimit = s.c_str();

//    std::stringstream ss(s);
//    double lane1;
//    double lane2;
//    double lane3;
//    ss >> lane1;
//    ss >> lane2;
//    ss >> lane3;
//    std::cout<<lane1<<endl;
//    std::cout<<lane2<<endl;
//    std::cout<<lane3<<endl;
//    TraCIMobility* mobility = TraCIMobilityAccess().get(getParentModule());
//    TraCICommandInterface* traci = mobility->getCommandInterface();
//    TraCICommandInterface::Vehicle* traciVehicle = mobility->getVehicleCommandInterface();
//    traci->lane("gneE1_0").getMaxSpeed();
//    traci->lane("gneE1_1").setMaxSpeed(lane2);
//    traci->lane("gneE1_2").setMaxSpeed(lane3);



    EV << myId << std::endl;
    // this method is for self messages (mostly timers)
    // it is important to call the DemoBaseApplLayer function for BSM and WSM transmission
    if (msg == sendBeacon){

        BeaconRSU* rsuBeacon = new BeaconRSU();
        rsuBeacon->setRSUId(this->getParentModule()->getIndex());
        rsuBeacon->setMyDemoData(speedLimit);
        //新建WSM，这是应用层和MAC层通信的消息
        BaseFrame1609_4* WSM = new BaseFrame1609_4();
        //把rsuBeacon封装在WSM中
        WSM->encapsulate(rsuBeacon);
        //设置WSM的基本信息
        populateWSM(WSM);
        send(WSM,lowerLayerOut);
        numSent++;
        //sendDown(WSM);
        EV << "rsu send success" <<endl;
        //if (simTime() < 2000) {
        scheduleAt(simTime()+1, sendBeacon);
        //}
        return;
    }
    //DemoBaseApplLayer::handleSelfMsg(msg);
}



void MyVeinsAppRSU::finish()
{
    DemoBaseApplLayer::finish(  );
    // statistics recording goes here
    EV << "00000000000000000000000000000000000002222222222222222222222222222222222222222222 " << std::endl;
    EV << "Sent: " << numSent << endl;
    recordScalar("#sent", numSent);

}

/*
void MyVeinsAppRSU::onBSM(DemoSafetyMessage* bsm)
{
    // Your application has received a beacon message from another car or RSU
    // code for handling the message goes here
    EV << " 0000000000000000000000000000000000000333333333333333333333333333333333333333333" << std::endl;

}

void MyVeinsAppRSU::onWSM(BaseFrame1609_4* wsm)
{
    // Your application has received a data message from another car or RSU
    // code for handling the message goes here, see TraciDemo11p.cc for examples
    EV << "0000000000000000000000000000000000000000000444444444444444444444444444444444444444" << std::endl;

}

void MyVeinsAppRSU::onWSA(DemoServiceAdvertisment* wsa)
{
    // Your application has received a service advertisement from another car or RSU
    // code for handling the message goes here, see TraciDemo11p.cc for examples
    EV << "00000000000000000000000000000000000000000000000055555555555555555555555555555555555555555 " << std::endl;

}

*/
//void MyVeinsAppRSU::handlePositionUpdate(cObject* obj)
//{
//    EV << " 00000000000000000000000000000000000000888888888888888888888888888888888888888" << std::endl;
//
//    DemoBaseApplLayer::handlePositionUpdate(obj);
//    std::cout<<"读取 vsl_control.txt"<<endl;
//    std::ifstream infile("vsl_control.txt", std::ios::in);
//    std::string s;
//    if (!infile.fail())
//    {
////            while(getline(infile,s))
////            {
////                std::cout<<s<<endl;
////            }
//       getline(infile,s);
//       std::cout<<s<<endl;
//       std::cout<<"handlePositionUpdate"<<endl;
//
//    }
//
//    infile.close();
//
//    // the vehicle has moved. Code that reacts to new positions goes here.
//    // member variables such as currentPosition and currentSpeed are updated in the parent class
//}


//void MyVeinsAppRSU::handleLowerMsg(cMessage* msg)
//{
//    EV << " 00000000000000000000000000000000000000000000999999999999999999999999999999999999999999" << std::endl;
//    findHost()->getDisplayString().updateWith("r=25,yellow");
//    EV << "receive Car message  !!!" << endl;
//}

