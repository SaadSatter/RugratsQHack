###############################################################################################
## priority.py
## Script to handle the client side interaction with LifeLine product
## 
## packet to be recvd ==> "#qhack2022#ip_addr=<ip_addr>#lat=<lat>#lon=<lon>#speed=<speed>"
## 
##
## Dependencies: python3, math, utm, threading, heapq, queue
##
##
###############################################################################################

import socket
import math
import utm
import threading
import heapq
import time
from queue import Queue

# Initialize the locks for buffer and queues
buflock = threading.Lock()
qlock = threading.Lock()

# Infinite Queue
buf = Queue(maxsize = -1)
q = Queue(maxsize = -1)

# Initialize the sockets to receive broadcast packets on port 11011
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', 11011))

# Dictionary of car IPs that we have seen so far
carDic = {}

# Radius of impact
radius = 9

######
###    @brief 
###        Polling thread function to poll the sockets for packet receive
###    
###    @param[in]  None
###    @retval     None
######
def poll():
    while(True):
        data, addr = sock.recvfrom(1024)
        print("rcvd")
        print(str(data))
        #print(b)
        #time.sleep(2)
        buflock.acquire()
        #print("poll: acquired")
        buf.put(data)
        buflock.release()

######
###    @brief 
###        Polling thread function to poll the sockets for packet receive
###    
###    @param[in]  Point tuple
###    @retval     List of XY coordinates
######
def convertToXY(point):
    return utm.from_latlon(point[0],point[1])[:2]

######
###    @brief 
###        Return slope and intercept from the pair of coordinates
###    
###    @param[in]  Points list
###    @retval     Tuple of slope and intercept (m, c)
######
def getLine(points):
    pt1_coords = points[0]
    pt2_coords = points[1]
    deltaX = pt2_coords[0] - pt1_coords[0]
    deltaY = pt2_coords[1] - pt1_coords[1]
    m=  deltaY/deltaX
    c = pt1_coords[1] - m*pt1_coords[0] 
    return (m,c)

######
###    @brief 
###        Compute and return the angle between the points
###    
###    @param[in]  Points list
###    @retval     Angle in degrees
######
def getAngle(points):
    pt1_coords = points[0]
    pt2_coords = points[1]
    deltaX = pt2_coords[0] - pt1_coords[0]
    deltaY = pt2_coords[1] - pt1_coords[1]
    radian =  math.atan(deltaY/deltaX)
    deg = (radian *180)/math.pi
    return deg

######
###    @brief 
###        Unpack the byte string passed from sockets layer to threading framework
###    
###    @param[in]  byte string
###    @retval     List of items [unique_id, ip_addr, lat, lon, speed]
######
def depack(data):
    dataList = data.split("#")
    
    dataList.remove("b'")
    id = dataList[0]
    print(dataList)
    if(id != "qhack2022"):
        return []
    ipaddr = dataList[1][(dataList[1].index("=") + 1):]
    lat = dataList[2][(dataList[2].index("=") + 1):]
    lon = dataList[3][(dataList[3].index("=") + 1):]
    speed = dataList[4][(dataList[4].index("=") + 1):(dataList[4].index("'"))]
    return [id, ipaddr, lat, lon, speed]


######
###    @brief 
###        Check function for the processing thread
###        - Check the distance from the client, compute angle, check collision trajectory
###    
###    @param[in]  ip_addr, car, data
###    @retval     List of ETA, message
######
def firstCheck(ipaddr, car, data):
    if not ipaddr in carDic:
        carDic[ipaddr] = []
    carDic[ipaddr].append(car)
    if(len(carDic[ipaddr]) <= 1):
        return []
    if (len(carDic[ipaddr]) > 2):
        carDic[ipaddr].remove(carDic[ipaddr][0])
    carVec = carDic[ipaddr]
    person = (32.90182,-117.19216)
    person = convertToXY(person)
    distance =  math.dist(carVec[1], person)

    minimumDistance = 50
    if distance > minimumDistance: 
        print("BAD")
        print(carDic[ipaddr])
        del carDic[ipaddr]
        return []
    tm = distance/float(data[4])

    carCurr = []
    carCurr.append(carVec[1][0])
    carCurr.append(carVec[1][1])
    carCurr[0] -= person[0]
    carCurr[1] -= person[1] 
    person = (0,0)
    points = []
    points.append(person)
    points.append(carCurr)
    angle = getAngle(points)
    m,c = getLine([(carVec[0][1]-person[0],carVec[0][1]-person[0]), carCurr])
    checkCollision(m,c,person,radius)
    angle = getAngle(points)
    msg = checkDirection(angle, carCurr)
    return [tm, msg]

