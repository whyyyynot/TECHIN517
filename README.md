cd ~/ros2_ws
source /opt/ros/humble/setup.bash        # distro layer
colcon build --packages-select custom_msgs
source install/setup.bash  
