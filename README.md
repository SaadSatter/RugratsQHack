# RugratsQHack

# Introduction

This project directory consists of client (pedastrian) side and server (vehicle) side code.

1. Server code (sender.py) scraps the location websites to retrieve the latitude and longitude of the vehicle and converts it to X-Y coordinates and sends the UDP broadcast with a dynamically changing frequency based on its speed.
2. The client side code (priority.py) polls the socket port 11011 for UDP broadcast message. Once it receives the broadcast, the poll threads enqueue the message into a common buffer protected by locks. Another two threads called processing threads read from the buffer and compute the distance and collision angle along with the trajectory of the vehicles. This message is enqueued into another buffer which is dequeued by the main thread which reads from it whenever the buffer size reaches 3 to simulate the effect of having 3 oncoming vehicles. Once the buffer is emptied, it enqueues the messages into a priority queue based on ETA of the vehicle and alerts the user of the direction in which the vehicle is arriving.


# Steps to run the scripts

1. Install the required packages specified in client and server scripts.
2. Connect to same network for both vehicle and pedestrian. (Non-Qualcomm networks, as Qualcomm networks don't allow broadcast/multicast packets).
3. Make sure you are running on linux/macOS or have disabled firewall on windows based systems to allow selenium to scrap the website.
4. Run priority.py on pedestrian side
5. Run sender.py on vehicle side.
6. Wait for 1 min for system to stabilize and move the vehicle towards pedestrian.
7. After the vehicle is in the radius, the client is informed of an incoming vehicle.
8. The same steps can be reproduced with the included Android App as well.
