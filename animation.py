import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import math
import time
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def getCoord():
    # return (28.394231,77.050308)
    return (0,0)

carDic = {}


radius = 300
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
    

def firstCheck(ipaddr, car, person, data):
    if not ipaddr in carDic:
        carDic[ipaddr] = []
    carDic[ipaddr].append(car)
    if(len(carDic[ipaddr]) <= 1):
        return False
    if (len(carDic[ipaddr]) > 2):
        carDic[ipaddr].remove(carDic[ipaddr][0])
    carVec = carDic[ipaddr]
    distance =  math.dist(carVec[1], person)
    print(distance)
    minimumDistance = 600
    if distance > minimumDistance: 
        print("BAD")
        print(carDic[ipaddr])
        del carDic[ipaddr]
        return False
    time = distance/float(data)
    print("Time ", time)
    carCurr = []
    print("Car:", carVec)
    print("Person:", person)
    carCurr.append(carVec[1][0])
    carCurr.append(carVec[1][1])
    carCurr[0] -= person[0]
    carCurr[1] -= person[1] 
    newCarPnts = ((carVec[0][0]-person[0],carVec[0][1]-person[1]), (carVec[1][0]-person[0],carVec[1][1]-person[1]))
    person = (0,0)
    points = []
    points.append(person)
    points.append(carCurr)
    m,c = getLine([(carVec[0][1]-person[0],carVec[0][1]-person[0]), carCurr])
    return(checkCollision(m,c,person,radius, newCarPnts))
   

def checkCollision(a, c, person, radius, newCarPnts):
    x, y = person
    b = 1
    print("Sloep and intercept", a,c)
    # Finding the distance of line
    # from center.
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
    print("-----------------", type(newCarPnts))

    print(dist)
    distances = (math.dist(newCarPnts[0], person), math.dist(newCarPnts[1], person))
    if distances[0] < distances[1]:
        print("car is moving away")
        return False
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
 
 
fig = plt.figure()
# 1 row, 1 col, 1 - ?
ax = fig.add_subplot(111)
x_lmt=(-600,600)
y_lmt=(-600,600)
ax.set_xlim(x_lmt)
ax.set_ylim(y_lmt)
 
 
#x1 = [-308, -305, -298,  -298,  -298, -179,  -50,   57,  209,  302,  347,  345,  344,  196,  154, 150,  63]
#y1 = [ 575,  516,  457,  422.5, 388,  376,  370,  363,  365,  361,  318,  195,   61,   34,   32,  31,  -4]
# car1 coordinates
x1 = []
y1 = []
x1.append(int(-343))
y1.append(int(586))
 
i=0
# start down motion
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(y1[i]>380):
        x1.append(int(x1[i]))
        y1.append(int(y1[i]-10))
    else:
        ##print("x1 at ", x1[i])
        ##print("y1 at ", y1[i])
        break
    i=i+1
# inclined right-bottom motion 
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(x1[i]<-274):
        x1.append(int(x1[i]+5))
        y1.append(int(y1[i]-5))
    else:
        #print("x1 at ", x1[i])
        #print("y1 at ", y1[i])
        break
    i=i+1
# start right motion  
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(x1[i]<280):
        x1.append(int(x1[i]+10))
        y1.append(int(y1[i]))
    else:
        #print("x1 at ", x1[i])
        #print("y1 at ", y1[i])
        break
    i=i+1
# inclined right-bottom motion  
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(x1[i]<307):
        x1.append(int(x1[i]+5))
        y1.append(int(y1[i]-5))
    else:
        #print("x1 at ", x1[i])
        #print("y1 at ", y1[i])
        break
    i=i+1
# start down motion
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(y1[i]>50):
        x1.append(int(x1[i]))
        y1.append(int(y1[i]-10))
    else:
        #print("x1 at ", x1[i])
        #print("y1 at ", y1[i])
        break
    i=i+1
# inclined left-bottom motion
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(y1[i]>20):
        x1.append(int(x1[i]-5))
        y1.append(int(y1[i]-5))
    else:
        #print("x1 at ", x1[i])
        #print("y1 at ", y1[i])
        break
    i=i+1
