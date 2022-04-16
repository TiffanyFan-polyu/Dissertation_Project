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

#include "veins/modules/application/traci/MyVeinsAppCar.h"
#include "veins/modules/application/traci/BeaconRSU_m.h"
#include "veins/modules/application/traci/MyVeinsAppRSU.h"
#include<string>
#include<sstream>
#include<vector>

using namespace veins;

Define_Module(veins::MyVeinsAppCar);

void MyVeinsAppCar::initialize(int stage)
{
    numReceived = 0;
    numRF = 0;
    numFR = 0;
    numLost = 0;
    WATCH(numReceived);

    DemoBaseApplLayer::initialize(stage);
    //change = par("change").boolValue();
    if (stage == 0) {
        // Initializing members and pointers of your application goes here
        EV << "Initializing " << par("appName").stringValue() << std::endl;
        //int a = INT_MIN;
    }
    else if (stage == 1) {
        // Initializing members that require initialized other modules goes here
        RSUIndex.setName("test");
        //int a= INT_MIN;
        EV << "MyVeinsAppCar is initializing" << std::endl;
        //EV << "11111111111111111111111111111111111111111111111111111111" << std::endl;


    }
}

void MyVeinsAppCar::handleLowerMsg(cMessage* msg)
{

    randomNum = uniform(0,1);
    EV << "randomNum = " << randomNum <<endl;

    if( randomNum < 0.4 & traciVehicle->getLanePosition()< 50 & traciVehicle->getRouteId().substr(0,4)=="!RF." )
    {
        //EV << "I cannot change lanes I'm RF and on the section 1" << endl;
        traciVehicle->setLaneChangeMode(0b001000000000);
    }
    else if ( 0.4<=randomNum<0.8 & traciVehicle->getLanePosition()<100 & traciVehicle->getRouteId().substr(0,4)=="!RF.")
    {
        //EV << "I cannot change lane until reach 200m" << endl;
        traciVehicle->setLaneChangeMode(0b001000000000);
    }
    else if ( randomNum >= 0.8 & traciVehicle->getLanePosition()<200 & traciVehicle->getRouteId().substr(0,4)=="!RF.")
    {
        //EV << "I cannot change lane until reach 300m" << endl;
        traciVehicle->setLaneChangeMode(0b001000000000);
    }
    else
    {
        //EV << "I can change lanes 1111111111111111111111111111111111" << endl;
        traciVehicle->setLaneChangeMode(0b011001010101);
    }


    if( uniform(0,1) <0.85)   //packet lost probability
    {
        //findHost()->getDisplayString().updateWith("r=6,red");
        EV << "\"Losing\" message " << msg << endl;
        //findHost()->bubble("message lost");
        delete msg;
        numLost++;
    }
    else{
            //findHost()->getDisplayString().updateWith("r=16,yellow");
            TraCIMobility* mobility = TraCIMobilityAccess().get(getParentModule());
            TraCICommandInterface* traci = mobility->getCommandInterface();
            TraCICommandInterface::Vehicle* traciVehicle = mobility->getVehicleCommandInterface();



            //消息传换成WSM
            BaseFrame1609_4* WSM = check_and_cast<BaseFrame1609_4*>(msg);
            //ASSERT(WSM);
            //从WSM中解封数据包
            cPacket* enc = WSM->getEncapsulatedPacket();
            //数据包转换成BeaconRSU
            BeaconRSU* bc = dynamic_cast<BeaconRSU*>(enc);
            //EV << "receive message  !!!" << endl;
            numReceived++;
            //EV << "RF: " << numRF << endl;
            //EV << "FR: " << numFR << endl;

            //if(a!=bc->getRSUId())
            //{
              // RSUIndex.record(bc->getRSUId());
               //a=bc->getRSUId();
            //}

            EV << "get speed limit from RSU : " <<bc->getMyDemoData()<<endl;

            const char * constc=bc->getMyDemoData();
            std::string str;
            str = constc;

            std::stringstream ss(str);
            double lane1;
            double lane2;
            double lane3;

            ss >> lane1;
            ss >> lane2;
            ss >> lane3;
            traci->lane("gneE1_0").setMaxSpeed(lane1);
            traci->lane("gneE1_1").setMaxSpeed(lane2);
            traci->lane("gneE1_2").setMaxSpeed(lane3);



// assign a random number to change lane------------LC2
//Case 1:able->unable




            //EV << "ExternalId = " <<mobility->getExternalId() <<endl;
            //EV << "Idnum = " <<mobility->getExternalId().substr(3) <<endl;
            //num=atoi("mobility->getExternalId().substr(3)");

            //value=rand()%3;
            //traciVehicle->setParameter("laneChangeModel.lcStrategic", value);
//            traciVehicle->getParameter("laneChangeModel.lcStrategic", lcStrategic);
//            traciVehicle->getParameter("laneChangeModel.lcKeepRight", lcKeepRight);
//            EV << "laneChangeModel.lcStrategic = " << lcStrategic <<endl;
//            EV << "laneChangeModel.lcKeepRight = " << lcKeepRight <<endl;



/*
//random number
//case2: unable->able

            randomNum = uniform(0,1);
            EV << "randomNum = " << randomNum <<endl;
            EV << "vType = " << mobility->getExternalId().substr(0,2) <<endl;

            if (mobility->getExternalId().substr(0,2)=="RF")
            {
                traciVehicle->setLaneChangeMode(0b001000000000);  //unable lane change

                if(randomNum < 0.5 & traciVehicle->getLanePosition()>=100 )
                {
                    traciVehicle->setLaneChangeMode(0b011001010101);
                }
                else if(0.5<=randomNum<0.9 & traciVehicle->getLanePosition()>=200)
                {
                    traciVehicle->setLaneChangeMode(0b011001010101);
                }
                else if(randomNum>=0.9 & traciVehicle->getLanePosition()>=300)
                {
                    traciVehicle->setLaneChangeMode(0b011001010101);
                }
            }
*/




    }
}

    /*
void MyVeinsAppCar::handlePositionUpdate(cObject* obj)
{
    EV << "**************8888888888888888888888888888888888888888888888888888888888888************************"<<endl;
    //DemoBaseApplLayer::handlePositionUpdate(obj);



    // the vehicle has moved. Code that reacts to new positions goes here.
    // member variables such as currentPosition and currentSpeed are updated in the parent class
}


 *    if (msg == BeaconRSU) {
        // get information about the vehicle via traci
        cModule* vehicle = getParentModule();
        Veins::TraCIMobility* traci = dynamic_cast<Veins::TraCIMobility*>(vehicle->getSubmodule("veinsmobility", 0));
        Veins::TraCICommandInterface::Vehicle* traciVehicle = traci->getVehicleCommandInterface();
      //  Plexe::VEHICLE_DATA data;
       // traciVehicle->getVehicleData(&data);
        THSposition[this->getParentModule()->getIndex()] = traci->getPositionAt(simTime());
        THSangle[this->getParentModule()->getIndex()] = traci->getAngleRad();
        THSspeed[this->getParentModule()->getIndex()] = traci->getSpeed();
        THSacceleration[this->getParentModule()->getIndex()] = acceleration;
        Beacon* beacon = new Beacon();

       beacon->setName("beacon");
       beacon->setVehicleId(this->getParentModule()->getIndex());

       acceleration = ( traci->getSpeed() - speedBefore ) * 1;//renew acc every 1s
       speedBefore = traci->getSpeed();
       beacon->setA(acceleration);
       beacon->setV(traci->getSpeed());
       beacon->setX(traci->getPositionAt(simTime()).x);
       beacon->setY(traci->getPositionAt(simTime()).y);
       SimTime frameStart = SimTime((double)((int)(simTime().raw()/SimTime(frameLength).raw()))/10);
       int frmNum = ((int)(10*(frameStart.raw()/SimTime(1).raw())))%10;
       int sltNum = this->getParentModule()->getIndex();
       beacon->setSlotpos(Coord(frmNum,sltNum));
       EV << "current position = " <<traci->getPositionAt(simTime())<<endl;

       //beacon->setLength();
       beacon->setAng(traci->getAngleRad());
     //  beacon->setP(selfp);
      // beacon->setBr(beaconRate);
     //  EV << "beaconrate = " <<beacon->getBeaconrate(i)<<endl;    //get THSbeaconrate ???


       for (int i = 0;i < 100;i++){
           beacon->setBeaconrate(i,THSbeaconrate[i]);
           beacon->setCp(i, THScp[i]);
           beacon->setSpeed(i,THSspeed[i]);
           beacon->setAcceleration(i, THSacceleration[i]);
           beacon->setPosition(i, THSposition[i]);
           beacon->setAngle(i, THSangle[i]);

*/



