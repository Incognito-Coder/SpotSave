#!/usr/bin/env bash

has_command() {
  command -v "$1" &> /dev/null
}

#Checking for package manager
manager(){
if has_command apt; then
	sudo apt udpate && sudo apt install -y python3 pip3 ffmpeg
elif has_command dnf; then
	sudo dnf install -y python3 pip3 ffmpeg
elif has_command yum; then
	sudo yum install -y python3 pip3 ffmpeg
elif has_command zypper; then
	sudo zypper in -y python3 pip3 ffmpeg
elif has_command pacman; then
	sudo pacman -Syyu --noconfirm python3 pip3 ffmpeg
else
	echo "Could not find your package manager."
	exit 1
fi
}

if ! has_command python3 || ! has_command pip3 || ! has_command ffmpeg
then
	echo "Project requirements are seem missing..." ; sleep 1
	echo "Installing 'python3', 'pip3' and 'ffmpeg'..." ; sleep 1
	manager ; sleep 2
fi
pip3 install -r requirements.txt
sleep 2; echo "Everything is ready to use!"
