"""
通信模块测试（Modbus）
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dobot_sdk import DobotRobot


def test_communication_methods():
    """测试通信模块方法"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试Modbus方法
    assert hasattr(robot.communication, 'modbus_create')
    assert hasattr(robot.communication, 'modbus_rtu_create')
    assert hasattr(robot.communication, 'modbus_close')
    print("Modbus创建/关闭方法存在")
    
    # 测试输入寄存器方法
    assert hasattr(robot.communication, 'get_in_bits')
    assert hasattr(robot.communication, 'get_in_regs')
    print("输入寄存器方法存在")
    
    # 测试线圈方法
    assert hasattr(robot.communication, 'get_coils')
    assert hasattr(robot.communication, 'set_coils')
    print("线圈方法存在")
    
    # 测试保持寄存器方法
    assert hasattr(robot.communication, 'get_hold_regs')
    assert hasattr(robot.communication, 'set_hold_regs')
    print("保持寄存器方法存在")
    
    del robot
    print("通信模块方法测试通过！")


def test_communication_command_generation():
    """测试通信指令生成"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试Modbus创建
    result = robot.communication.modbus_create(1, "192.168.1.101", 502)
    assert result is not None
    print(f"modbus_create(1, 192.168.1.101, 502): {result}")
    
    # 测试读取输入寄存器
    result = robot.communication.get_in_regs(1, 0, 10)
    assert result is not None
    print(f"get_in_regs(1, 0, 10): {result}")
    
    del robot
    print("通信指令生成测试通过！")


if __name__ == "__main__":
    print("运行通信模块测试...\n")
    
    test_communication_methods()
    print()
    
    test_communication_command_generation()
    print()
    
    print("=" * 50)
    print("通信模块所有测试通过！")
