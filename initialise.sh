# Script to initialise and configure containers and network
# Author: Lydia MacBride

# Variables
if [ $# -eq 0 ] || [ $# -eq 1 ]
  then
    # Defaults when no arguments provided
    sensor_count=3
    actuator_count=3
else
  sensor_count=$1
  actuator_count=$2
fi

subnet=172.20.0.0/16

echo "š Beginning initialisation"

# Create network
echo -e "\nš Creating network"
sudo docker network create -d bridge --subnet $subnet a1-network

# Create containers
# Create server
echo -e "\nš Creating server"
sudo docker build -t a1-server ./server
sudo docker container create --name a1-server --cap-add=ALL a1-server
echo -e "\nš Connecting container to network"
sudo docker network connect a1-network a1-server

# Create client
echo -e "\nš  Creating client"
sudo docker build -t a1-client ./client
sudo docker container create --name a1-client --cap-add=ALL a1-client
echo -e "\nš Connecting container to network"
sudo docker network connect a1-network a1-client

# Create sensors
echo -e "\nš¦ Creating sensor(s)"
sudo docker build -t a1-sensor ./sensor

for ((i=0; i < sensor_count; i++)) do
  sudo docker container create --name "a1-sensor$i" --cap-add=ALL a1-sensor
  echo -e "\nš Connecting container a1-sensor$i to network"
  sudo docker network connect a1-network a1-sensor"$i"
done

# Create actuators
 echo -e "\nš Creating actuator(s)"
 sudo docker build -t a1-actuator ./actuator

 for ((i=0; i < actuator_count; i++)) do
   sudo docker container create --name "a1-actuator$i" --cap-add=ALL a1-actuator
   echo -e "\nš Connecting container a1-actuator$i to network"
   sudo docker network connect a1-network a1-actuator"$i"
 done

# List created containers
echo -e "\nš³ The following containers were created"
sudo docker container ls -a -f name="a1-*"

# Ask input on whether to launch or not
# echo -e "\n"
# read -p "ā Do you want to launch the created containers? [Y/n] " yn
# case $yn in
#    [Yy]* ) echo -e "\n"; ./launch.sh;;
# esac

# Finished!
echo -e "\nšŗ All done initialising!"
