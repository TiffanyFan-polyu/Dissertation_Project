#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 01:36:24 2018

@author: wuyuankai
"""

from __future__ import division
#from Priority_Replay import SumTree, Memory
import tensorflow as tf
import tensorflow.compat.v1 as tf
import numpy as np
import time
import xlwt
import os
import sys

tools = 'D:/Program Files (x86)/Eclipse/tools'
sys.path.append(tools)
import traci
from networks_llcd import rm_vsl_co

# EP_MAX = 600
EP_MAX = 1
LR_A = 0.0002    # learning rate for actor
LR_C = 0.0005    # learning rate for critic
GAMMA = 0.9      # reward discount
TAU = 0.01      # soft replacement
MEMORY_CAPACITY = 64
BATCH_SIZE = 32

RENDER = False  ##可视化

###############################  DDPG  ####################################


class VSL_DDPG_PR(object):
    def __init__(self, a_dim, s_dim,):
        #self.memory = Memory(capacity=MEMORY_CAPACITY)
        self.memory = np.zeros((MEMORY_CAPACITY, s_dim * 2 + a_dim + 1), dtype=np.float32)
        self.pointer = 0
        self.sess = tf.Session()

        self.a_dim, self.s_dim = a_dim, s_dim  ## a_sim=5(action=5,lane是5）s_dim=13
        #tf.compat.v1.disable_eager_execution()
        self.S = tf.placeholder(tf.float32, [None, s_dim], 's')    ## current state input,batch_size（输入的需要train的数量，维度待定）
        self.S_ = tf.placeholder(tf.float32, [None, s_dim], 's_')    ## next state input
        self.R = tf.placeholder(tf.float32, [None, 1], 'r')    ## reward

        self.a = self._build_a(self.S,)    ##build actor network
        q = self._build_c(self.S, self.a, )   ##build critic network
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Actor')    ##TRAINALBEL_VARIABLES: 所有用于反向传递的Variable，即可训练(可以被optimizer优化，进行参数更新)的变量
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Critic')
        ema = tf.train.ExponentialMovingAverage(decay=1 - TAU)          # soft replacement

        def ema_getter(getter, name, *args, **kwargs):
            return ema.average(getter(name, *args, **kwargs))

        target_update = [ema.apply(a_params), ema.apply(c_params)]      # soft update operation
        a_ = self._build_a(self.S_, reuse=True, custom_getter=ema_getter)   # replaced target parameters
        q_ = self._build_c(self.S_, a_, reuse=True, custom_getter=ema_getter)

        a_loss = - tf.reduce_mean(q)  # maximize the q
        self.atrain = tf.train.AdamOptimizer(LR_A).minimize(a_loss, var_list=a_params)
        self.td = self.R + GAMMA * q_ - q

        with tf.control_dependencies(target_update):    # soft replacement happened at here
            q_target = self.R + GAMMA * q_ 
            td_error = tf.losses.mean_squared_error(labels=q_target, predictions=q)
            self.ctrain = tf.train.AdamOptimizer(LR_C).minimize(td_error, var_list=c_params)

        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver(max_to_keep = 1)
        
    
    def choose_action(self, s):
        return self.sess.run(self.a, {self.S: s[np.newaxis, :]})[0]
    

    def learn(self):
#        tree_idx, bt, ISWeights = self.memory.sample(BATCH_SIZE)
        indices = np.random.choice(MEMORY_CAPACITY, size=BATCH_SIZE)
        bt = self.memory[indices, :]
        bs = bt[:, :self.s_dim]
        ba = bt[:, self.s_dim: self.s_dim + self.a_dim]
        br = bt[:, -self.s_dim - 1: -self.s_dim]
        bs_ = bt[:, -self.s_dim:]

        self.sess.run(self.atrain, {self.S: bs})
        self.sess.run(self.ctrain, {self.S: bs, self.a: ba, self.R: br, self.S_: bs_})


#    def store_transition(self, s, a, r, s_):
#        transition = np.hstack((s, a, r, s_))
#        self.memory.store(transition) 
    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, a, [r], s_))    ##使用np.hstack将4个向量（s、a、[r]、s_）合并为一个transition向量。horizontal
        index = self.pointer % MEMORY_CAPACITY  # replace the old memory with new memory
        self.memory[index, :] = transition   ##定义了具体存放经验的数组
        self.pointer += 1


    def _build_a(self, s, reuse=None, custom_getter=None):
        trainable = True if reuse is None else False
        with tf.variable_scope('Actor', reuse=reuse, custom_getter=custom_getter):
            neta = tf.layers.dense(s, 60, activation=tf.nn.relu, name='l1', trainable=trainable)  ##fully-connected layer
            a = tf.layers.dense(neta, self.a_dim, activation=tf.nn.sigmoid, name='l2', trainable=trainable,  use_bias=False)
            return tf.multiply(a, 8, name='scaled_a')

    def _build_c(self, s, a, reuse=None, custom_getter=None):
        trainable = True if reuse is None else False
        with tf.variable_scope('Critic', reuse=reuse, custom_getter=custom_getter):
            n_l1 = 50
            w1_s = tf.get_variable('w1_s', [self.s_dim, n_l1], trainable=trainable)
            w1_a = tf.get_variable('w1_a', [self.a_dim, n_l1], trainable=trainable)
            b1 = tf.get_variable('b1', [1, n_l1], trainable=trainable)
            netc = tf.nn.relu(tf.matmul(s, w1_s) + tf.matmul(a, w1_a) + b1)
            return tf.layers.dense(netc, 1, trainable=trainable)  
    
    def savemodel(self,):
        self.saver.save(self.sess,'ddpg_networkss_withoutexplore/' + 'ddpg.ckpt')
        
    def loadmodel(self,):
        loader = tf.train.import_meta_graph('ddpg_networkss_withoutexplore/ddpg.ckpt.meta')
        loader.restore(self.sess, tf.train.latest_checkpoint("ddpg_networkss_withoutexplore/"))

    def plot_reward(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(all_ep_r)), all_ep_r)
        plt.ylabel('reward')
        plt.xlabel('training steps')
        plt.show()

#def data_write(file_path, datas):


def from_a_to_mlv(a):
    return 17.8816 + 2.2352*np.floor(a)   #floor向下取整  40miles/h+5*np.floor(a)




time_start=time.time()
vsl_controller = VSL_DDPG_PR(s_dim = 25, a_dim = 3)
net = rm_vsl_co(visualization = False, incidents = False)
#net.writenewtrips()
traveltime='meanTravelTime='
co = 0
hc = 0
nox = 0
pmx = 0
ep_r = 0
oflow = 0
bspeed = 0
v = 30 *np.ones(3,)
net.start_new_simulation(write_newtrips = False)
s, r, simulationSteps, oflow_temp, bspeed_temp = net.run_step(v)
oflow = oflow + oflow_temp
bspeed_temp = bspeed + bspeed_temp
while simulationSteps < 3600:
    with open('vsl_control.txt', 'r') as f:  # 打开文件
        lines = f.readlines()  # 读取所有行
        for control_step in range(1, 120):
            v_str = lines[control_step]
            v_float = list(map(float, v_str.split()))
            v = v_float
            #print("control_step:", control_step,v)
            s_, r, simulationSteps, oflow_temp, bspeed_temp = net.run_step(v)
            oflow = oflow + oflow_temp
            bspeed = bspeed + bspeed_temp
            ep_r += r
net.close()
fname = 'output_sumo.xml'
print("no VSL control")
print(v)
with open(fname, 'r') as f:  # 打开文件
   lines = f.readlines()  # 读取所有行
   last_line = lines[-2]  # 取最后一行
nPos=last_line.index(traveltime)
aat_tempo = float(last_line[nPos+16:nPos+21])
# 打开“laneData.xml"
laneData = 'laneData.xml'
with open(laneData, 'r') as f:  # 打开文件
    lines = f.readlines()  # 读取所有行
    for lane in range(3):
        mainlane = lines[lane + 51]  # 取gne1那三行
        traveltimePos = mainlane.index('traveltime=')
        waitingTimePos = mainlane.index('waitingTime=')
        speedPos = mainlane.index('speed=')
        lane_traveltime = mainlane[traveltimePos + 12:traveltimePos + 17]
        lane_waitingTime = mainlane[waitingTimePos + 13:waitingTimePos + 19]
        lane_speed = mainlane[speedPos + 7:speedPos + 12]
        print('mainlane', lane, ': traveltime=', lane_traveltime, 'waitingTime=', lane_waitingTime, 'speed=',
              lane_speed)
print( 'Rewards: %.4f' % ep_r, 'Bottleneck speed: %.4f' % bspeed, 'out-in flow: %.4f' % oflow, 'Average Travel Time: %.4f' % aat_tempo)
time_end=time.time()
print('totally cost',time_end-time_start)



# time_start=time.time()
# #tf.compat.v1.disable_v2_behavior()
# vsl_controller.loadmodel()
# co = 0
# hc = 0
# nox = 0
# pmx = 0
# ep_r = 0
# oflow = 0
# bspeed = 0
# v = 30 *np.ones(3,)
# net.start_new_simulation(write_newtrips = False)
# s, r, simulationSteps, oflow_temp, bspeed_temp = net.run_step(v)
# oflow = oflow + oflow_temp
# bspeed_temp = bspeed + bspeed_temp
# stime = np.zeros(25,)
# stime[0:24] = s
# stime[24] = 0
# while simulationSteps < 3600:
#    a = vsl_controller.choose_action(stime)
#    #a = np.clip(np.random.laplace(a, var), 0, 7.99)
#    v = from_a_to_mlv(a)
#    stime_ = np.zeros(25,)
#    s_, r, simulationSteps, oflow_temp, bspeed_temp = net.run_step(v)
#    oflow = oflow + oflow_temp
#    bspeed = bspeed + bspeed_temp
#    stime_[0:24] = s_
#    stime_[24] = simulationSteps/3600
#    stime = stime_
#    ep_r += r
# net.close()
# print("VSL control with saved model")
# print(v)
# fname = 'output_sumo.xml'
# with open(fname, 'r') as f:  # 打开文件
#    lines = f.readlines()  # 读取所有行
#    last_line = lines[-2]  # 取最后一行
# nPos=last_line.index(traveltime)
# aat_tempo = float(last_line[nPos+16:nPos+21])
# # 打开“laneData.xml"
# laneData = 'laneData.xml'
# with open(laneData, 'r') as f:  # 打开文件
#     lines = f.readlines()  # 读取所有行
#     for lane in range(3):
#         mainlane = lines[lane + 49]  # 取gne1那三行
#         traveltimePos = mainlane.index('traveltime=')
#         waitingTimePos = mainlane.index('waitingTime=')
#         speedPos = mainlane.index('speed=')
#         lane_traveltime = mainlane[traveltimePos + 12:traveltimePos + 17]
#         lane_waitingTime = mainlane[waitingTimePos + 13:waitingTimePos + 19]
#         lane_speed = mainlane[speedPos + 7:speedPos + 12]
#         print('mainlane', lane, ': traveltime=', lane_traveltime, 'waitingTime=', lane_waitingTime, 'speed=',
#               lane_speed)
# print( 'Rewards: %.4f' % ep_r, 'Bottleneck speed: %.4f' % bspeed, 'out-in flow: %.4f' % oflow, 'Average Travel Time: %.4f' % aat_tempo)
# time_end=time.time()
# print('totally cost',time_end-time_start)