######
###    @brief 
###        Check for perpendicular distance between the vehicle vector and pedestrian vector
###    
###    @param[in]  a, c, person, radius
###    @retval     None
######
def checkCollision(a, c, person, radius):
    x, y = person
    b = 1
    #print("Sloep and intercept", a,c)
    # Finding the distance of line
    # from center.
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
    #print(dist)
    # Checking if the distance is less
    # than, greater than or equal to radius.
    if (radius == dist):
        print("Touch")
    elif (radius > dist):
        print("Intersect")
    else:
        print("Outside")
        return

######
###    @brief 
###        Find the direction from where vehicle is approaching
###    
###    @param[in]  angle, car current coordinates
###    @retval     Message
######
def checkDirection(angle, carCurr):
    if angle > 0:
        if( angle < 45 and carCurr[0] > 0):
            msg = "Front Right"
        elif( angle > 45 and carCurr[0] > 0):
            ms = "Front"
        elif( angle < 45 and carCurr[0] < 0):
            msg = "Back Left"
        elif( angle > 45 and carCurr[0] < 0):
            msg = "Back"
    elif angle < 0:
        if( angle > -45 and carCurr[0] > 0):
            msg = "Back Right"
        elif( angle < -45 and carCurr[0] > 0):
            msg = "Back"
        elif( angle > -45 and carCurr[0] < 0):
            msg = "Front Left"
        elif( angle < -45 and carCurr[0] < 0):
            msg = "Front"
    else:
        if(carCurr[0] > 0):
            msg = "Right"
        else:
            msg = "Left"
    return msg

######
###    @brief 
###       Processing thread's function
###    
###    @param[in]  None
###    @retval     None
######
def vec():
    while(True):
        buflock.acquire()
        try:
            data = buf.get(block=False)
        except:
            buflock.release()
            continue
        buflock.release()
    
        dataList = depack(str(data))
        priorityList = []
        priorityList = firstCheck(dataList[1],(float(dataList[2]), float(dataList[3])), dataList)
        if(len(priorityList)==0):
            print("false check for: ")
            print(dataList)
            continue
        qlock.acquire()
        q.put(priorityList)
        qlock.release()
    
######
###    @brief 
###        Main thread's function
###    
###    @param[in]  None
###    @retval     None
######
def end():
    while(True):
        l = []
        while(q.qsize() < 3):
            time.sleep(1)
        qlock.acquire()
        while(not q.empty()):
                l.append(q.get())
        qlock.release()
        
        h = []
        while(len(l) > 0):
            el = l.pop()
            tm = int(el[0])
            msg = el[1]
            heapq.heappush(h, (tm, msg))
        print("heap: " + str(h))
        if(len(h) > 0):
            print("res = ")
            print(heapq.heappop(h))
            print("\n")

######
###    @brief 
###         Driver code
###
###    @param[in]  None
###    @retval     None
######
def main():
    # Initialize the polling threads
    t1 = threading.Thread(target = poll)
    t2 = threading.Thread(target = poll)
    t3 = threading.Thread(target = poll)
    
    # Start the threads
    t1.start()
    t2.start()
    t3.start()
    
    # Initialize the processing threads
    t4 = threading.Thread(target = vec)
    t5 = threading.Thread(target = vec)
    t4.start()
    t5.start()
    
    # Initialize the main processing thread
    mainthread = threading.Thread(target = end)
    mainthread.start()
    
    # Wait for the threads to finish
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    mainthread.join()
    
if __name__ == "__main__":
    main()
