# Client providing CLI for user to interact with network
# Author: Lydia MacBride
# TODO: Move classes to own python scripts

import socket
import threading
import time
import devices

print("Starting Client")

# Device parameters
port = 4444
buff_size = 4096
dev_type = "3"
dev_id = ""
server_ip = ""
queue = list()
debug = False

# Network devices
sensors = list()
actuators = list()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)
# Bind the socket it to the port
sensor_address = ('0.0.0.0', port)
s.bind(sensor_address)

# Running boolean
running = True


# Print only if debug enabled
def print_d(string):
    if debug:
        print(string)


# Add packet to queue
def queue_packet(packet): 
    print_d("Adding packet to queue")

    pck_exists = False
    for i in queue:
        pck_exists = i[1] == packet[1]
        
        print_d("Checking: " + i[1] + ", " + packet[1] + ", match: " + str(pck_exists))
        break

    if len(queue) == 0 or not pck_exists:
        queue.append(packet)


# Send acknowledgement to given ip
# Acknowledgement format [ack:<dev_type>:<dev_id>:<original_packet>]
def send_ack(ack_ip, ack_type):
    print_d("Sending acknowledgement to: " + ack_ip[0])
    ack_data = "ack:" + dev_type + ":" + dev_id + ":" + ack_type

    # Save packet to queue
    queue_packet([server_ip, ack_data])


# Process incoming packets
def rec_packet():
    print_d("Awaiting packet")

    # Receive packet or handle timeout
    try:
        pck_data, pck_address = s.recvfrom(buff_size)
    except socket.timeout:
        print_d("Connection timed out")
        return

    pck_str = pck_data.decode("utf-8")
    pck_arr = pck_str.split(':')
    print_d("Received packet: " + pck_str + ", From: " + pck_address[0])

    # Process various commands from devices
    # Acknowledge packets
    if pck_arr[0] == "ack":
        print_d("Acknowledgment from: " + pck_arr[1] + ":" + pck_arr[2])

        # Pull ack_type from packet
        ack_type = pck_str[8:]

        # Remove queued request if match found
        for i in queue:
            if i[1] == ack_type:
                queue.remove(i)
                break

    # Device update packets
    elif pck_arr[0] == "upd":
        print_d("Updating device parameters")
        upd_type = pck_arr[1]
        upd_id = pck_arr[2]
        upd_value = pck_arr[3]

        # Find matching device id and update upd_value
        for i in (sensors if upd_type == '1' else actuators):
            print_d("Checking device: " + str(i.get_upd_type()) + ":" + str(i.get_upd_id()))
            if upd_id == str(i.get_upd_id()):
                i.update(upd_value)
                print_d("Updated device value for: " + upd_type + ":" + upd_id + ", to: " + upd_value)
                break

    # Sync packet
    elif pck_arr[0] == "syn":
        syn_type = pck_arr[1]
        syn_id = pck_arr[2]
        syn_data = pck_arr[3]

        print_d("Sync packet received")
        if syn_type == '1':
            if int(syn_id) > len(sensors) - 1:
                sensors.extend([None] * (int(syn_id) - (len(sensors) - 1)))

            sensors[int(syn_id)] = devices.Device(syn_type, syn_id, False, syn_data)

        elif syn_type == '2':
            if int(syn_id) > len(actuators) - 1:
                actuators.extend([None] * (int(syn_id) - (len(actuators) - 1)))

            actuators[int(syn_id)] = devices.Device(syn_type, syn_id, False, syn_data)

        else:
            print_d("Invalid device type received")

    else:
        print_d("Unknown packet type received: " + pck_arr[0])

    # Send acknowledgement
    if pck_arr[0] != "ack":
        send_ack(pck_address, pck_str)


# Process input from user
# TODO: Block threads from printing when prompt is displayed
class ProcessInput(threading.Thread):
    def run(self):
        global running
        while running:
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

                    for i in actuators:
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

                # TODO: Run sync after subscribing

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

            # debug: Display debug output
            elif user_in == "debug":
                global debug
                debug = not debug
                print("Debug output " + "enabled" if debug else "disabled")

            # exit: Shutdown client
            elif user_in == "exit":
                print("Shutting down")
                running = False

            # help: Print available commands
            elif user_in == "help":
                print("sync                         Sync device list with server\n" +
                      "ls (-sensors, -actuators)    List sensor/actuator devices\n" +
                      "sub <Type>:<ID>              Subscribe to sensor data\n" +
                      "pub <Type>:<ID> <value>      Publish command to actuator\n" +
                      "debug                        Display debug output\n" +
                      "exit                         Stop and exit client\n" +
                      "help                         print available commands")

            # Invalid input
            else:
                print("Invalid input. Run help to see available commands")


# Send packets from queue
class SendPacket(threading.Thread):
    def run(self):
        global running
        while running:
            # Sleep for a few seconds to stop packet spam
            time.sleep(1.0)

            for i in queue:
                print_d("Sending packet: " + i[1] + ", To: " + i[0])
                s.sendto(i[1].encode("utf-8"), (i[0], port))

                # If i is an acknowledge packet, remove it from queue
                if i[1][0:3] == "ack":
                    print_d("Removing acknowledgment: " + i[1])
                    queue.remove(i)


# Initialisation
# Start SendPacket thread
send_packet = SendPacket()
send_packet.start()

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

# Start ProcessInput thread
proc_input = ProcessInput()
proc_input.start()

# Main Loop
while running:
    rec_packet()

# End of program
send_packet.join()
proc_input.join()
