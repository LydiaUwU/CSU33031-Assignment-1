# Script to remove docker configuration created by ./initialise.sh
# Author: Lydia MacBride

echo "🔥 Beginning removal"

# List current configuration
echo -e "\n🐳 Current docker containers"
sudo docker container ls -a
echo -e "\n📸 Current docker images"
sudo docker image ls
echo -e "\n🌐 Current docker networks"
sudo docker network ls

# Kill containers
echo -e "\n💀 Killing containers"
sudo docker container kill $(sudo docker container ls -a -q -f name="a1-*") > /dev/null

# List containers to be removed
echo -e "\n🗑 Removing the following containers:"
sudo docker container ls -a -f name="a1-*"
sudo docker container rm $(sudo docker container ls -a -q -f name="a1-*") > /dev/null

# List images to be removed
echo -e "\n🗑 Removing the following images:"
sudo docker image ls -a -f label=name="a1"
sudo docker image rm $(sudo docker image ls -q -f label=name="a1") > /dev/null

# List network to be removed
echo -e "\n🗑 Removing the following network:"
sudo docker network ls -f name="a1-*"
sudo docker network rm $(sudo docker network ls -q -f name="a1-*") > /dev/null

# List updated containers, images and network
echo -e "\n🐳 Updated docker containers"
sudo docker container ls -a
echo -e "\n📸 Updated docker images"
sudo docker image ls
echo -e "\n🌐 Updated docker networks"
sudo docker network ls

# Finished!
echo -e "\n😺 All done removing!"
