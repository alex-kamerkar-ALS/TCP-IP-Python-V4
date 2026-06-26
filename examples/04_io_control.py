"""
示例4: IO控制

演示数字IO、模拟IO和末端IO的使用方法
"""

from dobot_sdk import DobotRobot
import time


def main():
    ROBOT_IP = "192.168.1.100"
    
    try:
        with DobotRobot(ROBOT_IP) as robot:
            print("=" * 50)
            print("4. IO控制示例")
            print("=" * 50)
            
            # 初始化
            robot.robot_control.request_control()
            robot.robot_control.clear_error()
            robot.robot_control.enable_robot(load=1.0)
            
            # ========== 数字输出控制 ==========
            print("\n--- 数字输出控制 (DO) ---")
            
            # 方式1: 使用 do_on/do_off
            print("打开DO1...")
            robot.io.do_on(1)
            time.sleep(1)
            
            print("关闭DO1...")
            robot.io.do_off(1)
            time.sleep(1)
            
            # 方式2: 使用 do（队列指令）
            print("设置DO2为ON...")
            robot.io.do(2, 1)
            time.sleep(1)
            
            print("设置DO2为OFF...")
            robot.io.do(2, 0)
            time.sleep(1)
            
            # 方式3: 使用 DOInstant（立即指令）
            print("使用立即指令设置DO3...")
            robot.io.do_instant(3, 1)
            time.sleep(1)
            robot.io.do_instant(3, 0)
            time.sleep(1)
            
            # ========== 数字输入读取 ==========
            print("\n--- 数字输入读取 (DI) ---")
            for i in range(1, 5):
                di_status = robot.io.get_di(i)
                print(f"DI{i} 状态: {di_status}")
            
            # ========== 数字输出状态读取 ==========
            print("\n--- 数字输出状态读取 (DO) ---")
            for i in range(1, 4):
                do_status = robot.io.get_do(i)
                print(f"DO{i} 状态: {do_status}")
            
            # ========== 模拟输出控制 ==========
            print("\n--- 模拟输出控制 (AO) ---")
            print("设置AO1为25%...")
            robot.io.ao(1, 25)
            time.sleep(2)
            
            print("设置AO1为75%...")
            robot.io.ao(1, 75)
            time.sleep(2)
            
            print("设置AO1为0%...")
            robot.io.ao(1, 0)
            time.sleep(1)
            
            # ========== 模拟输入读取 ==========
            print("\n--- 模拟输入读取 (AI) ---")
            for i in range(1, 3):
                ai_value = robot.io.get_ai(i)
                print(f"AI{i} 值: {ai_value}")
            
            # ========== 末端IO控制 ==========
            print("\n--- 末端IO控制 (Tool IO) ---")
            
            # 设置末端DO
            print("设置末端DO1为ON...")
            robot.io.tool_do(1, 1)
            time.sleep(1)
            
            print("设置末端DO1为OFF...")
            robot.io.tool_do(1, 0)
            time.sleep(1)
            
            # 读取末端DI
            print("读取末端DI...")
            tool_di_status = robot.io.tool_di()
            print(f"末端DI 状态: {tool_di_status}")
            
            # 设置末端工具供电（开启）
            print("\n开启末端工具供电...")
            robot.io.set_tool_power(1)  # 1 = 开启
            
            # ========== 批量IO操作 ==========
            print("\n--- 批量IO操作 ---")
            print("设置IO组0的DO为ON...")
            robot.io.do_group(0, "{1,1,1,1}")  # group_index=0, status="{1,1,1,1}"
            time.sleep(2)
            
            print("设置IO组0的DO为OFF...")
            robot.io.do_group(0, "{0,0,0,0}")
            time.sleep(1)
            
            # 下使能
            robot.robot_control.disable_robot()
            
            print("\n" + "=" * 50)
            print("✅ IO控制示例完成")
            print("=" * 50)
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
