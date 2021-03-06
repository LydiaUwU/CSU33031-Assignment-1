# Script to launch all the devices created by initialise.sh
# Author: Lydia MacBride

echo -e "š Launching components"

# Launch server
echo -e "\nš Launching server"
sudo docker container start a1-server

# Launch sensors
echo -e "\nš¦ Launching sensors"
sudo docker container start $(sudo docker container ls -a -q -f name="a1-sensor*") > /dev/null

# Launch actuators
echo -e "\nš Launching actuators"
sudo docker container start $(sudo docker container ls -a -q -f name="a1-actuator*") > /dev/null

# Launch and connect to client
echo -e "\nāØ Launching client"
./client.sh