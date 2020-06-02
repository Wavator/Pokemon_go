
## System Requirements
1. **Install ROS and gazebo in the system**
	I have used Ubuntu 18.04, ROS-melodic and Gazebo 9. Refer to http://wiki.ros.org/ROS/Installation for instructions.

## To run on simulation:

**Worlds:**
The description of the world is given in `pokemon.world` file.

**Models:**
The models for the world file is given in the `models` folder. Place the models in the `~/.gazebo/models` folder.

Terminal 1: (turn on Gazebo)

```powershell
$ roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=/home/<user_name>/catkin_ws/src/pokemon_maze/worlds/pokemon.world
```

Terminal 2: Virtual SLAM

```
$roslaunch turtlebot_gazebo gmapping_demo.launch
```

Terminal 3: rviz visualization

```
$roslaunch turtlebot_rviz_launchers view_navigation.launch
```

Terminal 4: Control TurtleBot

```
$roslaunch turtlebot_teleop keyboard_teleop.launch
```

Terminal 5: Save the Map

```
$rosrun map_server map_saver -f ~/map
```

## To run on real robot:

Terminal 1: 

```powershell
$ roslaunch turtlebot_bringup minimal.launch
```

Terminal 2: SLAM

```
$roslaunch turtlebot_navigation gmapping_demo.launch
```

Terminal 3: rviz visualization

```
$roslaunch turtlebot_rviz_launchers view_navigation.launch
```

Terminal 4: Control TurtleBot

```
$roslaunch turtlebot_teleop keyboard_teleop.launch
```

Terminal 5: Save the Map

```
$rosrun map_server map_saver -f ~/map
```

--------------------------------------------------------
