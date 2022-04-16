
-----------------------------------connection method--------------------------------------
1 open Anaconda -- Powershell Prompt
2 activate virtual enviromment "tensorflow", all required packets are installed in this enviromment.  
(base)   >   conda activate tensorflow
3 (tensorflow) >   cd path(ddpg_llcd.py)
4 (tensorflow) llcd>  python ddpg_llcd.py

-------------
if connect to omnet
5 open mingwenv.cmd, enter command: omnetpp
6 Run python script (with traCI 2 clients mode)


-------------------------------python script--------------------------------------
ddpg_llcd.py : the DDPG agent to train VSL
networks_llcd.py : SUMO enrivonment to interact with DDPG agent
optimal_.py : input the optimal VSL from vsl_control.txt
runner.py : running SUMO without control