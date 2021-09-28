# Script to launch containers
# Author: Lydia MacBride

echo "🙂 Launching containers"

# Kill containers
echo -e "\n✨ Launching the following containers"
sudo docker container ls -a -f name="a1-*"
sudo docker container start $(sudo docker container ls -a -q -f name="a1-*") > /dev/null # TODO: Fix this

# Finished!
echo -e "\n😺 All done launching!"