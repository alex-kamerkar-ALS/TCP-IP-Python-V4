"""
插件模块测试（力控和传送带）
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dobot_sdk import DobotRobot


def test_plugins_methods():
    """测试插件模块方法"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试力控方法
    assert hasattr(robot.plugins, 'fc_force_mode')
    assert hasattr(robot.plugins, 'fc_set_deviation')
    assert hasattr(robot.plugins, 'fc_set_force_limit')
    assert hasattr(robot.plugins, 'fc_set_mass')
    assert hasattr(robot.plugins, 'fc_set_stiffness')
    assert hasattr(robot.plugins, 'fc_set_damping')
    assert hasattr(robot.plugins, 'fc_off')
    assert hasattr(robot.plugins, 'fc_set_force')
    assert hasattr(robot.plugins, 'set_fc_collision')
    assert hasattr(robot.plugins, 'fc_collision_switch')
    print("力控方法存在")
    
    # 测试传送带方法
    assert hasattr(robot.plugins, 'cnv_init')
    assert hasattr(robot.plugins, 'get_cnv_object')
    assert hasattr(robot.plugins, 'start_sync_cnv')
    assert hasattr(robot.plugins, 'cnv_movl')
    assert hasattr(robot.plugins, 'cnv_movc')
    assert hasattr(robot.plugins, 'stop_sync_cnv')
    assert hasattr(robot.plugins, 'set_cnv_point_offset')
    assert hasattr(robot.plugins, 'set_cnv_time_compensation')
    print("传送带方法存在")
    
    del robot
    print("插件模块方法测试通过！")


def test_plugins_command_generation():
    """测试插件指令生成"""
    robot = DobotRobot("192.168.1.100")
    
    # 测试力控模式设置
    result = robot.plugins.fc_force_mode(1)
    assert result is not None
    print(f"fc_force_mode(1): {result}")
    
    # 测试力关闭
    result = robot.plugins.fc_off()
    assert result is not None
    print(f"fc_off(): {result}")
    
    # 测试传送带初始化
    result = robot.plugins.cnv_init(0)
    assert result is not None
    print(f"cnv_init(0): {result}")
    
    del robot
    print("插件指令生成测试通过！")


if __name__ == "__main__":
    print("运行插件模块测试...\n")
    
    test_plugins_methods()
    print()
    
    test_plugins_command_generation()
    print()
    
    print("=" * 50)
    print("插件模块所有测试通过！")
