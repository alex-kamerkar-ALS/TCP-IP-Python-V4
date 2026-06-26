"""
IO模块测试
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dobot_sdk import DobotRobot


def test_io_methods():
    """测试IO模块方法"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试数字输出方法
    assert hasattr(robot.io, 'do')
    assert hasattr(robot.io, 'do_on')
    assert hasattr(robot.io, 'do_off')
    assert hasattr(robot.io, 'do_instant')
    print("数字输出方法存在")
    
    # 测试数字输入方法
    assert hasattr(robot.io, 'di')
    assert hasattr(robot.io, 'get_di')
    print("数字输入方法存在")
    
    # 测试数字输出组方法
    assert hasattr(robot.io, 'do_group')
    assert hasattr(robot.io, 'do_group_dec')
    assert hasattr(robot.io, 'get_do_group')
    print("数字输出组方法存在")
    
    # 测试数字输入组方法
    assert hasattr(robot.io, 'di_group')
    assert hasattr(robot.io, 'di_group_dec')
    print("数字输入组方法存在")
    
    # 测试模拟输出方法
    assert hasattr(robot.io, 'ao')
    assert hasattr(robot.io, 'ao_instant')
    assert hasattr(robot.io, 'get_ao')
    assert hasattr(robot.io, 'get_ai')
    print("模拟输入输出方法存在")
    
    # 测试工具IO方法
    assert hasattr(robot.io, 'tool_do')
    assert hasattr(robot.io, 'tool_do_instant')
    assert hasattr(robot.io, 'tool_di')
    assert hasattr(robot.io, 'tool_ai')
    print("工具IO方法存在")
    
    # 测试工具设置方法
    assert hasattr(robot.io, 'set_tool_power')
    assert hasattr(robot.io, 'set_tool_mode')
    assert hasattr(robot.io, 'set_tool_485')
    print("工具设置方法存在")
    
    del robot
    print("IO模块测试通过！")


def test_io_parameter_validation():
    """测试IO参数验证"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试do_on方法
    result = robot.io.do_on(1)
    assert result is not None
    print(f"do_on(1): {result}")
    
    # 测试do_off方法
    result = robot.io.do_off(1)
    assert result is not None
    print(f"do_off(1): {result}")
    
    # 测试别名方法
    result = robot.io.get_di(1)
    assert result is not None
    print(f"get_di(1): {result}")
    
    del robot
    print("IO参数验证测试通过！")


if __name__ == "__main__":
    print("运行IO模块测试...\n")
    
    test_io_methods()
    print()
    
    test_io_parameter_validation()
    print()
    
    print("=" * 50)
    print("IO模块所有测试通过！")
