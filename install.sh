#!/bin/bash -p
chmod +x browsermob-proxy-2.1.4/bin/browsermob-proxy

echo  "deb http://deb.debian.org/debian unstable main non-free contrib" | sudo tee /etc/apt/sources.list.d/java.list
sudo apt update
sudo apt install python3-pip openjdk-11-jdk -y
sudo update-java-alternatives -s java-1.11.0-openjdk-amd64
python3 -m pip install  -r requirements.txt
