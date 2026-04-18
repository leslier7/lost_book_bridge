#!/bin/bash

docker run -it \
  -v ~/ros2_ws:/root/ros2_ws \
  my_ros2 \
  bash -c "cd /root/ros2_ws && exec bash"
