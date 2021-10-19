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
s.settimeout(5)
# Bind the socket it to the port
sensor_address = ('0.0.0.0', port)
s.bind(sensor_address)


# Send acknowledgement to given ip
# Acknowledgement format [ack:<dev_type>:<dev_id>:<original_packet>]
def send_ack(ack_ip, ack_type):
    print("Sending acknowledgement to: " + ack_ip[0])
    ack_data = "ack:" + dev_type + ":" + dev_id + ":" + ack_type

    # Save packet to queue
    queue_packet([server_ip, ack_data])


# TODO: Process inputs from user
# Process input from user
def proc_input():
    try:
        user_in = input("✨〉")
    except EOFError:
        print("Input not found")
        return

    # sync: Sync device list with server
    if user_in == "sync":
        print("Syncing devices with server")
        syn_data = "syn:" + dev_type + ":" + dev_id
        queue_packet([server_ip, syn_data])
        rec_packet(True)

    # ls (-sensors, -actuators): List sensor/actuator devices
    elif user_in[0:2] == "ls":
        args = ["-sensors" in user_in, "-actuators" in user_in]  # Store whether arguments are set or not

        # List sensors
        if args[0] or args[0] == args[1]:
            print("\nSensors\n" +
                  "ID\t\tData")

            for i in sensors:
                print(str(i.dev_type) + ":" + str(i.dev_id) + "\t\t" + str(i.dev_value))

        # List actuators
        if args[1] or args[0] == args[1]:
            print("\nActuators\n" +
                  "ID\t\tData")

            for i in sensors:
                print(str(i.dev_type) + ":" + str(i.dev_id) + "\t\t" + str(i.dev_value))

        print("")

    # sub <ID>: Subscribe to sensor data
    elif user_in[0:3] == "sub":
        user_str = user_in[4:].split(":")
        user_type = user_str[0]
        user_id = user_str[1]

        if user_type == '1':  # Sensors
            if int(user_id) > len(sensors):
                print("Invalid device ID")
                return

        elif user_type == 2:  # Actuators
            print("Can't subscribe to actuators!")
            return

        else:
            print("Invalid device ID")
            return

        sub_data = "sub:" + dev_type + ":" + dev_id + ":" + user_in[4:]
        print("Subscribing to device: " + sub_data)
        queue_packet([server_ip, sub_data])

    # pub <ID> <value>: Publish command to actuator
    elif user_in[0:3] == "pub":
        user_str = user_in[4:].split(":")
        user_type = user_str[0]

        if user_type != '2':
            print("Only actuators can receive commands!")
            return

        pub_data = "pub:" + dev_type + ":" + dev_id + ":" + user_in[4:]
        print("Publishing command: " + pub_data)
        queue_packet([server_ip, pub_data])

    # rec <time>: Open packet requests for a given amount of time
    elif user_in[0:3] == "rec":
        s.settimeout(int(user_in[4:]))  # TODO: ensure integer value passed in
        rec_packet(False)
        s.settimeout(5)

    # send: Send queue
    elif user_in[0:4] == "send":
        while len(queue) > 0:
            send_packet()
            rec_packet(False)

    # help: Print available commands
    elif user_in == "help":
        print("sync                         Sync device list with server\n" +
              "ls (-sensors, -actuators)    List sensor/actuator devices\n" +
              "sub <Type>:<ID>              Subscribe to sensor data\n" +
              "pub <Type>:<ID> <value>      Publish command to actuator\n" +
              "rec <time>                   Open packet requests for a given amount of time\n" +
              "send                         Send queue\n" +
              "help                         print available commands")

    # Invalid input
    else:
        print("Invalid input. Run help to see available commands")


# Process incoming packets
def rec_packet(recur):
    recur_local = True
    while recur_local:

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

        # Device update packets
        elif pck_arr[0] == "upd":
            print("Updating device parameters")
            upd_type = pck_arr[1]
            upd_id = pck_arr[2]
            upd_value = pck_arr[3]

            # Find matching device id and update upd_value
            for i in (sensors if upd_type == '1' else actuators):
                print("Checking device: " + str(i.get_upd_type()) + ":" + str(i.get_upd_id()))
                if upd_id == str(i.get_upd_id()):
                    i.update(upd_value)
                    print("Updated device value for: " + upd_type + ":" + upd_id + ", to: " + upd_value)
                    break

        # Sync packet
        elif pck_arr[0] == "syn":
            syn_type = pck_arr[1]
            syn_id = pck_arr[2]
            syn_data = pck_arr[3]

            print("Sync packet received")
            # Sync process ending
            if syn_type == 'end':
                print("Ending sync")
                send_ack(pck_address, pck_str)
                return

            elif syn_type == '1':
                if int(syn_id) > len(sensors) - 1:
                    sensors.extend([None] * (int(syn_id) - (len(sensors) - 1)))

                sensors[int(syn_id)] = devices.Device(syn_type, syn_id, False, syn_data)

            elif syn_type == '2':
                if int(syn_id) > len(actuators) - 1:
                    actuators.extend([None] * (int(syn_id) - (len(actuators) - 1)))

                    actuators[int(syn_id)] = devices.Device(syn_type, syn_id, False, syn_data)

            else:
                print("Invalid device type received")

            send_ack(pck_address, pck_str)
            rec_packet(True)  # Recur to continue sync process

        else:
            print("Unknown packet type received: " + pck_arr[0])

        # Send acknowledgement
        if pck_arr[0] != "ack":
            send_ack(pck_address, pck_str)

        recur_local = recur

        if recur_local:
            send_packet()


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
            # Update device info
            print("New device ID: " + new_arr[4])
            dev_id = new_arr[4]

            # Clear queue
            queue.clear()

            # Send acknowledgement
            print("Sending acknowledgement")
            send_ack(new_address, new_str)


# Main Loop
while True:
    proc_input()
    rec_packet(False)  # TODO: Run in thread
    send_packet()
