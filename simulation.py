
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import math
import time
from re import T
import socket
from time import sleep

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import socket
import haversine as hs
import math
from webbrowser import get
import haversine as hs
import math
from numpy import ones,vstack
import utm
from numpy.linalg import lstsq

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', 11011))



def convertToXY(point):
    # print(point)
    print("XY : ", utm.from_latlon(point[0],point[1]))
    return utm.from_latlon(point[0],point[1])[:2]


def getCoord():
    # return (28.394231,77.050308)
    return (0,0)

carDic = {}


radius = 9
def getLine(points):
    pt1_coords = points[0]
    pt2_coords = points[1]
    deltaX = pt2_coords[0] - pt1_coords[0]
    deltaY = pt2_coords[1] - pt1_coords[1]
    m=  deltaY/deltaX
    c = pt1_coords[1] - m*pt1_coords[0] 
    return (m,c)

def getAngle(points):
    pt1_coords = points[0]
    pt2_coords = points[1]
    deltaX = pt2_coords[0] - pt1_coords[0]
    deltaY = pt2_coords[1] - pt1_coords[1]
    radian =  math.atan(deltaY/deltaX)
    deg = (radian *180)/math.pi
    return deg
    

def firstCheck(ipaddr, car, data):
    if not ipaddr in carDic:
        carDic[ipaddr] = []
    carDic[ipaddr].append(car)
    if(len(carDic[ipaddr]) <= 1):
        return False
    if (len(carDic[ipaddr]) > 2):
        carDic[ipaddr].remove(carDic[ipaddr][0])
    carVec = carDic[ipaddr]
    # person= get_loc()
    # person = (32.90182,-117.19216)
    person = (0,0)
    # distance = hs.haversine(carVec[1], person)
    distance =  math.dist(carVec[1], person)
    print(distance)
    minimumDistance = 50;
    if distance > minimumDistance: 
        print("BAD")
        print(carDic[ipaddr])
        del carDic[ipaddr]
        return False
    time = distance/float(data)
    print("Time ", time)
    carCurr = []
    # carVec = (convertToXY(carVec[0]),convertToXY(carVec[1]))
    print("Car:", carVec)
    # person = convertToXY(person)
    print("Person:", person)
    carCurr.append(carVec[1][0])
    carCurr.append(carVec[1][1])
    carCurr[0] -= person[0]
    carCurr[1] -= person[1] 
    person = (0,0)
    points = []
    points.append(person)
    points.append(carCurr)
    # angle = getAngle(points)
    m,c = getLine([(carVec[0][1]-person[0],carVec[0][1]-person[0]), carCurr])
    return(checkCollision(m,c,person,radius))
    # carCurr[0] -= person[0]
    # carCurr[1] -= person[1] 
    # person = (0,0)
    # points = []
    # points.append(person)
    # points.append(carCurr)
    angle = getAngle(points)
    checkDirection(angle, carCurr)

def checkCollision(a, c, person, radius):
    x, y = person
    b = 1
    radius = 2
    print("Sloep and intercept", a,c)
    # Finding the distance of line
    # from center.
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
    print(dist)
    # Checking if the distance is less
    # than, greater than or equal to radius.
    if (radius == dist):
        print("Touch")
        return True
    elif (radius > dist):
        print("Intersect")
        return True
    else:
        print("Outside")
        return False
    
def checkDirection(angle, carCurr):
    if angle > 0:
        if( angle < 45 and carCurr[0] > 0):
            print("Front Right")
        elif( angle > 45 and carCurr[0] > 0):
            print("Front")
        elif( angle < 45 and carCurr[0] < 0):
            print("Back Left")
        elif( angle > 45 and carCurr[0] < 0):
            print("Back")
    elif angle < 0:
        if( angle > -45 and carCurr[0] > 0):
            print("Back Right")
        elif( angle < -45 and carCurr[0] > 0):
            print("Back")
        elif( angle > -45 and carCurr[0] < 0):
            print("Front Left")
        elif( angle < -45 and carCurr[0] < 0):
            print("Front")
    else:
        if(carCurr[0] > 0):
            print("Right")
        else:
            print("Left")
x_data = []
y_data = []
xp_data = []
yp_data = []
flag=False
 
x = [ 5,  4,  3,  2,  1,  0, -1, -2, -2, -1]
y = [-5, -5, -4, -4, -4, -4, -4, -3, -2, -1]
 
x_p = []
y_p = []
#x_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#y_p = x_p
 
i=0
while(i<len(x)):
    x_p.append(int(0))
    y_p.append(int(0))
    i=i+1
fig = plt.figure()
# 1 row, 1 col, 1 - ?
ax = fig.add_subplot(111)
x_lmt=(-10,10)
y_lmt=(-10,10)
ax.set_xlim(x_lmt)
ax.set_ylim(y_lmt)
 
# car object
car, = ax.plot(0, 0, linewidth =15, color = 'red')
#car trajectory
car_trj, = ax.plot(0, 0, linewidth =0.1, color = 'black')
#person object
person = patches.Circle((x_lmt[1]+5, y_lmt[1]+5), 0.2, color = 'blue')
# cicle for person
person_cir = patches.Circle((x_lmt[1]+5, y_lmt[1]+5), 2, fill = False)
 
ax.add_patch(person_cir)
ax.add_patch(person)
 
# animation function - runs for every frame
def animation_frame(i):
    global flag
    
    idx=i
    flag = firstCheck(1, (x[i], y[i]), 4);
    # creating peson 
    person.center = ([x_p[i], y_p[i]])
    # editing color if danger flag is true
    if(flag==True):
        person.set_color('red')
 
    # creating the car with two pairs of (x,y)
    car.set_xdata([x[idx], x[idx+1]])
    car.set_ydata([y[idx], y[idx+1]])
    
    # creating a trajectory for the car
    if((x[idx+1]-x[idx]) == 0):
        #xtj_data.append(x[idx])
        car_trj.set_xdata([x[idx], x[idx]])
        if(y[idx+1]-y[idx] >= 0):
            #ytj_data.append(x_lmt[1])
            car_trj.set_ydata([y[idx], x_lmt[1]])
        else:
            #ytj_data.append(x_lmt[0])
            car_trj.set_ydata([y[idx], x_lmt[1]])
    else:
        m = (y[idx+1]-y[idx]) / (x[idx+1]-x[idx])
        c = y[idx] - m * x[idx]
        if(x[idx+1]-x[idx] >= 0):
            etm_y = m*(x_lmt[1]) + c
            #xtj_data.append(x_lmt[1])
            car_trj.set_xdata([x[idx], x_lmt[1]])
            #ytj_data.append(etm_y)
            car_trj.set_ydata([y[idx], etm_y])
        else:
            etm_y = m*(x_lmt[0]) + c
            #xtj_data.append(x_lmt[0])
            car_trj.set_xdata([x[idx], x_lmt[0]])
            #ytj_data.append(etm_y)
            car_trj.set_ydata([y[idx], etm_y])
    
    if(i>5):
        flag=True
        person_cir.center = ([x_p[i], y_p[i]])
    
 
# main animation function
animation = FuncAnimation(fig, animation_frame,
                          
                          frames=len(x)-1,
                          repeat = False,
                          interval=200)
 
# show the plot
plt.show()


