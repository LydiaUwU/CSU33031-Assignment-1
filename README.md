# CSU33031-Assignment-1
My implementation for CSU33031 Computer Networks assignment 1.

Please read the included pdf for in depth information about the protocol and implementation. 

## Packet format
``<packet_type>:<sender_type>:<sender_id>:<data>``
- `ack` - Acknowledgement packet
- `new` - Sent by any initialising device to server to request for a unique ID
- `upd` - Sent from sensors/actuators to the server containing their current data, passed to clients
- `syn` - Device list sync request from client to server
- `sub` - Sent from client to subscribe to data from a given sensor
- `pub` - Sent from client to publish a command to an actuator

## Software used
- Python 3
- Docker
- Pycharm

## Setup, launching and removal
- To setup the network for the first time run `./initialise.sh`, which can be supplied with two integer parameters specifying how many sensor and actuator devices you wish to instantiate (defaults for both is 3), i.e. `./initialise.sh 5 6` will create 5 sensors and 6 actuators.
- To launch the network once setup run `./launch.sh`, this will automatically connect you to a client.
- To stop running containers run `./stop.sh`
- To remove docker configuration run `./remove.sh`

## Attributions
- My lecturer Prof. Stefan Weber
- https://linuxhint.com/send_receive_udp_python/
- https://flask.palletsprojects.com/