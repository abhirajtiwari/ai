#!/bin/bash
option=0
while [ $option != 7 ]
do
printf "\n[0] Install ROS \n[1] Clone repo \n[2] Install robot-localisation \n[3] Install rtabmap \n[4] Install realsense \n[5] Install mapviz \n[6] Install python deps \n[7] Quit\n"
read option

if [ $option == 0 ]
then
	sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
	sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
	sudo apt update

	printf "\nInstall [f]ull or [b]ase: "
	read option
	if [ $option == "f" ]
	then
		sudo apt install ros-melodic-desktop-full -y
	elif [ option == "b" ]
	then
		sudo apt install ros-melodic-ros-base -y
	fi
	echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
	mkdir ~/catkin_ws/src
	cd ~/catkin_ws/src
	catkin_init_workspace
	cd ..
	catkin_make
	echo "source $HOME/catkin_ws/devel/setup.bash" >> ~/.bashrc
	source ~/.bashrc

elif [ $option == 1 ]
then
	echo "Enter github url to clone NOTE: use userame and password if repo is private!!"
	read git_url
	git clone $git_url $HOME

elif [ $option == 2 ]
then
	sudo apt install ros-$ROS_DISTRO-robot-localization ros-$ROS_DISTRO-nmea-navsat-driver ros-$ROS_DISTRO-imu-filter-madgwick -y

elif [ $option == 3 ]
then
	sudo apt install ros-$ROS_DISTRO-rtabmap ros-$ROS_DISTRO-rtabmap-ros -y
elif [ $option == 4 ]
then
	git clone https://github.com/IntelRealSense/librealsense.git $HOME
	sudo apt-key adv --keyserver keys.gnupg.net --recv-key C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C8B3A55A6F3EFCDE
	sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u
	sudo apt update
	sudo apt-get install librealsense2-dkms librealsense2-utils librealsense2-dev librealsense2-dbg -y
	
	echo "Enter path for ros workspace src: "
	read workspace_src
	git clone https://github.com/IntelRealSense/realsense-ros.git $workspace_src
	cd $workspace_src/realsense-ros
	pwd
	git checkout `git tag | sort -V | grep -P "^\d+\.\d+\.\d+" | tail -1`
	cd ..
	pwd
	catkin_init_workspace
	cd ..
	pwd
	catkin_make clean
	catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
	catkin_make install
	source ~/.bashrc
elif [ $option == 5 ]
then
	sudo apt install ros-$ROS_DISTRO-mapviz ros-$ROS_DISTRO-mapviz-plugins ros-$ROS_DISTRO-tile-map ros-$ROS_DISTRO-multires-image -y
	git clone https://github.com/danielsnider/MapViz-Tile-Map-Google-Maps-Satellite.git $HOME
	cd $HOME
	sudo apt install docker.io -y	
	sudo docker run -p 8080:8080 -d -t -v ~/mapproxy:/mapproxy danielsnider/mapproxy
	printf "\n\nEnter this in the custom wmts field\nhttp://localhost:8080/wmts/gm_layer/gm_grid/{level}/{x}/{y}.png\n"
elif [ $option == 6 ]
then
	sudo apt install python-pip python3-pip -y
	pip install sockets pygame pyproj pyserial pyqt5
	pip3 install sockets pygame pyproj pyserial pyqt5
	
fi

done
