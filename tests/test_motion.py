"""
运动控制模块测试
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dobot_sdk import DobotRobot
from dobot_sdk import CoordinateType


def test_motion_methods():
    """测试运动控制方法"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试MovJ方法
    assert hasattr(robot.motion, 'movj')
    print("movj方法存在")
    
    # 测试MovL方法
    assert hasattr(robot.motion, 'movl')
    print("movl方法存在")
    
    # 测试Arc方法
    assert hasattr(robot.motion, 'arc')
    print("arc方法存在")
    
    # 测试Circle方法
    assert hasattr(robot.motion, 'circle')
    print("circle方法存在")
    
    # 测试相对运动方法
    assert hasattr(robot.motion, 'rel_movl')
    assert hasattr(robot.motion, 'rel_movl_tool')
    assert hasattr(robot.motion, 'rel_movl_user')
    print("相对运动方法存在")
    
    # 测试速度设置方法
    assert hasattr(robot.motion, 'speed')
    assert hasattr(robot.motion, 'acceleration')
    print("速度/加速度设置方法存在")
    
    # 测试工具设置方法
    assert hasattr(robot.motion, 'tool_voltage')
    assert hasattr(robot.motion, 'tool_pose')
    print("工具设置方法存在")
    
    # 测试伺服控制方法
    assert hasattr(robot.motion, 'servo_j')
    assert hasattr(robot.motion, 'servo_p')
    print("伺服控制方法存在")
    
    # 测试Jog控制方法
    assert hasattr(robot.motion, 'move_jog')
    assert hasattr(robot.motion, 'jog_stop')
    print("Jog控制方法存在")
    
    # 测试坐标系设置方法
    assert hasattr(robot.motion, 'set_user')
    assert hasattr(robot.motion, 'set_tool')
    print("坐标系设置方法存在")
    
    del robot
    print("运动控制方法测试通过！")


def test_motion_command_generation():
    """测试运动指令生成"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试MovJ指令生成
    result = robot.motion.movj([400, 0, 300, 180, 0, 0], CoordinateType.CARTESIAN)
    assert result is not None
    print(f"MovJ指令: {result}")
    
    # 测试MovL指令生成
    result = robot.motion.movl([400, 100, 300, 180, 0, 0], CoordinateType.CARTESIAN)
    assert result is not None
    print(f"MovL指令: {result}")
    
    # 测试相对运动
    result = robot.motion.rel_movl([50, 0, 0, 0, 0, 0])
    assert result is not None
    print(f"相对运动指令: {result}")
    
    # 测试关节运动
    result = robot.motion.movj([0, -30, -60, 0, 90, 0], CoordinateType.JOINT)
    assert result is not None
    print(f"关节运动指令: {result}")
    
    del robot
    print("运动指令生成测试通过！")


def test_coordinate_type_enum():
    """测试坐标系类型枚举"""
    assert CoordinateType.CARTESIAN == 0
    assert CoordinateType.JOINT == 1
    assert CoordinateType.CARTESIAN.name == 'CARTESIAN'
    assert CoordinateType.JOINT.name == 'JOINT'
    print("坐标系类型枚举测试通过！")


if __name__ == "__main__":
    print("运行运动控制模块测试...\n")
    
    test_motion_methods()
    print()
    
    test_motion_command_generation()
    print()
    
    test_coordinate_type_enum()
    print()
    
    print("=" * 50)
    print("运动控制模块所有测试通过！")
