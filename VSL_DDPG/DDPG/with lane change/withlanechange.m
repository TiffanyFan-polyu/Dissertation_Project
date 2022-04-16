% The script is to plot the...
% k1 is the number of the IDs;
clear
clc
close all
%addpath(genpath('C:\Users\13660\Desktop\FTT'));% add the filepath

excel_path='D:\FTT\sumo_test\llcd\DDPG\with lane change\';   %文件夹路径 
path_list = dir('D:\FTT\sumo_test\llcd\DDPG\with lane change\*.xlsx');          
%dir 函数 列出当前目录下所有子文件夹和文件%
list_num = length(path_list);
X=zeros(4,41);
for i=1:list_num
   [txt,num,raw] = xlsread([excel_path,path_list(i).name]);
   [tm,tn]=size(num);
   numT(1:tm,1:tn,i)=num;
   
   num(1,:)=[];
   Speed=txt(:,7);
   Ncar=txt(:,4);
   I=findgroups(num(:,3));  
   I=sort(I);
   func = @(x,y) sum(x.*y)/sum(y);
   Varspeed=splitapply(func,Speed,Ncar,I);
   num(1,:)=[];
Varspeed=Varspeed';
X(i,:)=Varspeed;

end
x=0:10:400;
hold on;
plot(x,X(1,:),'-*k','Linewidth',2)
plot(x,X(2,:),'-ob','Linewidth',2)
plot(x,X(4,:),'-dg','Linewidth',2)
plot(x,X(3,:),'-or','Linewidth',2)
%plot(x,X(5,:),'-.r','Linewidth',2)
%plot(x,X(6,:),'-.k','Linewidth',2)

xlabel('Distance(m)');
ylabel('speed(m/s)');
legend('no control','VSL','LC','LC+VSL');

hold off