# start left motion
while(x1[i]<x_lmt[1] and x1[i]>x_lmt[0] and y1[i]>y_lmt[0] and y1[i]<y_lmt[1]):
    #if(i < 17)
    if(x1[i]>100):
        x1.append(int(x1[i]-10))
        y1.append(int(y1[i]))
    else:
        #print("x1 at ", x1[i])
        #print("y1 at ", y1[i])
        break
    i=i+1
 
# car1 coordinates
x2 = []
y2 = []
x2.append(int(-294))
y2.append(int(-577))
 
i=0
# start up motion
while(x2[i]<x_lmt[1] and x2[i]>x_lmt[0] and y2[i]>y_lmt[0] and y2[i]<y_lmt[1]):
    #if(i < 17)
    if(y2[i]<-70):
        x2.append(int(x2[i]))
        y2.append(int(y2[i]+10))
    else:
        #print("x2 at ", x2[i])
        #print("y2 at ", y2[i])
        break
    i=i+1
# inclined right-top motion
while(x2[i]<x_lmt[1] and x2[i]>x_lmt[0] and y2[i]>y_lmt[0] and y2[i]<y_lmt[1]):
    if(x2[i]<-260):
        x2.append(int(x2[i]+5))
        y2.append(int(y2[i]+5))
    else:
        #print("x2 at ", x2[i])
        #print("y2 at ", y2[i])
        break
    i=i+1
# strait right motions
while(x2[i]<x_lmt[1] and x2[i]>x_lmt[0] and y2[i]>y_lmt[0] and y2[i]<y_lmt[1]):
    if(x2[i]<-100):
        x2.append(int(x2[i]+10))
        y2.append(int(y2[i]))
    else:
        #print("x2 at ", x2[i])
        #print("y2 at ", y2[i])
        break
    i=i+1
# strait right motions
while(x2[i]<x_lmt[1] and x2[i]>x_lmt[0] and y2[i]>y_lmt[0] and y2[i]<y_lmt[1]):
    if(x2[i]<-80):
        x2.append(int(x2[i]+10))
        y2.append(int(y2[i]-1))
    else:
        #print("x2 at ", x2[i])
        #print("y2 at ", y2[i])
        break
    i=i+1
    
 
if(len(x1)>len(x2)):
    i=len(x2)
    while(i<len(x1)):
        x2.append(int(x2[i-1]))
        y2.append(int(y2[i-1]))
        
        i=i+1
else:
    i=len(x1)
    while(i<len(x2)):
        x1.append(int(x1[i-1]))
        y1.append(int(y1[i-1]))
        
        i=i+1
    
#print(len(x2))
#print(len(x1))
 
x_p1 = []
y_p1 = []
#x_p2 = []
#y_p2 = []
x_p3 = []
y_p3 = []
x_p4 = []
y_p4 = []
#x_p1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#y_p1 = x_p1
 
i=0
while(i<len(x2)):
    x_p1.append(int(0))
    y_p1.append(int(-60))
    #x_p2.append(int(395))
    #y_p2.append(int(130))
    x_p3.append(int(-450))
    y_p3.append(int(390))
    x_p4.append(int(-390))
    y_p4.append(int(-453))
    
    i=i+1
 
 
 
# car1 object
car1_line, = ax.plot(0, 0, linewidth =10, color = 'red')
# car2 object
car2_line, = ax.plot(0, 0, linewidth =10, color = 'red')
 
img_bg = plt.imread('back.jpg')
img_bg = ax.imshow(img_bg, extent=[x_lmt[0], x_lmt[1], y_lmt[0], y_lmt[1]])
#img_car = plt.imread('car_s.png')
 
#fig.figimage(img, 100, 10, alpha =0.9)
#set_figsize_inches = ((fig.get_size_inches),())
#img = plt.imread("C:/Users/sohanlal/OneDrive - Qualcomm/Documents/qhach2022/", format = 'png')
#oi = OffsetImage(img, zoom = 0.15)
ax.plot(0,0)
#car1 trajectory
car1_trj, = ax.plot(0, 0, linewidth =0.8, color = 'black', dashes = (10,5))
#car2 trajectory
car2_trj, = ax.plot(0, 0, linewidth =0.8, color = 'black', dashes = (10,5))
 
