#!/bin/bash

if docker ps -q -f name=my_ros2_container | grep -q .; then
  docker exec -it -w /root/ros2_ws my_ros2_container bash
else
  docker rm -f my_ros2_container 2>/dev/null
  docker run -it \
    --name my_ros2_container \
    --network=host \
    -v ~/ros2_ws:/root/ros2_ws \
    my_ros2 \
    bash -c "cd /root/ros2_ws && exec bash"
fi
