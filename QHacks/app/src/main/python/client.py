from hashlib import new
from re import T
import socket
from time import sleep
import time
from types import new_class
import haversine as hs
import math
# from numpy import ones,vstack
import utm
# from numpy.linalg import lstsq

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', 11011))



def convertToXY(point):
    # print(point)
    print("XY : ", utm.from_latlon(point[0],point[1]))
    return utm.from_latlon(point[0],point[1])[:2]

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
    

def firstCheck(ipaddr, car, data, coord, personAngle):
    if not (ipaddr in carDic):
        print(not (ipaddr in carDic), ipaddr, carDic.keys())
        carDic[ipaddr] = []
    
    carDic[ipaddr].append(car)
    
    if(len(carDic[ipaddr]) <= 1):
        return "First Signal"
    print("check")
    if (len(carDic[ipaddr]) > 2):
        carDic[ipaddr].remove(carDic[ipaddr][0])
    carVec = carDic[ipaddr]
    # person= get_loc()
    # person = (32.90182,-117.19216)
    person = coord
    person = convertToXY(person)
    # distance = hs.haversine(carVec[1], person)
    distance =  math.dist(carVec[1], person)
    print(distance)
    minimumDistance = 50;
    if distance > minimumDistance: 
        print("BAD")
        print(carDic[ipaddr])
        print(person)
        del carDic[ipaddr]
        return "Too Far"
    time = distance/float(data[4])
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
    newCarPnts = (carVec[0][1]-person[0],carVec[0][1]-person[0])
    newCarPnts = (carVec)
    points = []
    points.append(person)
    points.append(carCurr)
    angle = getAngle(points)
    m,c = getLine([newCarPnts[0], carCurr])
    flag = checkCollision(m,c,person,radius, newCarPnts)
    # carCurr[0] -= person[0]
    # carCurr[1] -= person[1] 
    # person = (0,0)
    # points = []
    # points.append(person)
    # points.append(carCurr)
    angle = getAngle(points)
    direction = checkDirection(angle, carCurr, personAngle)
    return flag[1] + "\n" + direction 

def checkCollision(a, c, person, radius, newCarPnts):
    x, y = person
    b = 1
    print("Sloep and intercept", a,c)
    # Finding the distance of line
    # from center.
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
    print(dist)
    distances = (math.dist(newCarPnts[0], person), math.dist(newCarPnts[1], person))
    if distances[1] > distances[0]:
        print("car is moving away")
        return (False, "car is moving away")
    # Checking if the distance is less
    # than, greater than or equal to radius.
    if (radius == dist):
        print("Touch")
        return (True, "Touch")
    elif (radius > dist):
        print("Intersect")
        return (True, "Intersect")
    else:
        print("Outside")
        return (False, "Outside")
    
def fixAngle(angle, carCurr):
    if angle > 0 and carCurr[0] > 0:
        return angle
    elif angle > 0:
        return angle + 180
    elif angle < 0 and carCurr[0] > 0:
        return angle
    elif angle < 0:
        return angle - 180

def checkDirection(angle, carCurr, personAngle):
    angle = fixAngle(angle, carCurr)
    print(angle)
    angleDifference = math.fabs(angle-personAngle)
    sign = angle-personAngle
    if angleDifference <= 45 or angleDifference > 315:
        return "Front"
    elif angleDifference > 45 and angleDifference <= 135:
        if sign < 0:
            return "Right"
        return "Left"
    elif angleDifference > 135 and angleDifference <= 225:
        return "Back"
    else:
        if sign < 0:
            return "Left"
        return "Right"
    # if angle > 0:
    #     if( angle < 45 and carCurr[0] > 0):
    #         print("Front Right")
    #     elif( angle > 45 and carCurr[0] > 0):
    #         print("Front")
    #     elif( angle < 45 and carCurr[0] < 0):
    #         print("Back Left")
    #     elif( angle > 45 and carCurr[0] < 0):
    #         print("Back")
    # elif angle < 0:
    #     if( angle > -45 and carCurr[0] > 0):
    #         print("Back Right")
    #     elif( angle < -45 and carCurr[0] > 0):
    #         print("Back")
    #     elif( angle > -45 and carCurr[0] < 0):
    #         print("Front Left")
    #     elif( angle < -45 and carCurr[0] < 0):
    #         print("Front")
    # else:
    #     if(carCurr[0] > 0):
    #         print("Right")
    #     else:
    #         print("Left")

## Get the current coordinates of the device by scrapping https://mycurrentlocation.net/
##
##  @retval (lat, lon)
##
# def get_loc():
#     options = Options()
#     options.add_argument("--use-fake-ui-for-media-stream")
#     timeout = 20
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get("https://mycurrentlocation.net/")
#     wait = WebDriverWait(driver, timeout)
#     time.sleep(3)
#     div_ele = driver.find_element("xpath", '//*[@id="maps-mapbox"]/div[4]/div[2]')
#     div_ele = str(div_ele.text)
#     div_ele = div_ele.split("\n")[2]
#     lat = div_ele.split(" ")[2]
#     lon = div_ele.split(" ")[-1]
#     driver.quit()
#     return (lat, lon)

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



def main(lat, lon, personAngle):
        
    # while True:
        
    # print("hi")
    data, addr = sock.recvfrom(1024)
    print(data)
    dataList = depack(str(data))
    if(dataList == []):
        return """BAD\nDATA"""
    
    ipaddr = 1
    # dataList = ["QHACK", ipaddr, 10,10, 30]
    val = firstCheck(dataList[1],(float(dataList[2]), float(dataList[3])), dataList, (lat, lon),personAngle)
    print("first " , val)
    # dataList = ["QHACK",ipaddr, 5,5, 30]
    val = firstCheck(dataList[1],(float(dataList[2]), float(dataList[3])), dataList, (lat, lon), personAngle)
    print("Person Angle: ", personAngle)
    print(val)
    return val
        # print("HI 2")
        # sleep(10)
        # print("Goodbye")
    # while(1):
    #     lat, lon = get_loc()
    #     if prev_lat == 0 and prev_lon == 0:
    #         # Initial broadcast
    #         udp_broadcast(lat, lon, 0)
    #         prev_lat = lat
    #         prev_lon = lon
    #     else:
    #         points = []
    #         prev_coord = []
    #         coord = []
    #         prev_coord.append(float(prev_lat))
    #         prev_coord.append(float(prev_lon))
    #         points.append(prev_coord)
    #         coord.append(float(lat))
    #         coord.append(float(lon))
    #         points.append(coord)
    #         speed = getSpeed(points, elapsed_time)

    #         # Send the broadcast
    #         udp_broadcast(lat, lon, speed)

    #         # Save current location as prev location
    #         prev_lat = lat
    #         prev_lon = lon

    #         # Dynamically change the time to wait based on current speed
    #         if speed > prev_speed:
    #             if elapsed_time > 20:
    #                 elapsed_time -= 1
    #         else:
    #             if elapsed_time < 50:
    #                 elapsed_time += 1
    #         prev_speed = speed
    #     print("elapsed_time:", elapsed_time)
    #     time.sleep(elapsed_time)

# if __name__ == "__main__":
#     main()
# main(32,-117)
