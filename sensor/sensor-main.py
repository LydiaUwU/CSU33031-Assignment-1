# Sensor device for sending dummy data to Server
# Author: Lydia MacBride

import socket
import random


print("Starting sensor")

# List of possible device groups, will be randomly assigned for demonstration purposes
groups = ["thermometers", "barometers", "motion-sensors", "light-sensors"]
group = random.choice(groups)
print("Group is: " + group)

# Device parameters
port = 4444
buff_size = 4096
dev_type = "1"
dev_id = ""
dev_value = "20"
server_ip = ""
queue = list()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(20)
# Bind the socket it to the port
sensor_address = ('0.0.0.0', port)
s.bind(sensor_address)


# Add packet to queue
def queue_packet(packet):
    print("Adding packet to queue")

    pck_exists = False
    for pck in queue:
        pck_exists = pck[1] == packet[1]
        print("Checking: " + pck[1] + ", " + packet[1] + ", match: " + str(pck_exists))
        break

    if len(queue) == 0 or not pck_exists:
        queue.append(packet)


# Send acknowledgement to given ip
# Acknowledgement format [ack:<dev_type>:<dev_id>:<original_packet>]
def send_ack(ack_ip, ack_type):
    print("Sending acknowledgement to: " + ack_ip[0])
    ack_data = "ack:" + dev_type + ":" + dev_id + ":" + ack_type

    # Save packet to queue
    queue_packet([ack_ip[0], ack_data])


# Send dev_value as upd packet
def send_value():
    print("Sending value to server")
    val_data = "upd:" + str(dev_type) + ":" + str(dev_id) + ":" + str(dev_value)

    # Save packet to queue
    queue_packet([server_ip, val_data])


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

    # Send acknowledgement
    if pck_arr[0] != "ack":
        send_ack(pck_address, pck_str)

    # Process various commands from devices
    # Acknowledge packets
    if pck_arr[0] == "ack":
        print("Acknowledgment from: " + pck_arr[1] + ":" + pck_arr[2])

        # Pull ack_type from packet
        ack_type = pck_str[8:]

        # Remove queued request if match found
        for pck in queue:
            if pck[1] == ack_type:
                queue.remove(pck)
                break


# Send packets from queue
def send_packet():
    for pck in queue:
        print("Sending packet: " + pck[1] + ", To: " + pck[0])
        s.sendto(pck[1].encode("utf-8"), (pck[0], port))

        # If i is an acknowledge packet, remove it from queue
        if pck[1][0:3] == "ack":
            print("Removing acknowledgment: " + pck[1])
            queue.remove(pck)


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
    new_data = "new:" + dev_type + ":" + group
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
            # Update device info
            print("New device ID: " + new_arr[4])
            dev_id = new_arr[4]

            # Send acknowledgement
            print("Sending acknowledgement")
            send_ack(new_address, new_str)


# Main loop
while True:
    # TODO: Put this on its own thread and use a timer
    # Generate dev_value and add packet to queue if theres no current outgoing update
    outgoing_upd = False
    for i in queue:
        if i[1][0:3] == "upd":
            outgoing_upd = True

    if not outgoing_upd:
        dev_value = str(float(dev_value) + random.random() - 0.5)
        send_value()

    # Process incoming packets and send any queued packets
    rec_packet()
    send_packet()
