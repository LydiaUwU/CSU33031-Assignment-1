# Script to initialise and configure containers and network
# Author: Lydia MacBride

# Variables
# TODO: Arguments to adjust variables
sensor_count=3
actuator_count=1
subnet=172.20.0.0/16

echo "🌙 Beginning initialisation"

# Create network
echo -e "\n🌐 Creating network"
sudo docker network create -d bridge --subnet $subnet a1-network

# Create containers
# Create server
echo -e "\n🎏 Creating server"
sudo docker build -t a1-server ./server
sudo docker container create --name a1-server --cap-add=ALL a1-server
echo -e "\n🌐 Connecting container to network"
sudo docker network connect a1-network a1-server

# Create client
echo -e "\n🌠 Creating client"
sudo docker build -t a1-client ./client
sudo docker container create --name a1-client --cap-add=ALL a1-client
echo -e "\n🌐 Connecting container to network"
sudo docker network connect a1-network a1-client

# Create sensors
echo -e "\n🦉 Creating sensor(s)"
sudo docker build -t a1-sensor ./sensor

for ((i=0; i < sensor_count; i++)) do
  sudo docker container create --name "a1-sensor$i" --cap-add=ALL a1-sensor
  echo -e "\n🌐 Connecting container a1-sensor$i to network"
  sudo docker network connect a1-network a1-sensor"$i"
done

# Create actuators
 echo -e "\n🏃 Creating actuator(s)"
 sudo docker build -t a1-actuator ./actuator

 for ((i=0; i < actuator_count; i++)) do
   sudo docker container create --name "a1-actuator$i" --cap-add=ALL a1-actuator
   echo -e "\n🌐 Connecting container a1-actuator$i to network"
   sudo docker network connect a1-network a1-actuator"$i"
 done

# List created containers
echo -e "\n🐳 The folllowing containers were created"
sudo docker container ls -a -f name="a1-*"

# Ask input on whether to launch or not
# echo -e "\n"
# read -p "❓ Do you want to launch the created containers? [Y/n] " yn
# case $yn in
#    [Yy]* ) echo -e "\n"; ./launch.sh;;
# esac

# Finished!
echo -e "\n😺 All done initialising!"
