import os
import time
import socket
import haversine as hs
import math
import server
import client
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

def main(prevLat, prevLon, lat, lon, personAngle):
    print("previos coord: ", prevLat, prevLon)
    prev_lat = prevLat
    prev_lon = prevLon
    prev_speed = 0.0
    # Start sending packets at 30s interval
    elapsed_time = 10  # in s
    lat, lon = (lat,lon)
    if prev_lat == 0 and prev_lon == 0:
        # Initial broadcast
        # udp_broadcast(str(lat), str(lon), 0)
        prev_lat = lat
        prev_lon = lon
        return str(prev_lat) + "," + str(prev_lon)
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
        if(speed > 3):
            val = server.main(speed, lat, lon)
                # Dynamically change the time to wait based on current speed
            if speed > prev_speed:
                if elapsed_time > 10:
                    elapsed_time -= 1
            else:
                if elapsed_time < 50:
                    elapsed_time += 1
                prev_speed = speed
            print("elapsed_time:", elapsed_time)
            time.sleep(elapsed_time)
            return val;
        else:
            val = client.main(lat, lon, personAngle)
            return val;

        
if __name__ == "__main__":
    main()