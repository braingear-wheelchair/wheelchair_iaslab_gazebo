cmake_minimum_required(VERSION 3.0.2)
project(wheelchair_iaslab_gazebo)

find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()

roslaunch_add_file_check(launch)

install(
  DIRECTORY launch meshes worlds 
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
