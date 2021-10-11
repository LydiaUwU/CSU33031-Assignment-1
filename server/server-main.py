# Main server script to initialise, control and monitor devices
# Author: Lydia MacBride
# TODO: Send command packet to actuators [cmd:0:0:<dev_value>]

import socket
import devices


print("Starting server")

# Global
ip = socket.gethostbyname("a1-server")
port = 4444
buff_size = 4096

# Network devices
sensors = list()
actuators = list()

# Packets to send
# List contains pairs of [dest_ip, data] that are awaiting acknowledgement
queue = list()

# Initialisation
# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)


# Add packet to queue
def queue_packet(packet):
    pck_exists = False
    for i in queue:
        pck_exists = i[1] == packet[1]
        print("Checking: " + i[1] + ", " + packet[1] + ", match: " + str(pck_exists))
        break

    if len(queue) == 0 or not pck_exists:
        print("Adding packet to queue: " + packet[1])
        queue.append(packet)


# Send acknowledgement to given ip
# Acknowledgement format [ack:<dev_type>:<dev_id>:<original_packet>]
def send_ack(ack_ip, ack_type):
    print("Sending acknowledgement to: " + ack_ip[0])
    ack_data = "ack:0:0:" + ack_type  # 0:0 to denote type server

    # Save packet to queue
    queue_packet([ack_ip, ack_data])


# Send device id
def send_dev_id(dev_ip, dev_id):
    print("Sending device information to: " + dev_ip[0])
    dev_data = "new:0:0:" + str(dev_id)  # 0:0 to denote type server

    # Save packet to queue
    queue_packet([dev_ip, dev_data])


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
        print("Checking for acknowledgment: " + ack_type)
        for i in queue:
            if i[1] == ack_type:
                queue.remove(i)

    # New device packets
    elif pck_arr[0] == "new":
        print("Adding new device")

        # Get device type and generate dev_id
        dev_type = pck_arr[1]
        dev_id = len(sensors) if dev_type == '1' else len(actuators)

        # Check that ip isn't already added
        dev_found = False
        for i in (sensors if dev_type == '1' else actuators):
            if i.dev_address == pck_address[0]:
                send_dev_id(pck_address[0], dev_id)
                dev_found = True
                break

        # Check for sensor or actuator and add to list
        if not dev_found:
            new_dev = devices.Device(1, dev_id, pck_address[0])

            if dev_type == '1':
                sensors.append(new_dev)

                # Print current sensors
                for i in sensors:
                    print("Sensor: " + str(i.get_dev_id()))

            elif dev_type == '2':
                actuators.append(new_dev)

                # Print current actuators
                for i in actuators:
                    print("Actuator: " + str(i.get_dev_id()))

            # Send device id back to device
            send_dev_id(pck_address[0], dev_id)

        # Send acknowledgement
        send_ack(pck_address[0], pck_str)

    # Device update packets
    elif pck_arr[0] == "upd":
        print("Updating device parameters")
        dev_type = pck_arr[1]
        dev_id = pck_arr[2]
        dev_value = pck_arr[3]

        # Find matching device id and update dev_value
        for i in (sensors if dev_type == '1' else actuators):
            print("Checking device: " + str(i.get_dev_type()) + ":" + str(i.get_dev_id()))
            if dev_id == str(i.get_dev_id()):
                i.update(dev_value)
                print("Updated device value for: " + dev_type + ":" + dev_id + ", to: " + dev_value)
                break

        # Send acknowledgement
        send_ack(pck_address[0], pck_str)


# Send packets from queue
def send_packet():
    for i in queue:
        print("Sending packet: " + i[1] + ", To: " + i[0])
        s.sendto(i[1].encode("utf-8"), (i[0], port))

        # If i is an acknowledge packet, remove it from queue
        if i[1][0:3] == "ack":
            print("Removing acknowledgment: " + i[1])
            queue.remove(i)


# Main function loop
while True:
    rec_packet()
    send_packet()
