FROM osrf/ros:humble-desktop-jammy

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyzmq

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
