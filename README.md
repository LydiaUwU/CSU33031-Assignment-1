# CSU33031-Assignment-1
My implementation for CSU33031 Computer Networks assignment 1.

## Packet format
``<packet_type>:<sender_type>:<sender_id>:<data>``
- `ack` - Acknowledgement packet
- `new` - Sent by any initialising device to server to request for a unique ID
- `upd` - Sent from sensors/actuators to the server containing their current data, passed to clients
- `syn` - Device list sync request from client to server
- `sub` - Sent from client to subscribe to data from a given sensor
- `pub` - Sent from client to publish a command to an actuator

## SUCCESS PT1
- Server and Sensor programs fleshed out
- Server accepts three request types indicated by ack, new and upd
- Client sends new request to server when initialising and server replies with a unique numerical identifier for the client
- Once initialised client sends random dummy data to the server using upd request
- Server stores any received upd requests in its list of devices corresponding to the sender's type and ID
- Server and client capable of queueing requests to send, and removes each once they receive a corresponding acknowledgement.
- Unacknowledged requests will be resent until acknowledgement is received

## Software used
- Python 3
- Docker
- Pycharm

## Setup, launching and removal
- To setup the network for the first time run `./initialise.sh`
- To launch the network once setup run `./launch.sh`
- To stop running containers run `./stop.sh`
- To remove docker configuration run `./remove.sh`

## Todo list
- ✅ Write setup process
- ✅ Create network layout diagram
- ✅ Create docker network
- ✅ Create docker machines for server, sensors and actuators
- ✅ Ensure that traffic can be monitored with wireshark
- ✅ Create script to allow user to easily instantiate and launch the network
  - ~~Research passing arguments via dockerfile (IP and port for server and actuator)~~
- Revise network topology for client CLI instead of websites.
- Move individual packet/command functionality to individual methods

### Server
- ✅ Instantiate each new device with a unique ID
- ✅ Receive information from sensors
- Allow client to subscribe to available sensors
- Publish sensor/actuator info to clients
- Allow client to send commands to actuators

### Client
- Receive and process commands from user
  - Send appropriate packets based on commands
- ~~Flask webpage for client~~
- Display subscribed sensor information on ~~webpage~~ client CLI
- ~~Basic but not programmer art website layout~~

### Sensors
- ✅ Connects to server to receive unique ID when starting
- Create two types of sensor (toggle and variable)
- ✅ Send information to server at regular intervals
- ✅ Random dummy data that changes over time

### Actuators
- Create two types of actuator (toggle and variable)
- Receive commands from server
- Send current status to server when requested

## Attributions
- My lecturer Prof. Stefan Weber
- https://linuxhint.com/send_receive_udp_python/
- https://flask.palletsprojects.com/