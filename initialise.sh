# Script to initialise and configure containers and network
# Author: Lydia MacBride

echo "🌙 Beginning initialisation"

# Create network
echo -e "\n🌐 Creating network"
sudo docker network create -d bridge --subnet 172.20.0.0/16 a1-network

# Create containers
# Create server
echo -e "\n🎏 Creating server"
sudo docker build -t a1-server ./server
sudo docker container create --name a1-server --cap-add=ALL a1-server
echo -e "\n🌐 Connecting container to network"
sudo docker network connect a1-network a1-server

# Create sensors
# TODO: Accept argument to create multiple
echo -e "\n🦉 Creating sensor(s)"
sudo docker build -t a1-sensor ./sensor
sudo docker container create --name a1-sensor --cap-add=ALL a1-sensor
echo -e "\n🌐 Connecting container to network"
sudo docker network connect a1-network a1-sensor

# Create actuators
# TODO: Accept argument to create multiple
echo -e "\n🦉 Creating actuator(s)"
sudo docker build -t a1-actuator ./actuator
sudo docker container create --name a1-actuator --cap-add=ALL a1-actuator
echo -e "\n🌐 Connecting container to network"
sudo docker network connect a1-network a1-actuator

# List created containers
echo -e "\n🐳 The folllowing containers were created"
sudo docker container ls -a -f name="a1-*"

# Ask input on whether to launch or not
echo -e "\n"
read -p "❓ Do you want to launch the created containers? [Y/n] " yn
case $yn in
    [Yy]* ) echo -e "\n"; ./launch.sh;;
esac

# Finished!
echo -e "\n😺 All done initialising!"
