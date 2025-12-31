# ROS Robot Coursework - Test Workspace

## 项目概述
该工作空间包含 BTR-80 机器人的 Gazebo 仿真、Karto SLAM 建图、AMCL+MoveBase 导航等功能包。

## 仓库结构
```
.
├── monitor_robot.sh            # 运行系统监控脚本
└── src
    ├── model_test              # 仿真、建图、导航的主要包
    │   ├── launch/             # karto_mapping.launch、navigation.launch 等启动文件
    │   ├── worlds/             # simple.world、autorace.world 场景
    │   ├── urdf/               # vehicle.urdf、sensors_robot.urdf 机器人模型
    │   ├── config/             # move_base、costmap、DWA 等参数
    │   ├── rviz/               # 各阶段的 RViz 配置
    │   └── src/navigation_client.py
    ├── open_karto              # 依赖的开源 karto 实现（源代码放在此处）
    └── slam_karto              # karto SLAM 相关依赖
```

## 环境依赖
- ROS Noetic（建议 Ubuntu 20.04）
- Gazebo（随 ROS 安装）
- teleop_twist_keyboard；未安装可通过 `sudo apt install ros-noetic-teleop-twist-keyboard` 安装
- rosdep 可用，用于自动安装依赖

## 安装与编译
假设工作空间目录名为 `test_ws`，即本仓库根目录：
1. 安装依赖
   ```bash
   cd test_ws
   rosdep install --from-paths src --ignore-src -r -y
   ```
2. 编译工作空间并加载环境
   ```bash
   catkin_make
   source devel/setup.bash
   ```

## 复现步骤（中文）

### 1. 建图（Karto SLAM）
1. 终端 A：启动仿真与 SLAM
   ```bash
   cd test_ws && source devel/setup.bash
   roslaunch model_test karto_mapping.launch
   ```
2. 终端 B：键盘控制机器人运动
   ```bash
   cd test_ws && source devel/setup.bash
   rosrun teleop_twist_keyboard teleop_twist_keyboard.py
   ```
3. 终端 C：完成探索后保存地图，会生成 map.pgm/map.yaml
   ```bash
   cd test_ws && source devel/setup.bash
   rosrun map_server map_saver -f $(rospack find model_test)/maps/simple/map
   ```
   生成的文件位于 `$(rospack find model_test)/maps/simple/`，包含 `map.pgm` 与 `map.yaml`。

### 2. 导航复现（AMCL + MoveBase）
1. 确保地图文件 `map.pgm` 与 `map.yaml` 已放在 `$(rospack find model_test)/maps/simple/`，可用以下命令验证：
   ```bash
   ls $(rospack find model_test)/maps/simple/map.*
   ```
   如需使用其他地图，可通过参数 `map_file:=<路径>` 指定。
2. 终端 A：启动导航，默认加载 simple.world 和保存的地图
   ```bash
   cd test_ws && source devel/setup.bash
   roslaunch model_test navigation.launch map_file:=$(rospack find model_test)/maps/simple/map.yaml
   ```
3. 终端 B：运行示例导航客户端，发送预设巡逻点
   ```bash
   cd test_ws && source devel/setup.bash
   rosrun model_test navigation_client.py
   ```

### 3. 系统监控
```bash
cd test_ws
./monitor_robot.sh
```
