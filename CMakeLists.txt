cmake_minimum_required(VERSION 2.8.3)
project(rovi_qc)

EXECUTE_PROCESS(COMMAND arch COMMAND tr -d '\n' OUTPUT_VARIABLE ARCH)
message(STATUS "Architecture: ${ARCH}")

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs
  sensor_msgs
  stereo_msgs
  cv_bridge
  message_generation
  image_geometry
)
find_package(OpenCV REQUIRED)

#add_message_files(
#  FILES
#  Floats.msg
#)

#generate_messages(
#  DEPENDENCIES
#  std_msgs
#  geometry_msgs
#  sensor_msgs
#  stereo_msgs
#)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES lib
  CATKIN_DEPENDS roscpp rovi std_msgs geometry_msgs sensor_msgs stereo_msgs cv_bridge image_geometry
  DEPENDS OpenCV
)

###########
## Build ##
###########

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_definitions("-std=c++11")

#add_executable(floats2pc src/floats2pc.cpp)
#target_link_libraries(floats2pc ${catkin_LIBRARIES})
#add_dependencies(floats2pc rovi_utils_gencpp)
