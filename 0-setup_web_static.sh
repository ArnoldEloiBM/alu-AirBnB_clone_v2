#!/usr/bin/env bash
# This script sets up a web servers for the deployment of web_static hbnb

# installing nginx
dpkg -l | grep nginx > /dev/null
if [ $? -eq 1 ]; then
    sudo apt update
    sudo apt install nginx -y
fi

# creat data directory
if [ ! -d "/data/" ]; then
    sudo mkdir /data/
fi

# create web_static directory
if [ ! -d "/data/web_static/" ]; then
    sudo mkdir -p /data/web_static/
fi

# create releases and test directory
if [ ! -d "/data/web_static/releases/test/" ]; then
    sudo mkdir -p /data/web_static/releases/test/
fi

# create shared directory
if [ ! -d "/data/web_static/shared/" ]; then
    sudo mkdir -p /data/web_static/shared/
fi

# create index.html in test directory
if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    sudo touch /data/web_static/releases/test/index.html
fi

# add some content to the index.html
if [ -f "/data/web_static/releases/test/index.html" ]; then
    echo "Welcome to our today's web static" | sudo tee /data/web_static/releases/test/index.html > /dev/null
fi

# creating a symlink
if [ -e "/data/web_static/current" ]; then
    sudo rm /data/web_static/current
    sudo ln -s /data/web_static/releases/test/ /data/web_static/current
else
    sudo ln -s /data/web_static/releases/test/ /data/web_static/current
fi

# change file/ directory ownership
sudo chown -R ubuntu:ubuntu /data/

# update nginx to serve the content of /data/
sudo sed -i "/server_name/a\        location /hbnb_static {\n                alias /data/web_static/current/;\n        }" /etc/nginx/sites-available/default

#updating nginx
sudo service nginx restart
