"""
示例6: 力控和传送带

演示力传感器控制和传送带跟踪功能
"""

from dobot_sdk import DobotRobot
from dobot_sdk import CoordinateType
import time


def main():
    ROBOT_IP = "120.79.211.106"
    
    try:
        with DobotRobot(ROBOT_IP) as robot:
            print("=" * 50)
            print("6. 力控和传送带示例")
            print("=" * 50)
            
            # 初始化
            robot.robot_control.request_control()
            robot.robot_control.clear_error()
            robot.robot_control.enable_robot(load=1.0)
            robot.robot_control.speed_factor(30)
            
            # ========== 力传感器控制 ==========
            print("\n--- 力传感器控制 ---")
            
            # 检查是否有力传感器
            print("开启力传感器...")
            response = robot.plugins.enable_ft_sensor(1)
            print(f"响应: {response}")
            time.sleep(1)
            
            # 力传感器归零
            print("力传感器归零...")
            response = robot.plugins.six_force_home()
            print(f"响应: {response}")
            time.sleep(1)
            
            # 获取力传感器数据
            print("读取力传感器数据...")
            for i in range(3):
                force_data = robot.plugins.get_force()
                print(f"力数据 {i+1}: {force_data}")
                time.sleep(0.5)
            
            # 进入力控拖拽模式
            print("\n进入力控拖拽模式...")
            response = robot.plugins.force_drive_mode(1)
            print(f"响应: {response}")
            print("等待5秒，可手动拖拽机器人...")
            time.sleep(5)
            
            # 退出力控拖拽模式
            print("退出力控拖拽模式...")
            response = robot.plugins.force_drive_mode(0)
            print(f"响应: {response}")
            
            # 关闭力传感器
            print("关闭力传感器...")
            response = robot.plugins.enable_ft_sensor(0)
            print(f"响应: {response}")
            
            # ========== 传送带控制（演示） ==========
            print("\n--- 传送带控制 ---")
            
            # 注意：实际使用传送带需要先配置编码器
            print("开启传送带...")
            response = robot.plugins.cnv_init(1)
            print(f"响应: {response}")
            
            # 开启传送带跟踪
            print("开启传送带跟踪...")
            response = robot.plugins.start_sync_cnv()
            print(f"响应: {response}")
            
            # 模拟传送带跟踪运动
            print("等待工件进入抓取区域...")
            # response = robot.plugins.get_cnv_object(timeout=5000)
            # print(f"工件检测响应: {response}")
            
            print("停止传送带跟踪...")
            response = robot.plugins.stop_sync_cnv()
            print(f"响应: {response}")
            
            print("关闭传送带...")
            response = robot.plugins.cnv_init(0)
            print(f"响应: {response}")
            
            # 返回安全位置
            print("\n返回安全位置...")
            safe_pose = [0, -30, -60, 0, 90, 0]
            robot.motion.movj(safe_pose, CoordinateType.JOINT)
            time.sleep(3)
            
            # 下使能
            robot.robot_control.disable_robot()
            
            print("\n" + "=" * 50)
            print("✅ 力控和传送带示例完成")
            print("=" * 50)
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
