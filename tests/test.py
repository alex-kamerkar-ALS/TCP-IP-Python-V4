from dobot_sdk import DobotRobot,CoordinateType
# from dobot_sdk.api.motion import CoordinateType
import time

with DobotRobot("192.168.5.1") as robot:
    robot.robot_control.request_control()
    robot.robot_control.enable_robot()

    # p1=[-200, -70, 400, -180, 0, -180]
    # p2=[-200, -100, 400, -180, 0, -180]
    p1=[-200, -70, 400, -180, 0, -180]
    p2=[-8.7346, -27.2151, 83.8642, 33.3090, -89.7513, -98.6253]   

    # 笛卡尔空间运动
    robot.motion.movj(
        pose=p1,
        coord_type=CoordinateType.CARTESIAN
    )
    robot.motion.movj(
        pose=p2,
        coord_type=CoordinateType.JOINT
    )    

    # 直线运动
    robot.motion.movl(
        pose=p1,
        coord_type=CoordinateType.CARTESIAN
    )    
    robot.motion.movl(
        pose=p2,
        coord_type=CoordinateType.JOINT
    )

        # 数字输出
    robot.io.do_on(4)    # 打开DO1
    time.sleep(10)
    robot.io.do_off(4)   # 关闭DO1

    # 读取输入
    di_status = robot.io.di(6)  # 读取DI1
    print(di_status)