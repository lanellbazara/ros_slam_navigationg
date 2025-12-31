# ROS Robot Coursework - Test Workspace

## 1. Overview
This workspace contains the simulation, mapping, and navigation package for the BTR-80 robot.

## 2. Prerequisites
- ROS Noetic
- Gazebo
- Dependencies: `slam_karto`, `open_karto` (Included in `src/`)

## 3. Installation
1. Extract the workspace.
2. Install dependencies:
   ```bash
   cd test_ws
   rosdep install --from-paths src --ignore-src -r -y
   ```
3. Build the workspace:
   ```bash
   catkin_make
   source devel/setup.bash
   ```

## 4. Running the Project

### 4.1 Mapping (Karto SLAM)
```bash
# Terminal 1: Launch Simulation & SLAM
roslaunch model_test karto_mapping.launch

# Terminal 2: Keyboard Control
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

# Terminal 3: Save Map (when done)
rosrun map_server map_saver -f $(rospack find model_test)/maps/simple/map
```

### 4.2 Navigation (AMCL + MoveBase)
```bash
# Terminal 1: Launch Navigation
roslaunch model_test navigation.launch

# Terminal 2: Run Patrol Action
rosrun model_test navigation_client.py
```

### 4.3 System Monitor
```bash
./monitor_robot.sh
```
