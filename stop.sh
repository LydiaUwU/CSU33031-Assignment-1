# Script to stop running containers
# Author: Lydia MacBride

# Kill containers
echo "š Stopping the following containers"
sudo docker container ls -f name="a1-*"
sudo docker container stop $(sudo docker container ls -a -q -f name="a1-*") > /dev/null

# Finished!
echo -e "\nšŗ All done stopping!"