# Script to remove docker configuration created by ./initialise.sh
# Author: Lydia MacBride

echo "š„ Beginning removal"

# List current configuration
echo -e "\nš³ Current docker containers"
sudo docker container ls -a
echo -e "\nšø Current docker images"
sudo docker image ls
echo -e "\nš Current docker networks"
sudo docker network ls

# Kill containers
echo -e "\nš Killing containers"
sudo docker container kill $(sudo docker container ls -a -q -f name="a1-*") > /dev/null

# TODO: Client not being removed properly
# List containers to be removed
echo -e "\nš Removing the following containers:"
sudo docker container ls -a -f name="a1-*"
sudo docker container rm $(sudo docker container ls -a -q -f name="a1-*") > /dev/null

# TODO: Client not being removed properly
# List images to be removed
echo -e "\nš Removing the following images:"
sudo docker image ls -f label=name="a1"
sudo docker image rm $(sudo docker image ls -q -f label=name="a1") > /dev/null

# List network to be removed
echo -e "\nš Following networks to be removed:";
sudo docker network ls -f name="a1-*";
read -p "ā Would you like to remove the above network: [Y/n] " yn
case $yn in
    [Yy]* ) echo -e "\nš Removing network:";
            sudo docker network rm $(sudo docker network ls -q -f name="a1-*") > /dev/null;;
esac

# List updated containers, images and network
echo -e "\nš³ Updated docker containers"
sudo docker container ls -a
echo -e "\nšø Updated docker images"
sudo docker image ls
echo -e "\nš Updated docker networks"
sudo docker network ls

# Finished!
echo -e "\nšŗ All done removing!"
