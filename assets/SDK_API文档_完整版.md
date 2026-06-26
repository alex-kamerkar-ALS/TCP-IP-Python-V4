# Dobot TCP-IP Python SDK API 文档（完整版）

## 目录

1. [概述](#概述)
2. [快速开始](#快速开始)
3. [DobotRobot 主控制类](#dobotrobot-主控制类)
4. [Motion 运动模块](#motion-运动模块)
5. [IO 数字IO模块](#io-数字io模块)
6. [RobotControl 机器人控制模块](#robotcontrol-机器人控制模块)
7. [Communication 通讯模块](#communication-通讯模块)
8. [Plugins 插件模块](#plugins-插件模块)
9. [状态反馈系统](#状态反馈系统)
10. [错误码处理](#错误码处理)
11. [完整示例](#完整示例)
12. [附录](#附录)

***

## 概述

### 关于本SDK

Dobot TCP-IP Python SDK 是越疆机器人官方提供的二次开发接口，基于TCP/IP协议实现与机器人的通信和控制。

### 支持的机器人型号

- CR3/CR5/CR10 系列协作机器人

### 协议版本

- 支持 Dobot TCP/IP 协议 V4.6.6

### 架构设计

```
DobotRobot (主类)
├── motion      - 运动控制模块
├── io          - 数字IO模块
├── robot_control - 机器人控制模块
├── communication - 通讯模块
└── plugins     - 插件模块
```

***

## 快速开始

### 环境要求

- Python 3.7+
- 机器人固件版本支持 TCP/IP 协议 V4.6.6

### 安装方式

```bash
# 源码安装
cd dobot_sdk
pip install -e .
```

### 基础示例

```python
from dobot_sdk import DobotRobot, CoordinateType

# 连接机器人
with DobotRobot("192.168.1.100") as robot:
    # 请求控制
    robot.robot_control.request_control()
    
    # 清除报警
    robot.robot_control.clear_error()
    
    # 使能机器人
    robot.robot_control.enable_robot()
    
    # 关节运动到初始位置
    robot.motion.movj([0, 0, 90, 0, 90, 0], CoordinateType.JOINT)
    
    # 笛卡尔运动
    robot.motion.movl([400, 0, 300, 180, 0, 0], CoordinateType.CARTESIAN)
    
    # 关闭DO1
    robot.io.do(1, 0)
    
    # 获取当前位姿
    pose = robot.robot_control.get_pose()
    print(f"当前位姿: {pose}")
```

***

## DobotRobot 主控制类

### 初始化

```python
DobotRobot(ip: str, dashboard_port: int = 29999, feedback_port: int = 30004)
```

**参数说明**:

| 参数              | 类型  | 默认值   | 说明                |
| --------------- | --- | ----- | ----------------- |
| ip              | str | -     | 机器人IP地址           |
| dashboard\_port | int | 29999 | Dashboard端口（命令控制） |
| feedback\_port  | int | 30004 | Feedback端口（状态反馈）  |

**示例**:

```python
# 使用默认端口
robot = DobotRobot("192.168.1.100")

# 自定义端口
robot = DobotRobot("192.168.1.100", dashboard_port=29999, feedback_port=30004)
```

### 连接管理

#### connect()

建立与机器人的连接。

```python
robot.connect(timeout: float = 5.0) -> None
```

**参数**:

| 参数      | 类型    | 默认值 | 说明        |
| ------- | ----- | --- | --------- |
| timeout | float | 5.0 | 连接超时时间（秒） |

**示例**:

```python
robot.connect()
```

#### disconnect()

断开与机器人的连接。

```python
robot.disconnect() -> None
```

**示例**:

```python
robot.disconnect()
```

### 模块接口说明

> **注意**: 为保持接口清晰，DobotRobot主类不再提供快捷控制方法，请通过对应模块调用：
> - 机器人控制: `robot.robot_control.enable_robot()` / `robot.robot_control.disable_robot()` / `robot.robot_control.clear_error()`
> - 运动控制: `robot.motion.movj()` / `robot.motion.movl()` / `robot.motion.arc()`
> - IO控制: `robot.io.do()` / `robot.io.di()` / `robot.io.ao()`
> - 通讯控制: `robot.communication.modbus_create()`
> - 插件控制: `robot.plugins.()`

详细接口请参考各模块章节。

### 状态监控

#### start\_feedback\_monitor()

启动状态反馈监控线程。

```python
robot.start_feedback_monitor(callback: Callable = None) -> None
```

**参数**:

| 参数       | 类型       | 说明                         |
| -------- | -------- | -------------------------- |
| callback | Callable | 状态更新回调函数，接收 RobotStatus 参数 |

**示例**:

```python
def on_status_update(status):
    print(f"当前位置: X={status.tool_vector_actual.x}")

robot.start_feedback_monitor(callback=on_status_update)
```

#### stop\_feedback\_monitor()

停止状态反馈监控。

```python
robot.stop_feedback_monitor() -> None
```

**示例**:

```python
robot.stop_feedback_monitor()
```

#### get\_status()

获取当前状态。

```python
robot.get_status() -> Optional[RobotStatus]
```

**返回值**: RobotStatus 对象

**示例**:

```python
status = robot.get_status()
if status:
    print(f"速度比例: {status.speed_scaling}%")
    print(f"机器人模式: {status.robot_mode.value}")
```

### 上下文管理器支持

```python
with DobotRobot("192.168.1.100") as robot:
    robot.robot_control.request_control()
    robot.robot_control.clear_error()
    robot.robot_control.enable_robot()
    # 执行操作
# 自动断开连接
```

***

## Motion 运动模块

通过 `robot.motion` 访问。

### 坐标系类型

```python
from dobot_sdk import CoordinateType

CoordinateType.CARTESIAN  # 笛卡尔坐标 (x, y, z, rx, ry, rz)
CoordinateType.JOINT      # 关节角度 (j1, j2, j3, j4, j5, j6)
```

### 基础运动指令

#### movj() - 关节运动

```python
motion.movj(pose, coord_type, user=-1, tool=-1, a=-1, v=-1, cp=-1) -> str
```

**参数**:

| 参数          | 类型             | 默认值 | 说明            |
| ----------- | -------------- | --- | ------------- |
| pose        | list\[float]   | -   | 6个坐标值         |
| coord\_type | CoordinateType | -   | 坐标系类型         |
| user        | int            | -1  | 用户坐标系编号（0-50） |
| tool        | int            | -1  | 工具坐标系编号（0-50） |
| a           | int            | -1  | 加速度比例（1-100）  |
| v           | int            | -1  | 速度比例（1-100）   |
| cp          | int            | -1  | 平滑过渡比例（0-100） |

**示例**:

```python
# 关节运动
robot.motion.movj([0, 0, 90, 0, 90, 0], CoordinateType.JOINT)

# 笛卡尔运动，带参数
robot.motion.movj([400, 0, 300, 180, 0, 0], CoordinateType.CARTESIAN, v=50)
```

#### movl() - 直线运动

```python
motion.movl(pose, coord_type, user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1) -> str
```

**参数**:

| 参数    | 类型  | 默认值 | 说明               |
| ----- | --- | --- | ---------------- |
| speed | int | -1  | 目标速度（mm/s），与v互斥  |
| r     | int | -1  | 平滑过渡半径（mm），与cp互斥 |

**示例**:

```python
robot.motion.movl([500, 100, 200, 180, 0, 0], CoordinateType.CARTESIAN, speed=100)
```

#### movj\_io() - 关节运动并输出DO

```python
motion.movj_io(pose, do_index, do_status, coord_type, user=-1, tool=-1, a=-1, v=-1, cp=-1) -> str
```

**示例**:

```python
# 运动到目标点，同时打开DO1
robot.motion.movj_io([400, 0, 300, 180, 0, 0], 1, 1, CoordinateType.CARTESIAN)
```

#### movl\_io() - 直线运动并输出DO

```python
motion.movl_io(pose, do_index, do_status, coord_type, user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1) -> str
```

**示例**:

```python
robot.motion.movl_io([500, 0, 300, 180, 0, 0], 1, 0, CoordinateType.CARTESIAN)
```

#### arc() - 圆弧插补运动

```python
motion.arc(p1, p2, coord_type, user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1, mode=0) -> str
```

**参数**:

| 参数   | 类型           | 默认值 | 说明                       |
| ---- | ------------ | --- | ------------------------ |
| p1   | list\[float] | -   | 圆弧中间点位姿                  |
| p2   | list\[float] | -   | 目标点位姿                    |
| mode | int          | 0   | 姿态控制模式（0-线性，1-过中间点，2-固定） |

**示例**:

```python
mid_point = [400, 100, 300, 180, 0, 0]
end_point = [400, 200, 300, 180, 0, 0]
robot.motion.arc(mid_point, end_point, CoordinateType.CARTESIAN)
```

#### arc\_io() - 圆弧运动并输出DO

```python
motion.arc_io(p1, p2, do_index, do_status, coord_type, user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1, mode=0) -> str
```

**示例**:

```python
mid_point = [400, 100, 300, 180, 0, 0]
end_point = [400, 200, 300, 180, 0, 0]
# 圆弧运动到终点时打开DO1
robot.motion.arc_io(mid_point, end_point, 1, 1, CoordinateType.CARTESIAN)
```

#### circle() - 整圆插补运动

```python
motion.circle(p1, p2, count, coord_type, user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1, mode=0) -> str
```

**参数**:

| 参数    | 类型  | 说明        |
| ----- | --- | --------- |
| count | int | 圈数（1-999） |

**示例**:

```python
# 画2圈圆
robot.motion.circle(mid_point, end_point, 2, CoordinateType.CARTESIAN)
```

### 伺服运动

#### servo\_j() - 关节空间动态跟随

```python
motion.servo_j(joints, t=0.1, aheadtime=50.0, gain=500.0) -> str
```

**参数**:

| 参数        | 类型    | 默认值   | 说明                   |
| --------- | ----- | ----- | -------------------- |
| joints    | Sequence[float] | -     | 关节角度列表 [j1,j2,j3,j4,j5,j6]（度） |
| t         | float | 0.1   | 运行时间（秒，0.004-3600.0） |
| aheadtime | float | 50.0  | 提前量（20.0-100.0）      |
| gain      | float | 500.0 | 比例增益（200.0-1000.0）   |

**示例**:

```python
import time

# 实时跟随示例
for i in range(100):
    j1 = i * 0.5
    robot.motion.servo_j([j1, 0, 90, 0, 90, 0], t=0.05)
    time.sleep(0.05)
```

#### servo\_p() - 笛卡尔空间动态跟随

```python
motion.servo_p(pose, t=0.1, aheadtime=50.0, gain=500.0) -> str
```

**示例**:

```python
robot.motion.servo_p([400 + i*2, 0, 300, 180, 0, 0], t=0.05)
```

### 点动控制

#### move\_jog() - 点动机械臂

```python
motion.move_jog(axis="", coord_type=CoordinateType.JOINT, user=0, tool=0) -> str
```

**参数**:

| 参数   | 类型  | 默认值 | 说明                                                        |
| ---- | --- | --- | --------------------------------------------------------- |
| axis | str | ""  | "X+", "X-", "Y+", "Y-", "Z+", "Z-", "J1+", "J1-" 等，空字符串停止 |

**示例**:

```python
# 启动点动
robot.motion.move_jog("X+", CoordinateType.CARTESIAN)

# 停止点动
robot.motion.move_jog()
```

### 相对运动

#### rel\_movj\_tool() - 工具坐标系相对关节运动

```python
motion.rel_movj_tool(offset, v=-1) -> str
```

**示例**:

```python
# 沿工具坐标系移动
robot.motion.rel_movj_tool([0, 0, 0, 0, 0, 30], v=50)
```

#### rel\_movl\_tool() - 工具坐标系相对直线运动

```python
motion.rel_movl_tool(offset, v=-1, r=-1) -> str
```

**示例**:

```python
# 沿X方向移动50mm
robot.motion.rel_movl_tool([50, 0, 0, 0, 0, 0], v=50)
```

#### rel\_movj\_user() - 用户坐标系相对关节运动

```python
motion.rel_movj_user(offset, v=-1) -> str
```

**示例**:

```python
# 在用户坐标系中相对移动
robot.motion.rel_movj_user([0, 50, 0, 0, 0, 0], v=50)
```

#### rel\_movl\_user() - 用户坐标系相对直线运动

```python
motion.rel_movl_user(offset, v=-1, r=-1) -> str
```

**示例**:

```python
# 在用户坐标系中相对直线移动
robot.motion.rel_movl_user([50, 0, 0, 0, 0, 0], v=50)
```

#### rel\_joint\_movj() - 关节坐标系相对运动

```python
motion.rel_joint_movj(offset, v=-1) -> str
```

**示例**:

```python
# J1轴相对旋转30度
robot.motion.rel_joint_movj([30, 0, 0, 0, 0, 0], v=30)
```

### 轨迹复现

#### movs() - 拟合导入轨迹

```python
motion.movs(trace_name, is_const=0, multi=1.0, sample=50, freq=0.2, user=-1, tool=-1) -> str
```

**参数**:

| 参数          | 类型    | 默认值 | 说明              |
| ----------- | ----- | --- | --------------- |
| trace\_name | str   | -   | 轨迹文件名（含后缀）      |
| is\_const   | int   | 0   | 是否匀速（0-原速，1-匀速） |
| multi       | float | 1.0 | 速度倍数（0.25-2）    |
| sample      | int   | 50  | 采样间隔（ms，8-1000） |
| freq        | float | 0.2 | 滤波系数（0-1）       |

**示例**:

```python
robot.motion.movs("trajectory.csv", is_const=1, multi=0.5)
```

#### start\_path() - 复现录制轨迹

```python
motion.start_path(trace_name, is_const=0, multi=1.0, sample=50, freq=0.2, user=-1, tool=-1) -> str
```

**示例**:

```python
robot.motion.start_path("recorded_trace.csv", is_const=1, multi=0.8)
```

#### get\_start\_pose() - 获取轨迹起点

```python
motion.get_start_pose(trace_name, path_type=1) -> str
```

**参数**:

| 参数         | 类型  | 默认值 | 说明                  |
| ---------- | --- | --- | ------------------- |
| path\_type | int | 1   | 轨迹类型（1-复现轨迹，2-拟合轨迹） |

**示例**:

```python
# 获取拟合轨迹的起点
response = robot.motion.get_start_pose("trajectory.csv", path_type=2)
print(f"轨迹起点: {response}")
```

### 坐标系偏移

#### start\_rt\_offset() - 启动坐标系偏移

```python
motion.start_rt_offset(offset) -> str

**示例**:

```python
# 启动偏移
robot.motion.start_rt_offset([10, 10, 0, 0, 0, 0])

# 执行运动（带偏移）
robot.motion.movl([400, 0, 300, 180, 0, 0], CoordinateType.CARTESIAN)

# 结束偏移
robot.motion.end_rt_offset()
```

#### end\_rt\_offset() - 结束坐标系偏移

```python
motion.end_rt_offset() -> str
```

#### offset\_para() - 设置偏移参数

```python
motion.offset_para(freq=0.2) -> str
```

**示例**:

```python
# 设置偏移滤波系数
robot.motion.offset_para(freq=0.5)
```

### 轨迹恢复

#### set\_resume\_offset() - 设置恢复回退距离

```python
motion.set_resume_offset(distance) -> str
```

**示例**:

```python
robot.motion.set_resume_offset(50)  # 回退50mm
```

#### path\_recovery() - 开始轨迹恢复

```python
motion.path_recovery() -> str
```

**示例**:

```python
# 设置回退距离后开始恢复
robot.motion.set_resume_offset(50)
robot.motion.path_recovery()
```

#### path\_recovery\_stop() - 停止轨迹恢复

```python
motion.path_recovery_stop() -> str
```

**示例**:

```python
robot.motion.path_recovery_stop()
```

#### path\_recovery\_status() - 查询恢复状态

```python
motion.path_recovery_status() -> str
```

**返回值**:

- 0: 已回到暂停位姿
- 1: 偏差较小
- 2: 偏差较大

**示例**:

```python
status = robot.motion.path_recovery_status()
print(f"恢复状态: {status}")
```

### 速度加速度设置

#### speed\_factor() - 设置全局速度比例

```python
motion.speed_factor(speed) -> str
```

**参数**:

| 参数    | 类型  | 说明          |
| ----- | --- | ----------- |
| speed | int | 速度比例（0-100） |

**示例**:

```python
robot.motion.speed_factor(50)  # 设置50%速度
```

#### j\_speed\_factor() - 设置关节速度比例

```python
motion.j_speed_factor(joint, speed) -> str
```

**示例**:

```python
# 设置J1轴速度比例为50%
robot.motion.j_speed_factor(1, 50)
```

#### l\_speed\_factor() - 设置直线速度比例

```python
motion.l_speed_factor(speed) -> str
```

**示例**:

```python
# 设置直线运动速度比例为70%
robot.motion.l_speed_factor(70)
```

#### acc\_j() - 设置关节加速度比例

```python
motion.acc_j(joint, acc) -> str
```

**示例**:

```python
# 设置J1轴加速度比例为30%
robot.motion.acc_j(1, 30)
```

#### acc\_l() - 设置直线加速度比例

```python
motion.acc_l(acc) -> str
```

**示例**:

```python
# 设置直线运动加速度比例为40%
robot.motion.acc_l(40)
```

### 坐标系设置

#### set\_user() - 设置用户坐标系

```python
robot_control.set_user(index, pose) -> str

**参数**:

| 参数    | 类型  | 说明           |
| ----- | --- | ------------ |
| index | int | 用户坐标系编号（0-50） |
| pose  | Sequence[float] | 6个坐标 [x,y,z,rx,ry,rz] |

**示例**:

```python
# 设置用户坐标系0
robot.robot_control.set_user(0, [100, 0, 0, 0, 0, 0])
```

#### set\_tool() - 设置工具坐标系

```python
robot_control.set_tool(index, pose) -> str

**示例**:

```python
# 设置工具坐标系0（末端工具偏移）
robot.robot_control.set_tool(0, [0, 0, 100, 0, 0, 0])
```

#### set\_work\_load() - 设置负载参数

```python
motion.set_work_load(index, weight, center) -> str

**示例**:

```python
robot.motion.set_work_load(0, 1.5, [0, 0, 50])
```

#### set\_payload() - 设置末端负载

```python
robot_control.set_payload(load, center=None) -> str

**示例**:

```python
# 方式一：直接设置参数
robot.robot_control.set_payload(1.5, [0, 0, 50])

# 方式二：只设置重量
robot.robot_control.set_payload(1.5)
```

### 运行模式设置

#### set\_run\_mode() - 设置运行模式

```python
motion.set_run_mode(mode) -> str
```

**参数**:

| 值 | 模式   |
| - | ---- |
| 0 | 拖动示教 |
| 1 | 正常运行 |
| 2 | 模拟运行 |
| 3 | 空载示教 |
| 4 | 力控拖动 |
| 5 | 协作示教 |
| 6 | 绝对拖动 |
| 7 | 相对拖动 |

**示例**:

```python
robot.motion.set_run_mode(1)  # 正常运行模式
```

#### drag\_teach\_switch() - 拖动示教开关

```python
motion.drag_teach_switch(status) -> str
```

**示例**:

```python
robot.motion.drag_teach_switch(1)  # 开启拖动示教
```

### 抱闸控制

#### brake\_control() - 抱闸控制

```python
motion.brake_control(axis, status) -> str
```

**参数**:

| 参数     | 类型  | 说明        |
| ------ | --- | --------- |
| axis   | int | 轴编号（1-6）  |
| status | int | 0-松开，1-抱紧 |

**示例**:

```python
robot.motion.brake_control(1, 0)  # 松开J1轴抱闸
```

### 末端控制

#### tool\_voltage() - 设置末端电压

```python
motion.tool_voltage(voltage) -> str
```

**参数**:

| 值 | 电压  |
| - | --- |
| 0 | 0V  |
| 1 | 5V  |
| 2 | 12V |
| 3 | 24V |

**示例**:

```python
robot.motion.tool_voltage(3)  # 设置24V
```

### 运动控制

#### init\_pose() - 回到初始位置

```python
motion.init_pose() -> str
```

**示例**:

```python
robot.motion.init_pose()
```

#### stop() - 停止运动

```python
motion.stop() -> str
```

**示例**:

```python
robot.motion.stop()
```

#### pause() - 暂停运动

```python
motion.pause() -> str
```

**示例**:

```python
robot.motion.pause()
```

#### continue\_motion() - 继续运动

```python
motion.continue_motion() -> str
```

**示例**:

```python
robot.motion.continue_motion()
```

#### emergency\_stop() - 紧急停止

```python
motion.emergency_stop() -> str
```

**示例**:

```python
robot.motion.emergency_stop()
```

***

## IO 数字IO模块

通过 `robot.io` 访问。

### 数字输出

#### do() - 设置数字输出（队列指令）

```python
io.do(index, status) -> str
```

**参数**:

| 参数     | 类型  | 说明           |
| ------ | --- | ------------ |
| index  | int | DO端口索引（1-64） |
| status | int | 0-Off，1-On   |

**示例**:

```python
robot.io.do(1, 1)  # 打开DO1
robot.io.do(1, 0)  # 关闭DO1
```

#### do\_instant() - 设置数字输出（立即指令）

```python
io.do_instant(index, status) -> str
```

**示例**:

```python
robot.io.do_instant(1, 1)
```

#### get\_do() - 获取数字输出状态

```python
io.get_do(index) -> str
```

**示例**:

```python
response = robot.io.get_do(1)
print(response)  # ErrorID,{status},GetDO(1);
```

#### do\_group() - 设置多个数字输出

```python
io.do_group(group_index, status) -> str
```

**参数**:

| 参数           | 类型       | 说明         |
| ------------ | -------- | ---------- |
| group\_index | int      | IO组索引（0-3） |
| status       | list/str | 端口状态列表或字符串 |

**示例**:

```python
# 设置第0组（DO1-DO4）
robot.io.do_group(0, [1, 0, 1, 0])
```

#### do\_group\_dec() - 十进制设置DO组

```python
io.do_group_dec(group_index, value) -> str
```

**示例**:

```python
robot.io.do_group_dec(0, 5)  # 二进制 0101
```

#### get\_do\_group() - 获取DO组状态

```python
io.get_do_group(group_index) -> str
```

**示例**:

```python
response = robot.io.get_do_group(0)
print(f"DO组状态: {response}")
```

### 数字输入

#### get\_di() - 获取数字输入状态

```python
io.get_di(index) -> str
```

**示例**:

```python
response = robot.io.get_di(1)
```

#### di\_group() - 等待数字输入组

```python
io.di_group(group_index, status) -> str
```

**示例**:

```python
robot.io.di_group(0, [1, 1, 0, 0])
```

#### get\_di\_group() - 获取DI组状态

```python
io.get_di_group(group_index) -> str
```

**示例**:

```python
response = robot.io.get_di_group(0)
print(f"DI组状态: {response}")
```

### 模拟IO

#### set\_ao() - 设置模拟输出

```python
io.set_ao(index, value) -> str
```

**参数**:

| 参数    | 类型    | 说明                  |
| ----- | ----- | ------------------- |
| index | int   | AO端口索引（1-2）         |
| value | float | 输出值（0-10V 对应 0-100） |

**示例**:

```python
robot.io.set_ao(1, 50)  # 输出5V
```

#### get\_ao() - 获取模拟输出

```python
io.get_ao(index) -> str
```

**示例**:

```python
response = robot.io.get_ao(1)
print(f"AO1输出值: {response}")
```

#### get\_ai() - 获取模拟输入

```python
io.get_ai(index) -> str
```

**示例**:

```python
response = robot.io.get_ai(1)
print(f"AI1输入值: {response}")
```

### 末端IO

#### set\_end\_do() - 设置末端数字输出

```python
io.set_end_do(index, status) -> str
```

**示例**:

```python
robot.io.set_end_do(1, 1)
```

#### get\_end\_di() - 获取末端数字输入

```python
io.get_end_di(index) -> str
```

**示例**:

```python
response = robot.io.get_end_di(1)
print(f"末端DI1状态: {response}")
```

#### get\_end\_ai() - 获取末端模拟输入

```python
io.get_end_ai(index) -> str
```

**示例**:

```python
response = robot.io.get_end_ai(1)
print(f"末端AI1输入值: {response}")
```

***

## RobotControl 机器人控制模块

通过 `robot.robot_control` 访问。

### 控制模式

#### request\_control() - 请求TCP控制模式

```python
robot_control.request_control() -> str
```

**示例**:

```python
robot.robot_control.request_control()
```

### 电源控制

#### power\_on() - 机器人上电

```python
robot_control.power_on() -> str
```

**示例**:

```python
robot.robot_control.power_on()
```

#### power\_off() - 机器人下电

```python
robot_control.power_off() -> str
```

**示例**:

```python
robot.robot_control.power_off()
```

### 状态查询

#### get\_error\_id() - 获取错误码

```python
robot_control.get_error_id() -> str
```

**返回值格式**: `ErrorID,{[error1,error2,...]},GetErrorID();`

**示例**:

```python
response = robot.robot_control.get_error_id()
print(response)  # 0,{[1537,2048]},GetErrorID();
```

#### get\_robot\_mode() - 获取机器人模式

```python
robot_control.get_robot_mode() -> str
```

**返回值**:

| 值 | 模式  |
| - | --- |
| 1 | 初始化 |
| 2 | 手动  |
| 3 | 自动  |
| 4 | 远程  |
| 9 | 错误  |

**示例**:

```python
mode = robot.robot_control.get_robot_mode()
print(f"机器人模式: {mode}")
```

#### get\_pose() - 获取当前位姿

```python
robot_control.get_pose(user=-1, tool=-1) -> str
```

**示例**:

```python
response = robot.robot_control.get_pose()
print(response)  # ErrorID,{x,y,z,rx,ry,rz},GetPose();
```

#### get\_joint\_angle() - 获取关节角度

```python
robot_control.get_joint_angle() -> str
```

**示例**:

```python
response = robot.robot_control.get_joint_angle()
print(response)  # ErrorID,{j1,j2,j3,j4,j5,j6},GetJointAngle();
```

#### get\_speed() - 获取当前速度

```python
robot_control.get_speed() -> str
```

**示例**:

```python
response = robot.robot_control.get_speed()
print(f"当前速度: {response}")
```

### 运动学计算

#### inverse\_kinematic() - 逆解计算

```python
robot_control.inverse_kinematic(pose, user=-1, tool=-1, use_joint_near=-1, joint_near=None) -> str
```

**示例**:

```python
pose = [400, 0, 300, 180, 0, 0]
response = robot.robot_control.inverse_kinematic(pose)
```

#### forward\_kinematic() - 正解计算

```python
robot_control.forward_kinematic(joints) -> str
```

**示例**:

```python
joints = [0, 0, 90, 0, 90, 0]
response = robot.robot_control.forward_kinematic(joints)
```

#### check\_pose() - 可达性检查

```python
robot_control.check_pose(pose, user=-1, tool=-1, is_joint=-1, joints=None) -> str
```

**返回值**:

- 0: 不可达
- 1: 可达

**示例**:

```python
pose = [400, 0, 300, 180, 0, 0]
response = robot.robot_control.check_pose(pose)
```

### 脚本控制

#### run\_script() - 运行脚本

```python
robot_control.run_script(script_name) -> str
```

**示例**:

```python
robot.robot_control.run_script("test.lua")
```

#### stop\_script() - 停止脚本

```python
robot_control.stop_script() -> str
```

**示例**:

```python
robot.robot_control.stop_script()
```

### 日志控制

#### set\_log\_level() - 设置日志级别

```python
robot_control.set_log_level(level) -> str
```

**参数**:

| 值 | 级别 |
| - | -- |
| 0 | 关闭 |
| 1 | 错误 |
| 2 | 警告 |
| 3 | 信息 |
| 4 | 调试 |

**示例**:

```python
robot.robot_control.set_log_level(3)  # 信息级别
```

#### get\_log() - 获取日志

```python
robot_control.get_log(count) -> str
```

**示例**:

```python
response = robot.robot_control.get_log(10)
```

***

## Communication 通讯模块

通过 `robot.communication` 访问。

### Modbus 主站

#### modbus\_create() - 创建Modbus主站

```python
communication.modbus_create(ip, port, slave_id, is_rtu=0) -> str
```

**参数**:

| 参数        | 类型  | 默认值 | 说明              |
| --------- | --- | --- | --------------- |
| ip        | str | -   | 从站IP地址          |
| port      | int | -   | 从站端口            |
| slave\_id | int | -   | 从站ID            |
| is\_rtu   | int | 0   | 0-TCP模式，1-RTU模式 |

**示例**:

```python
response = robot.communication.modbus_create("192.168.1.10", 502, 1)
```

#### modbus\_rtu\_create() - 创建RTU主站

```python
communication.modbus_rtu_create(slave_id, baud, parity="E", data_bit=8, stop_bit=1) -> str
```

**参数**:

| 参数     | 类型  | 默认值 | 说明                      |
| ------ | --- | --- | ----------------------- |
| parity | str | "E" | "O"-奇校验，"E"-偶校验，"N"-无校验 |

**示例**:

```python
robot.communication.modbus_rtu_create(1, 19200, "N", 8, 1)
```

#### modbus\_close() - 关闭Modbus连接

```python
communication.modbus_close(index) -> str
```

**示例**:

```python
robot.communication.modbus_close(0)
```

### 寄存器读写

#### get\_in\_bits() - 读取触点寄存器

```python
communication.get_in_bits(index, addr, count) -> str
```

**示例**:

```python
response = robot.communication.get_in_bits(0, 0, 8)
print(f"触点寄存器: {response}")
```

#### get\_coils() - 读取线圈寄存器

```python
communication.get_coils(index, addr, count) -> str
```

**示例**:

```python
response = robot.communication.get_coils(0, 0, 8)
print(f"线圈寄存器: {response}")
```

#### set\_coils() - 写入线圈寄存器

```python
communication.set_coils(index, addr, count, values) -> str
```

**示例**:

```python
robot.communication.set_coils(0, 0, 4, [1, 0, 1, 0])
```

#### get\_input\_registers() - 读取输入寄存器

```python
communication.get_input_registers(index, addr, count) -> str
```

**示例**:

```python
response = robot.communication.get_input_registers(0, 0, 4)
print(f"输入寄存器: {response}")
```

#### get\_holding\_registers() - 读取保持寄存器

```python
communication.get_holding_registers(index, addr, count) -> str
```

**示例**:

```python
response = robot.communication.get_holding_registers(0, 0, 4)
print(f"保持寄存器: {response}")
```

#### set\_holding\_registers() - 写入保持寄存器

```python
communication.set_holding_registers(index, addr, count, values) -> str
```

**示例**:

```python
robot.communication.set_holding_registers(0, 0, 2, [100, 200])
```

***

## Plugins 插件模块

通过 `robot.plugins` 访问。

### 力传感器

#### enable\_ft\_sensor() - 开启/关闭力传感器

```python
plugins.enable_ft_sensor(status) -> str
```

**示例**:

```python
robot.plugins.enable_ft_sensor(1)  # 开启
```

#### six\_force\_home() - 力传感器回零

```python
plugins.six_force_home() -> str
```

**示例**:

```python
robot.plugins.six_force_home()
```

#### get\_force() - 获取力传感器数值

```python
plugins.get_force(tool=-1) -> str
```

**返回值格式**: `ErrorID,{fx,fy,fz,frx,fry,frz},GetForce();`

**示例**:

```python
response = robot.plugins.get_force()
```

### 力控拖拽模式

#### force\_drive\_mode() - 进入力控拖拽模式

```python
plugins.force_drive_mode(status) -> str
```

**示例**:

```python
robot.plugins.force_drive_mode(1)  # 进入拖拽模式
```

#### force\_drive\_speed() - 设置拖拽速度

```python
plugins.force_drive_speed(speed) -> str
```

**参数**:

| 参数    | 类型  | 说明          |
| ----- | --- | ----------- |
| speed | int | 速度比例（0-100） |

**示例**:

```python
robot.plugins.force_drive_speed(50)
```

### 力控模式

#### fc\_force\_mode() - 开启力控模式

```python
plugins.fc_force_mode(pose, force, reference=-1, user=-1, tool=-1) -> str
```

**参数**:

| 参数        | 类型           | 说明                |
| --------- | ------------ | ----------------- |
| pose      | list\[float] | 6个方向的刚度系数         |
| force     | list\[float] | 6个方向的目标力          |
| reference | int          | 参考坐标系（-1-工具，1-用户） |

**示例**:

```python
pose = [1, 1, 0, 0, 0, 0]      # X,Y方向刚度
force = [10, 10, 0, 0, 0, 0]   # X,Y方向目标力
robot.plugins.fc_force_mode(pose, force)
```

#### fc\_force\_mode2() - 力控模式2

```python
plugins.fc_force_mode2(pose, force, reference=-1, user=-1, tool=-1) -> str
```

**示例**:

```python
pose = [1, 1, 1, 0, 0, 0]
force = [5, 5, 5, 0, 0, 0]
robot.plugins.fc_force_mode2(pose, force)
```

#### fc\_force\_mode3() - 力控模式3

```python
plugins.fc_force_mode3(pose, force, reference=-1, user=-1, tool=-1) -> str
```

**示例**:

```python
pose = [2, 2, 0, 0, 0, 0]
force = [0, 0, -10, 0, 0, 0]
robot.plugins.fc_force_mode3(pose, force)
```

#### fc\_force\_mode4() - 力控模式4

```python
plugins.fc_force_mode4(pose, force, reference=-1, user=-1, tool=-1) -> str
```

**示例**:

```python
pose = [1, 1, 1, 1, 1, 0]
force = [0, 0, -8, 0, 0, 0]
robot.plugins.fc_force_mode4(pose, force)
```

### 力控参数设置

#### fc\_set\_param() - 设置力控参数

```python
plugins.fc_set_param(index, value) -> str
```

**参数**:

| 参数    | 类型    | 说明   |
| ----- | ----- | ---- |
| index | int   | 参数索引 |
| value | float | 参数值  |

**示例**:

```python
robot.plugins.fc_set_param(0, 100)
```

#### fc\_get\_param() - 获取力控参数

```python
plugins.fc_get_param(index) -> str
```

**示例**:

```python
response = robot.plugins.fc_get_param(0)
print(f"力控参数0: {response}")
```

### 传送带跟踪

#### conveyor\_create() - 创建传送带跟踪

```python
plugins.conveyor_create(sensor_index, conveyor_index, direction=1) -> str
```

**示例**:

```python
robot.plugins.conveyor_create(0, 0, direction=1)
```

#### conveyor\_start() - 启动传送带跟踪

```python
plugins.conveyor_start(conveyor_index) -> str
```

**示例**:

```python
robot.plugins.conveyor_start(0)
```

#### conveyor\_stop() - 停止传送带跟踪

```python
plugins.conveyor_stop(conveyor_index) -> str
```

**示例**:

```python
robot.plugins.conveyor_stop(0)
```

#### conveyor\_set\_speed() - 设置传送带速度

```python
plugins.conveyor_set_speed(conveyor_index, speed) -> str
```

**示例**:

```python
robot.plugins.conveyor_set_speed(0, 50)
```

***

## 状态反馈系统

### RobotStatus 对象

**属性说明**:

| 属性                   | 类型            | 说明          |
| -------------------- | ------------- | ----------- |
| robot\_mode          | RobotMode     | 机器人模式       |
| speed\_scaling       | float         | 速度比例（0-100） |
| digital\_inputs      | int           | 数字输入状态（64位） |
| digital\_outputs     | int           | 数字输出状态（64位） |
| joint\_state         | JointState    | 关节状态        |
| tool\_vector\_actual | CartesianPose | 当前工具位姿      |
| tool\_vector\_target | CartesianPose | 目标工具位姿      |
| current\_tool        | int           | 当前工具坐标系     |
| current\_user        | int           | 当前用户坐标系     |

### JointState 对象

| 属性         | 类型           | 说明     |
| ---------- | ------------ | ------ |
| q\_actual  | list\[float] | 实际关节角度 |
| q\_target  | list\[float] | 目标关节角度 |
| qd\_actual | list\[float] | 实际关节速度 |
| i\_actual  | list\[float] | 实际关节电流 |

### CartesianPose 对象

| 属性 | 类型    | 说明      |
| -- | ----- | ------- |
| x  | float | X坐标（mm） |
| y  | float | Y坐标（mm） |
| z  | float | Z坐标（mm） |
| rx | float | Rx角度（度） |
| ry | float | Ry角度（度） |
| rz | float | Rz角度（度） |

**方法**:

```python
pose.to_list()  # 转换为列表 [x, y, z, rx, ry, rz]
```

### 使用示例

```python
# 获取状态
status = robot.get_status()

if status:
    # 机器人模式
    print(f"模式: {status.robot_mode.value}")
    
    # 速度比例
    print(f"速度: {status.speed_scaling}%")
    
    # 数字输入输出
    print(f"DI: {bin(status.digital_inputs)}")
    print(f"DO: {bin(status.digital_outputs)}")
    
    # 关节角度
    if status.joint_state:
        print(f"J1: {status.joint_state.q_actual[0]:.2f}")
    
    # 笛卡尔坐标
    if status.tool_vector_actual:
        pose = status.tool_vector_actual.to_list()
        print(f"位置: {pose}")
```

***

## 错误码处理

### 错误码解析

```python
from dobot_sdk.api.error_code import parse_error_ids, format_error_messages

# 解析错误码响应
response = "0,{[1537,2048,2049]},GetErrorID();"
error_ids = parse_error_ids(response)
print(error_ids)  # [1537, 2048, 2049]

# 格式化错误信息
message = format_error_messages(error_ids, lang="zh_CN")
print(message)
```

### 支持的语言

- `zh_CN` - 简体中文
- `en` - English
- `ja` - 日本語

### 错误信息格式

```
错误码: 1537
描述: 急停触发
原因: 急停按钮被按下
解决方案: 检查急停按钮并复位

错误码: 2048
描述: J1轴伺服报警
原因: J1轴伺服驱动器报警
解决方案: 检查J1轴伺服电机
```

### 常用错误码

| 错误码  | 描述      | 原因         |
| ---- | ------- | ---------- |
| 0    | 无错误     | -          |
| 1537 | 急停触发    | 急停按钮被按下    |
| 2048 | J1轴伺服报警 | J1轴伺服驱动器报警 |
| 2049 | J2轴伺服报警 | J2轴伺服驱动器报警 |
| 2050 | J3轴伺服报警 | J3轴伺服驱动器报警 |
| 2051 | J4轴伺服报警 | J4轴伺服驱动器报警 |
| 2052 | J5轴伺服报警 | J5轴伺服驱动器报警 |
| 2053 | J6轴伺服报警 | J6轴伺服驱动器报警 |

***

## 完整示例

### 示例1：基础运动控制

```python
from dobot_sdk import DobotRobot, CoordinateType
import time

# 连接机器人
robot = DobotRobot("192.168.1.100")
robot.connect()

try:
    # 请求控制
    robot.robot_control.request_control()
    
    # 清除报警
    robot.robot_control.clear_error()
    
    # 使能
    robot.robot_control.enable_robot()
    print("机器人已使能")
    
    # 等待稳定
    time.sleep(2)
    
    # 关节运动
    print("执行关节运动...")
    robot.motion.movj([0, 0, 90, 0, 90, 0], CoordinateType.JOINT)
    time.sleep(3)
    
    # 直线运动
    print("执行直线运动...")
    robot.motion.movl([400, 0, 300, 180, 0, 0], CoordinateType.CARTESIAN)
    time.sleep(3)
    
    # 圆弧运动
    print("执行圆弧运动...")
    mid_point = [400, 100, 300, 180, 0, 0]
    end_point = [400, 200, 300, 180, 0, 0]
    robot.motion.arc(mid_point, end_point, CoordinateType.CARTESIAN)
    time.sleep(3)
    
    # 回到初始位置
    print("回到初始位置...")
    robot.motion.init_pose()
    time.sleep(3)
    
    # 下使能
    robot.robot_control.disable_robot()
    print("机器人已下使能")
    
finally:
    # 断开连接
    robot.disconnect()
    print("已断开连接")
```

### 示例2：IO控制

```python
from dobot_sdk import DobotRobot

with DobotRobot("192.168.1.100") as robot:
    robot.robot_control.request_control()
    robot.robot_control.clear_error()
    robot.robot_control.enable_robot()
    
    # 设置DO1
    robot.io.do(1, 1)
    print("DO1已打开")
    
    # 读取DI1状态
    response = robot.io.get_di(1)
    print(f"DI1状态: {response}")
    
    # 设置模拟输出
    robot.io.set_ao(1, 50)  # 输出5V
    print("AO1已设置为5V")
    
    # 等待输入信号
    print("等待DI1为高电平...")
    robot.io.di_group(0, [1, 0, 0, 0])
    print("DI1已触发")
    
    # 关闭DO1
    robot.io.do(1, 0)
    print("DO1已关闭")
```

### 示例3：状态监控

```python
from dobot_sdk import DobotRobot
import time

def on_status(status):
    """状态回调函数"""
    if status.tool_vector_actual:
        x = status.tool_vector_actual.x
        y = status.tool_vector_actual.y
        z = status.tool_vector_actual.z
        print(f"\r位置: X={x:.2f} Y={y:.2f} Z={z:.2f}", end="")

robot = DobotRobot("192.168.1.100")
robot.connect()
robot.robot_control.request_control()
robot.robot_control.clear_error()
robot.robot_control.enable_robot()

# 启动状态监控
robot.start_feedback_monitor(callback=on_status)

try:
    # 执行运动
    robot.motion.movj([400, 0, 300, 180, 0, 0], CoordinateType.CARTESIAN)
    time.sleep(5)
    
    # 获取当前状态
    status = robot.get_status()
    if status:
        print(f"\n最终位置: {status.tool_vector_actual.to_list()}")
        
finally:
    robot.stop_feedback_monitor()
    robot.disconnect()
```

### 示例4：力控模式

```python
from dobot_sdk import DobotRobot
import time

with DobotRobot("192.168.1.100") as robot:
    # 请求控制并使能机器人
    robot.robot_control.request_control()
    robot.robot_control.clear_error()
    robot.robot_control.enable_robot()
    
    # 开启力传感器
    robot.plugins.enable_ft_sensor(1)
    robot.plugins.six_force_home()
    
    # 设置力控参数
    stiffness = [1, 1, 1, 0, 0, 0]   # XYZ方向刚度
    force = [0, 0, -5, 0, 0, 0]       # Z方向施加5N力
    
    # 进入力控模式
    robot.plugins.fc_force_mode(stiffness, force)
    
    # 保持力控状态5秒
    time.sleep(5)
    
    # 停止力控
    robot.motion.stop()
```

***

## 附录

### 机器人模式对照表

| 值 | 模式名称  | 说明      |
| - | ----- | ------- |
| 1 | 初始化模式 | 系统初始化中  |
| 2 | 手动模式  | 手动操作模式  |
| 3 | 自动模式  | 自动运行模式  |
| 4 | 远程模式  | 远程控制模式  |
| 9 | 错误模式  | 错误/报警状态 |

### 常用端口

| 端口    | 用途        | 说明     |
| ----- | --------- | ------ |
| 29999 | Dashboard | 命令控制端口 |
| 30004 | Feedback  | 状态反馈端口 |
| 30003 | Real-time | 实时控制端口 |

### 指令类型说明

| 类型   | 说明          | 示例                        |
| ---- | ----------- | ------------------------- |
| 队列指令 | 加入运动队列，顺序执行 | MovJ, MovL, Arc           |
| 立即指令 | 立即执行，不进入队列  | GetPose, ClearError, Stop |

### 坐标系说明

| 坐标系   | 范围  | 说明       |
| ----- | --- | -------- |
| 用户坐标系 | 0-9 | 用户自定义坐标系 |
| 工具坐标系 | 0-9 | 工具末端坐标系  |

### 速度加速度范围

| 参数    | 范围    | 说明   |
| ----- | ----- | ---- |
| 速度比例  | 0-100 | 百分比  |
| 加速度比例 | 0-100 | 百分比  |
| 平滑过渡  | 0-100 | cp参数 |

### 安全注意事项

1. **急停按钮**：确保急停按钮易于触及
2. **速度限制**：首次调试建议使用低速
3. **碰撞检测**：开启碰撞检测功能
4. **安全区域**：确保机器人工作范围内无人
5. **负载检查**：正确设置负载参数

***

**文档版本**: V1.0\
**生成日期**: 2026年5月\
**适用SDK**: Dobot TCP-IP Python SDK V4.0