#person1 object and circle
person1 = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 10, color = 'blue')
person1_cir = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 50, fill = False)
#person2 object and circle
person2 = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 10, color = 'blue')
person2_cir = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 50, fill = False)
#person3 object and circle
person3 = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 10, color = 'blue')
person3_cir = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 50, fill = False)
#person4 object and circle
person4 = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 10, color = 'blue')
person4_cir = patches.Circle((x_lmt[1]*2, y_lmt[1]*2), 50, fill = False)
 
ax.add_patch(person1)
ax.add_patch(person1_cir)
ax.add_patch(person2)
ax.add_patch(person2_cir)
ax.add_patch(person3)
ax.add_patch(person3_cir)
ax.add_patch(person4)
ax.add_patch(person4_cir)
 
 
# animation function - runs for every frame
def animation_frame(i):
    global flag1
    global flag2
    global flag3
    global flag4    
    global flag5
    global flag6
    global flag7
    global flag8
    
    idx=i
    #x1[i] = x2[i]
    #y1[i] = y2[i]
    #img_car = ax.imshow(f(x1, y1), animated=True)
    #img = ax.imshow(img)
    #ax.imshow(img, extent=[0, 400, 0, 300])
    #oi = OffsetImage(img, zoom = 0.15)
    #box = AnnotationBbox(oi, (0, 0), frameon=False)
    #a.append(ax.add_artist(box))
    # creating peson1 
    person1.center = ([x_p1[i], y_p1[i]])
    person1_cir.center = ([x_p1[i], y_p1[i]])
    # creating peson2 
    #person2.center = ([x_p2[i], y_p2[i]])
    #person2_cir.center = ([x_p2[i], y_p2[i]])
    # creating peson3 
    person3.center = ([x_p3[i], y_p3[i]])
    person3_cir.center = ([x_p3[i], y_p3[i]])
    # creating peson4 
    person4.center = ([x_p4[i], y_p4[i]])
    person4_cir.center = ([x_p4[i], y_p4[i]])
    
    flag1 = firstCheck(1, (x1[i], y1[i]), person1.center, 4)
    flag2 = firstCheck(1, (x2[i], y2[i]), person1.center, 4)
    flag3 = firstCheck(1, (x1[i], y1[i]), person2.center, 4)
    flag4 = firstCheck(1, (x2[i], y2[i]), person2.center, 4)
    flag5 = firstCheck(1, (x1[i], y1[i]), person3.center, 4)
    flag6 = firstCheck(1, (x2[i], y2[i]), person3.center, 4)
    flag7 = firstCheck(1, (x1[i], y1[i]), person4.center, 4)
    flag8 = firstCheck(1, (x2[i], y2[i]), person4.center, 4)
    
    
    # editing color if danger flag is true
    if(flag1==True):
        person1.set_color('red')
    else:
        person1.set_color('blue')
    if(flag2==True):
        person1.set_color('red')
    else:
        person1.set_color('blue')
    # if(flag3==True):
    #     person2.set_color('red')
    # else:
    #     person2.set_color('blue')
    # if(flag4==True):
    #     person2.set_color('red')
    # else:
    #     person2.set_color('blue')
    if(flag5==True):
        person3.set_color('red')
    else:
        person3.set_color('blue')
    if(flag6==True):
        person3.set_color('red')
    else:
        person3.set_color('blue')
    if(flag7==True):
        person4.set_color('red')
    else:
        person4.set_color('blue')
    if(flag8==True):
        person4.set_color('red')
    else:
        person4.set_color('blue')
    
    #if(i>len(x2)/2):
        #flag=True
 
    
    # creating a trajectory for the car1
    if((x1[idx+1]-x1[idx]) == 0):
        car1_trj.set_xdata([x1[idx], x1[idx]])
        if(y1[idx+1]-y1[idx] >= 0):
            car1_trj.set_ydata([y1[idx], y_lmt[1]])
        else:
            car1_trj.set_ydata([y1[idx], y_lmt[0]])
    else:
        m = (y1[idx+1]-y1[idx]) / (x1[idx+1]-x1[idx])
        c = y1[idx] - m * x1[idx]
        if(x1[idx+1]-x1[idx] >= 0):
            etm_y = m*(x_lmt[1]) + c
            car1_trj.set_xdata([x1[idx], x_lmt[1]])
            car1_trj.set_ydata([y1[idx], etm_y])
        else:
            etm_y = m*(x_lmt[0]) + c
            car1_trj.set_xdata([x1[idx], x_lmt[0]])
            car1_trj.set_ydata([y1[idx], etm_y])
    
    # creating the car1 with one pairs of (x1,y1) and angle
    car_len = 60
    if((x1[idx+1]-x1[idx]) == 0):
        car1_line.set_xdata([x1[idx], x1[idx]])
        if(y1[idx+1]-y1[idx] >= 0):
            car1_line.set_ydata([y1[idx], y1[idx]+car_len])
        else:
            car1_line.set_ydata([y1[idx], y1[idx]-car_len])
    else:
        m = (y1[idx+1]-y1[idx]) / (x1[idx+1]-x1[idx])
        c = y1[idx] - m * x1[idx]
        angle = math.atan(m)
        dist = car_len*math.cos(angle)
        if(x1[idx+1]-x1[idx] >= 0):
            etm_y = m*(x1[idx]+dist) + c
            car1_line.set_xdata([x1[idx], x1[idx]+dist])
            car1_line.set_ydata([y1[idx], etm_y])
        else:
            etm_y = m*(x1[idx]-dist) + c
            car1_line.set_xdata([x1[idx], x1[idx]-dist])
            car1_line.set_ydata([y1[idx], etm_y])
    
    
    # creating a trajectory for the car2
    if((x2[idx+1]-x2[idx]) == 0):
        if(y2[idx+1]-y2[idx] > 0):
            car2_trj.set_xdata([x2[idx], x2[idx]])
            car2_trj.set_ydata([y2[idx], y_lmt[1]])
        elif(y2[idx+1]-y2[idx] == 0):
            car2_trj.set_xdata([x2[idx], x_lmt[1]])
            car2_trj.set_ydata([y2[idx], y2[idx]])
        else:
            car2_trj.set_xdata([x2[idx], x2[idx]])
            car2_trj.set_ydata([y2[idx], y_lmt[0]])   
    else:
        m = (y2[idx+1]-y2[idx]) / (x2[idx+1]-x2[idx])
        c = y2[idx] - m * x2[idx]
        if(x2[idx+1]-x2[idx] >= 0):
            etm_y = m*(x_lmt[1]) + c
            car2_trj.set_xdata([x2[idx], x_lmt[1]])
            car2_trj.set_ydata([y2[idx], etm_y])
        else:
            etm_y = m*(x_lmt[0]) + c
            car2_trj.set_xdata([x2[idx], x_lmt[0]])
            car2_trj.set_ydata([y2[idx], etm_y])
    
    # creating the car2 with one pairs of (x2,y2) and angle
    car_len = 60
    if((x2[idx+1]-x2[idx]) == 0):
        if(y2[idx+1]-y2[idx] > 0):
            car2_line.set_xdata([x2[idx], x2[idx]])
            car2_line.set_ydata([y2[idx], y2[idx]+car_len])
        elif(y2[idx+1]-y2[idx] == 0):
            car2_line.set_xdata([x2[idx], x2[idx]+car_len])
            car2_line.set_ydata([y2[idx], y2[idx]])
        else:
            car2_line.set_xdata([x2[idx], x2[idx]])
            car2_line.set_ydata([y2[idx], y2[idx]-car_len])
    else:
        m = (y2[idx+1]-y2[idx]) / (x2[idx+1]-x2[idx])
        c = y2[idx] - m * x2[idx]
        angle = math.atan(m)
        dist = car_len*math.cos(angle)
        if(x2[idx+1]-x2[idx] >= 0):
            etm_y = m*(x2[idx]+dist) + c
            car2_line.set_xdata([x2[idx], x2[idx]+dist])
            car2_line.set_ydata([y2[idx], etm_y])
        else:
            etm_y = m*(x2[idx]-dist) + c
            car2_line.set_xdata([x2[idx], x2[idx]-dist])
            car2_line.set_ydata([y2[idx], etm_y])
    
    
 
# main animation function
animation = FuncAnimation(fig, animation_frame,
                          
                          frames=len(x2)-1,
                          repeat = False,
                          interval=100)
 
# show the plot
plt.show()
