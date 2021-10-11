# Client providing CLI for user to interact with network
# Author: Lydia MacBride

import socket
import devices


print("Starting Client")

# Device parameters
port = 4444
buff_size = 4096
dev_type = "3"
dev_id = ""
server_ip = ""
queue = list()

# Network devices
sensors = list()
actuators = list()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(20)
# Bind the socket it to the port
sensor_address = ('0.0.0.0', port)
s.bind(sensor_address)


# Send acknowledgement to given ip
# Acknowledgement format [ack:<dev_type>:<dev_id>:<original_packet>]
def send_ack(ack_ip, ack_type):
    print("Sending acknowledgement to: " + ack_ip[0])
    ack_data = "ack:" + dev_type + ":" + dev_id + ":" + ack_type

    # Save packet to queue
    queue_packet([ack_ip[0], ack_data])


# TODO: Process inputs from user
# Process input from user
def proc_input():
    user_in = input("✨〉")

    # TODO: sync: Sync device list with server
    if user_in == "sync":
        print("Syncing devices with server")

    # TODO: ls (-sensors, -actuators): List sensor/actuator devices
    elif user_in[0:2] == "ls":
        # TODO: Process arguments
        print("Listing devices")

    # sub <ID>: Subscribe to sensor data
    elif user_in[0:3] == "sub":
        sub_data = "sub:" + dev_type + ":" + dev_id + ":" + user_in[4:]
        print("Subscribing to device: " + sub_data)
        queue_packet([server_ip, sub_data])

    # pub <ID> <value>: Publish command to actuator
    elif user_in[0:3] == "pub":
        pub_data = "pub:" + dev_type + ":" + dev_id + ":" + user_in[4:]
        print("Publishing command: " + pub_data)
        queue_packet([server_ip, pub_data])

    # help: Print available commands
    elif user_in == "help":
        print("sync                         Sync device list with server\n" +
              "ls (-sensors, -actuators)    List sensor/actuator devices\n" +
              "sub <Type>:<ID>              Subscribe to sensor data\n" +
              "pub <Type>:<ID> <value>      Publish command to actuator\n" +
              "help                         print available commands")

    # Invalid input
    else:
        print("Invalid input. Run help to see available commands")


# Process incoming packets
def rec_packet():
    print("Awaiting packet")

    # Receive packet or handle timeout
    try:
        pck_data, pck_address = s.recvfrom(buff_size)
    except socket.timeout:
        print("Connection timed out")
        return

    pck_str = pck_data.decode("utf-8")
    pck_arr = pck_str.split(':')
    print("Received packet: " + pck_str + ", From: " + pck_address[0])

    # Process various commands from devices
    # Acknowledge packets
    if pck_arr[0] == "ack":
        print("Acknowledgment from: " + pck_arr[1] + ":" + pck_arr[2])

        # Pull ack_type from packet
        ack_type = ""
        for i in range(3, len(pck_arr)):
            ack_type += pck_arr[i] + (":" if i < len(pck_arr) - 1 else "")

        # Remove queued request if match found
        for i in queue:
            if i[1] == ack_type:
                queue.remove(i)
                break

    # TODO: upd, syn packet types

    else:
        # Send acknowledgement
        send_ack(pck_address, pck_str)


# Add packet to queue
def queue_packet(packet):
    print("Adding packet to queue")

    pck_exists = False
    for i in queue:
        pck_exists = i[1] == packet[1]
        print("Checking: " + i[1] + ", " + packet[1] + ", match: " + str(pck_exists))
        break

    if len(queue) == 0 or not pck_exists:
        queue.append(packet)


# Send packets from queue
def send_packet():
    for i in queue:
        print("Sending packet: " + i[1] + ", To: " + i[0])
        s.sendto(i[1].encode("utf-8"), (i[0], port))

        # If i is an acknowledge packet, remove it from queue
        if i[1][0:3] == "ack":
            print("Removing acknowledgment: " + i[1])
            queue.remove(i)


# Initialisation
# Get server IP
print("Getting server IP")
while True:
    try:
        server_ip = socket.gethostbyname("a1-server")
    except socket.gaierror:
        print("Server IP not found, retrying")
        continue
    break

# Send new device packet to server
while dev_id == "":
    print("Sending device information request to server")
    new_data = "new:" + dev_type
    queue_packet([server_ip, new_data])
    send_packet()

    # Receive device info from server
    print("Awaiting packet from server")

    # Receive packet or handle timeout
    try:
        new_data, new_address = s.recvfrom(buff_size)
    except socket.timeout:
        print("Connection timed out")
        continue

    if new_data is not None:
        new_str = new_data.decode("utf-8")
        new_arr = new_str.split(':')
        print("Received device information packet: " + new_str)

        if new_arr[0] == "new":
            # Send acknowledgement
            print("Sending acknowledgement")
            send_ack(new_address, new_str)

            # Update device info
            print("New device ID: " + new_arr[3])
            dev_id = new_arr[3]

# Main Loop
while True:
    proc_input()
    rec_packet()  # TODO: Run in thread
    send_packet()
