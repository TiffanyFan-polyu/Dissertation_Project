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

#pragma once

#include "veins/veins.h"
#include "veins/modules/application/ieee80211p/DemoBaseApplLayer.h"
#include "veins/modules/application/traci/BeaconRSU_m.h"

using namespace omnetpp;

namespace veins {

class VEINS_API MyVeinsAppCar : public DemoBaseApplLayer {
public:
    void initialize(int stage) override;
    void finish() override;

protected:
    //void onBSM(DemoSafetyMessage* bsm) override;
    //void onWSM(BaseFrame1609_4* wsm) override;
    //void onWSA(DemoServiceAdvertisment* wsa) override;
    //void handleSelfMsg(cMessage* msg) override;
    //void handlePositionUpdate(cObject* obj) override;
    void handleLowerMsg(cMessage* msg) override;
    bool change;
    long numReceived;
    long numRF;
    long numFR;
    long numLost;

    cOutVector RSUIndex;
    int a;
    double lcStrategic;
    double lcKeepRight;
    double randomNum;
    int num;
    int value;
    std::string vtype0;
    std::string b;
    std::string c;
    std::string d;
    //std::string c;
    //cMessage* sendCarBeacon;
};

} // namespace veins