void MyVeinsAppCar::finish()
{
    DemoBaseApplLayer::finish();
    // statistics recording goes here
    EV << "33333333333333333333333333333333333333333333333333333333333333333 " << std::endl;
    EV << "Received: " << numReceived << endl;
    EV << "RF: " << numRF << endl;
    EV << "FR: " << numFR << endl;
    recordScalar("#received", numReceived);
}

/*
void MyVeinsAppCar::onBSM(DemoSafetyMessage* bsm)
{
    // Your application has received a beacon message from another car or RSU
    // code for handling the message goes here
    EV << " 4444444444444444444444444444444444444444444444444444444444444444" << std::endl;

}

void MyVeinsAppCar::onWSM(BaseFrame1609_4* wsm)
{
    BaseFrame1609_4* WSM = check_and_cast<BaseFrame1609_4*>(wsm);
    //从WSM中解封数据包
    cPacket* enc = WSM->getEncapsulatedPacket();
    //数据包转换成BeaconRSU
    BeaconRSU* bc = dynamic_cast<BeaconRSU*>(enc);

    if(a!=bc->getRSUId())
    {
       RSUIndex.record(bc->getRSUId());
       a=bc->getRSUId();
    }

    EV << "my message = " <<bc->getMyDemoData()<<endl;
    EV <<"send message RSU id:" <<bc->getRSUId() << "  Receive successfully !!!!!!!!!!!" << endl;
    EV << "2222222222222222222222222222222222222222222222222222222 " << std::endl;

    EV << "receive message  !!!" << endl;
    // Your application has received a data message from another car or RSU
    // code for handling the message goes here, see TraciDemo11p.cc for examples
    EV << "555555555555555555555555555555555555555555555555555555555555555555555555 " << std::endl;

}

void MyVeinsAppCar::onWSA(DemoServiceAdvertisment* wsa)
{
    // Your application has received a service advertisement from another car or RSU
    // code for handling the message goes here, see TraciDemo11p.cc for examples
    EV << "666666666666666666666666666666666666666666666666666666666666666 " << std::endl;

}


void MyVeinsAppCar::handleSelfMsg(cMessage* msg)
{
    EV << "477477777777747777777777477777777777774777777777777777777774777777777774444444444444444444444 " << std::endl;


        EV << "885555555555555555555555555555555588888888888888888888888888888888888888 " << std::endl;
        BeaconRSU* carmsg = new BeaconRSU();
        carmsg->setMyDemoData("CAR message!!");
            //BaseFrame1609_4* carmsg = new BaseFrame1609_4();
            //把rsuBeacon封装在WSM中
            //WSM->encapsulate(rsuBeacon);
            //设置WSM的基本信息
        populateWSM(carmsg,10);
            //send(WSM,lowerLayerOut);
        sendDown(carmsg);
        EV << "Car send success" <<endl;





}
*/


