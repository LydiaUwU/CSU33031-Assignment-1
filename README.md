# CSU33031-Assignment-1
My implementation for CSU33031 Computer Networks assignment 1.

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
- Create network layout diagram
- Create docker network
- Create docker machines for server, sensors and actuators
- Ensure that traffic can be monitored with wireshark
- Create script to allow user to easily instantiate and launch the network
  - Research passing arguments via dockerfile (IP and port for server and actuator)

### Server
- Receive information from sensors
- Flask webpage for client
- Allow client to subscribe to available sensors
- Display subscribed sensor information on webpage
- Basic but not programmer art website layout
- Allow client to send commands to actuators

### Sensors
- Create two types of sensor (toggle and variable)
- Send information to server at regular intervals
- Random dummy data that changes over time

### Actuators
- Create two types of actuator (toggle and variable)
- Receive commands from server
- Send current status to server when requested

## Attributions
- My lecturer Prof. Stefan Weber
- https://linuxhint.com/send_receive_udp_python/
- https://flask.palletsprojects.com/