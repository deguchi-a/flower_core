cmake_minimum_required(VERSION 3.5)  # Update this line to require at least version 3.5
project(flower_core)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs
  roslib  # Keep this line to find roslib
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(flower_core src/flower_core.cpp)
target_link_libraries(flower_core ${catkin_LIBRARIES})
