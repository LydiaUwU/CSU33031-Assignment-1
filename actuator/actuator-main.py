# Actuator device to receive commands from Server
# Author: Lydia MacBride

import socket


print("Starting actuator")

# Device parameters
port = 4444
buff_size = 4096
dev_type = "2"
dev_id = ""
dev_value = ""
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

    # Process various commands from devices
    # Acknowledge packets
    if pck_arr[0] == "ack":
        print("Acknowledgment from: " + pck_arr[1] + ":" + pck_arr[2])

        # Pull ack_type from packet
        ack_type = pck_str[8:]

        # Remove queued request if match found
        for i in queue:
            if i[1] == ack_type:
                queue.remove(i)
                break

    # Publish command packet
    if pck_arr[0] == "pub":
        print("Publish command from: " + pck_arr[1] + ":" + pck_arr[2] + ", Containing: " + pck_arr[3])

        global dev_value
        dev_value = pck_arr[3]  # update dev_value with incoming data

    else:
        # Send acknowledgement
        send_ack(pck_address, pck_str)


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
            # Update device info
            print("New device ID: " + new_arr[4])
            dev_id = new_arr[4]

            # Send acknowledgement
            print("Sending acknowledgement")
            send_ack(new_address, new_str)


# Main loop
while True:
    # TODO: Only send status on receiving a command
    outgoing_upd = False
    for i in queue:
        if i[1][0:3] == "upd":
            outgoing_upd = True

    if not outgoing_upd:
        send_value()

    # Process incoming packets and send any queued packets
    rec_packet()
    send_packet()
