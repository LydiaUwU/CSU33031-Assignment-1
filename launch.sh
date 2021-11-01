# Script to launch all the devices created by initialise.sh
# Author: Lydia MacBride

echo -e "🌙 Launching components"

# Launch server
echo -e "\n🌐 Launching server"
sudo docker container start a1-server

# Launch sensors
echo -e "\n🦉 Launching sensors"
sudo docker container start $(sudo docker container ls -a -q -f name="a1-sensor*") > /dev/null

# Launch actuators
echo -e "\n🏃 Launching actuators"
sudo docker container start $(sudo docker container ls -a -q -f name="a1-actuator*") > /dev/null

# Launch and connect to client
echo -e "\n✨ Launching client"
./client.sh