####################################################################################
## sender.py
## Script to send the current ip_addr, latitude, longitude and speed to the client
## 
## packet ==> "#qhack2022#ip_addr=<ip_addr>#lat=<lat>#lon=<lon>#speed=<speed>"
## 
## UDP unicast is used to send the packet to specific ip, broadcast/multicast
## is preferred but due to network admin settings, both are disabled.
##
## Dependencies: python3, selenium, webdriver-manager, chromedriver, socket
##               haversine
##
####################################################################################

import os
import time
import socket
import haversine as hs
import math

## Extract the ip address for the current WiFi interface
interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
allips = [ip[-1][0] for ip in interfaces]
curr_ip = ""
i = 0
while i < len(allips):
    if allips[i] == '127.0.0.1':
        i += 1
        continue
    curr_ip = allips[i]
    break


# Return the speed of the car given the coordinates and time taken
def getSpeed(points, time):
    print(points)
    tup1 = (points[0][0], points[0][1])
    tup2 = (points[1][0], points[1][1])
    distance = hs.haversine(tup1, tup2)
    return distance/time

# ## Get the current coordinates of the device by scrapping https://mycurrentlocation.net/
# ##
# ##  @retval (lat, lon)
# ##
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

## Send the ip_addr, lat, lon over UDP broadcast
def udp_broadcast(lat, lon, speed):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #sock.settimeout(0.2)
    msg = "#qhack2022#ip_addr=" + curr_ip + "#lat=" + lat + "#lon=" + lon + "#speed=" + str(speed)
    print("sending ")
    print(msg)
    #sock.bind((ip,0))
    sock.sendto(msg.encode(), ('<broadcast>', 11011))
    time.sleep(2)
    sock.close()

def main(speed, lat, lon):
    prev_lat = lat
    prev_lon = lon
    prev_speed = speed
    # Start sending packets at 30s interval
    elapsed_time = 30  # in s
    
        # lat, lon = get_loc()
    if prev_lat == 0 and prev_lon == 0:
        # Initial broadcast
        udp_broadcast(str(lat), str(lon), 0)
        prev_lat = lat
        prev_lon = lon
    else:
        points = []
        prev_coord = []
        coord = []
        prev_coord.append(float(prev_lat))
        prev_coord.append(float(prev_lon))
        points.append(prev_coord)
        coord.append(float(lat))
        coord.append(float(lon))
        points.append(coord)
        speed = getSpeed(points, elapsed_time)
        print("calculated speed : " + str(speed))

        # Send the broadcast
        udp_broadcast(str(lat), str(lon), speed)

        # Save current location as prev location
        prev_lat = lat
        prev_lon = lon
    string = str(prev_lat) + "," + str(prev_lon)
    return string

if __name__ == "__main__":
    main()