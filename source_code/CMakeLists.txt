cmake_minimum_required(VERSION 2.8.3)
project(pokemon_go)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  rospy
  roscpp
  sensor_msgs
  geometry_msgs
  actionlib
  move_base_msgs
  nav_msgs
)
find_package(OpenCV REQUIRED)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES pokemon_go
#  CATKIN_DEPENDS cv_bridge image_transport opencv2 ros roscpp sensor_msgs
#  DEPENDS system_lib
)



## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
  # ${OpenCV_INCLUDE_DIRS}
)
# set(OpenCV_DIR /usr/include/opencv2)

add_executable(pokemon_searching src/pokemon_searching.cpp)
target_link_libraries(pokemon_searching ${catkin_LIBRARIES} ${OpenCV_LIBS})

add_executable(pokemon_searching0 src/pokemon_searching0.cpp)
target_link_libraries(pokemon_searching0 ${catkin_LIBRARIES} ${OpenCV_LIBS})

add_executable(pokemon_searching1 src/pokemon_searching1.cpp)
target_link_libraries(pokemon_searching1 ${catkin_LIBRARIES} ${OpenCV_LIBS})

add_executable(pokemon_searching2 src/pokemon_searching2.cpp)
target_link_libraries(pokemon_searching2 ${catkin_LIBRARIES} ${OpenCV_LIBS})

add_executable(pokemon_catching0 src/pokemon_catching0.cpp)
target_link_libraries(pokemon_catching0 ${catkin_LIBRARIES} ${OpenCV_LIBS})

add_executable(pokemon_catching1 src/pokemon_catching1.cpp)
target_link_libraries(pokemon_catching1 ${catkin_LIBRARIES} ${OpenCV_LIBS})

add_executable(pokemon_catching2 src/pokemon_catching2.cpp)
target_link_libraries(pokemon_catching2 ${catkin_LIBRARIES} ${OpenCV_LIBS})

catkin_install_python(PROGRAMS scripts/exploring_pokemon.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

