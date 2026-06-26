# Copyright (c) 2026 Dobot
# Licensed under the MIT License

"""Robot Control模块 - 状态查询、运动学计算、可达性检查、机器人控制"""

from typing import Tuple, Sequence
from ..core.connection import DobotConnection


class RobotControl:
    """Robot控制模块 - 状态查询、运动学计算、可达性检查、日志、脚本控制"""

    def __init__(self, connection: DobotConnection):
        self.connection = connection

    def _send_cmd(self, command: str) -> str:
        """发送命令并接收响应"""
        return self.connection.send_receive_text(command)

    # ==================== 控制模式与电源====================

    def request_control(self) -> str:
        """
        RequestControl请求将设备控制模式切换为TCP模式（立即指令）
        
        说明：
        - 只有在TCP模式下才可执行其他TCP指令
        - 仅当机器人处于未上电或下使能（且非暂停或松抱闸状态）时才可切换TCP模式
        - 调用此接口后，才能执行enable_robot、运动指令等
        
        Returns:
            str: ErrorID,{},RequestControl();
        """
        return self._send_cmd("RequestControl()")

    def power_on(self) -> str:
        """PowerOn机器人上电（立即指令）"""
        return self._send_cmd("PowerOn()")

    def enable_robot(self, load: float = 0.0, **kwargs) -> str:
        """
        EnableRobot使能机器人（立即指令）        
        Args:
            load: 负载重量 (kg)
            centerX, centerY, centerZ: 负载重心坐标
            isCheck: 是否检查负载 (0/1)
        """
        if load == 0.0:
            cmd = "EnableRobot()"
        elif 'centerX' not in kwargs:
            cmd = f"EnableRobot({load:.6f})"
        else:
            cx = kwargs.get('centerX', 0.0)
            cy = kwargs.get('centerY', 0.0)
            cz = kwargs.get('centerZ', 0.0)
            check = kwargs.get('isCheck', 0)
            cmd = f"EnableRobot({load:.6f},{cx:.6f},{cy:.6f},{cz:.6f},{check})"
        return self._send_cmd(cmd)

    def disable_robot(self) -> str:
        """DisableRobot下使能机器人（立即指令）"""
        return self._send_cmd("DisableRobot()")

    def clear_error(self) -> str:
        """ClearError清除机器人报警（立即指令）"""
        return self._send_cmd("ClearError()")

    # ==================== 运动控制 ====================

    def run_script(self, script_name: str) -> str:
        """
        RunScript运行指定工程（立即指令）
        
        Args:
            script_name: 脚本文件名        """
        return self._send_cmd(f"RunScript(\"{script_name}\")")

    def stop(self) -> str:
        """Stop停止运动（或正在运行的工程）（立即指令）"""
        return self._send_cmd("Stop()")

    def pause(self) -> str:
        """Pause暂停运动（或正在运行的工程）（立即指令）"""
        return self._send_cmd("Pause()")

    def continue_motion(self) -> str:
        """Continue继续运动（或已暂停的工程）（立即指令）"""
        return self._send_cmd("Continue()")

    def emergency_stop(self) -> str:
        """EmergencyStop紧急停止机器人（立即指令）"""
        return self._send_cmd("EmergencyStop()")

    # ==================== 抱闸与拖拽====================

    def brake_control(self, axis_id: int, value: int) -> str:
        """
        BrakeControl控制指定关节的抱闸（立即指令）        
        Args:
            axis_id: 关节编号 (1-6)
            value: 0-抱闸, 1-松闸
        """
        if not 1 <= axis_id <= 6:
            raise ValueError("关节编号必须在1-6之间")
        if value not in [0, 1]:
            raise ValueError("value必须是0或1")
        return self._send_cmd(f"BrakeControl({axis_id},{value})")

    def start_drag(self) -> str:
        """StartDrag机器人进入关节拖拽模式（立即指令）"""
        return self._send_cmd("StartDrag()")

    def stop_drag(self) -> str:
        """StopDrag机器人退出拖拽模式（立即指令）"""
        return self._send_cmd("StopDrag()")

    def drag_sensivity(self, level: int) -> str:
        """
        DragSensivity设置拖拽灵敏度（立即指令）        
        Args:
            level: 灵敏度等级(0-10)
        """
        if not 0 <= level <= 10:
            raise ValueError("灵敏度等级必须在0-10之间")
        return self._send_cmd(f"DragSensivity({level})")

    # ==================== 速度与加速度设置 ====================

    def speed_factor(self, factor: int) -> str:
        """
        SpeedFactor设置全局速度比例（立即指令）
        
        Args:
            factor: 速度比例 (0-100)
        """
        if not 0 <= factor <= 100:
            raise ValueError("速度比例必须在0-100之间")
        return self._send_cmd(f"SpeedFactor({factor})")

    def acc_j(self, acc: int) -> str:
        """
        AccJ设置关节运动方式的加速度比例（立即指令）
        
        Args:
            acc: 加速度比例 (1-100)
        """
        if not 1 <= acc <= 100:
            raise ValueError("加速度比例必须在0-100之间")
        return self._send_cmd(f"AccJ({acc})")

    def acc_l(self, acc: int) -> str:
        """
        AccL设置直线和弧线运动方式的加速度比例（立即指令）
        
        Args:
            acc: 加速度比例 (1-100)
        """
        if not 1 <= acc <= 100:
            raise ValueError("加速度比例必须在0-100之间")
        return self._send_cmd(f"AccL({acc})")

    def vel_j(self, vel: int) -> str:
        """
        VelJ设置关节运动方式的速度比例（立即指令）
        
        Args:
            vel: 速度比例 (1-100)
        """
        if not 1 <= vel <= 100:
            raise ValueError("速度比例必须在0-100之间")
        return self._send_cmd(f"VelJ({vel})")

    def vel_l(self, vel: int) -> str:
        """
        VelL设置直线和弧线运动方式的速度比例（立即指令）
        
        Args:
            vel: 速度比例 (1-100)
        """
        if not 1 <= vel <= 100:
            raise ValueError("速度比例必须在0-100之间")
        return self._send_cmd(f"VelL({vel})")

    def cp(self, value: int) -> str:
        """
        CP设置平滑过渡比例（立即指令）
        
        Args:
            value: 平滑过渡比例 (0-100)
        """
        if not 0 <= value <= 100:
            raise ValueError("平滑过渡比例必须在0-100之间")
        return self._send_cmd(f"CP({value})")

    # ==================== 坐标系设置====================

    def user(self, index: int) -> str:
        """
        User设置全局用户坐标系（队列指令）        
        Args:
            index: 用户坐标系编号(0-50)
        """
        if not 0 <= index <= 50:
            raise ValueError("用户坐标系编号必须在0-50之间")
        return self._send_cmd(f"User({index})")

    def set_user(self, index: int, pose: Sequence[float]) -> str:
        """
        SetUser修改指定的用户坐标系（立即指令）
        
        Args:
            index: 用户坐标系编号(0-50)
            pose: 6个坐标参数[x,y,z,rx,ry,rz]
        """
        if not 0 <= index <= 50:
            raise ValueError("用户坐标系编号必须在0-50之间")
        if len(pose) != 6:
            raise ValueError("pose需要6个参数")
        pose_str = "{" + ",".join([f"{v:.6f}" for v in pose]) + "}"
        return self._send_cmd(f"SetUser({index},{pose_str})")

    def calc_user(self, index: int, matrix_direction: int, table: Sequence[float]) -> str:
        """
        CalcUser计算用户坐标系（立即指令）
        Args:
            index: 用户坐标系编号(0-9)
            matrix_direction: 计算方向 (1-左乘，坐标系沿基坐标系偏转; 0-右乘，坐标系沿自身偏转)
            table: 偏移值 [x,y,z,rx,ry,rz]
        """
        if not 0 <= index <= 9:
            raise ValueError("用户坐标系编号必须在0-9之间")
        if matrix_direction not in [0, 1]:
            raise ValueError("matrix_direction 必须是0或1")
        if len(table) != 6:
            raise ValueError("table需要6个参数")
        table_str = "{" + ",".join([f"{v:.6f}" for v in table]) + "}"
        return self._send_cmd(f"CalcUser({index},{matrix_direction},{table_str})")

    def tool(self, index: int) -> str:
        """
        Tool设置全局工具坐标系（队列指令）        
        Args:
            index: 工具坐标系编号(0-50)
        """
        if not 0 <= index <= 50:
            raise ValueError("工具坐标系编号必须在0-50之间")
        return self._send_cmd(f"Tool({index})")

    def set_tool(self, index: int, pose: Sequence[float]) -> str:
        """
        SetTool修改指定的工具坐标系（立即指令）
        
        Args:
            index: 工具坐标系编号(0-50)
            pose: 6个坐标参数[x,y,z,rx,ry,rz]
        """
        if not 0 <= index <= 50:
            raise ValueError("工具坐标系编号必须在0-50之间")
        if len(pose) != 6:
            raise ValueError("pose需要6个参数")
        pose_str = "{" + ",".join([f"{v:.6f}" for v in pose]) + "}"
        return self._send_cmd(f"SetTool({index},{pose_str})")

    def calc_tool(self, index: int, matrix_direction: int, table: Sequence[float]) -> str:
        """
        CalcTool计算工具坐标系（立即指令）
        Args:
            index: 工具坐标系编号(0-9)
            matrix_direction: 计算方向 (1-左乘，坐标系沿法兰坐标系偏转; 0-右乘，坐标系沿自身偏转)
            table: 偏移值 [x,y,z,rx,ry,rz]
        """
        if not 0 <= index <= 9:
            raise ValueError("工具坐标系编号必须在0-9之间")
        if matrix_direction not in [0, 1]:
            raise ValueError("matrix_direction 必须是0或1")
        if len(table) != 6:
            raise ValueError("table需要6个参数")
        table_str = "{" + ",".join([f"{v:.6f}" for v in table]) + "}"
        return self._send_cmd(f"CalcTool({index},{matrix_direction},{table_str})")

    # ==================== 负载设置 ====================

    def set_payload(self, load: float, center: Sequence[float] = None) -> str:
        """
        SetPayload设置机械臂末端负载（队列指令）        
        Args:
            load: 负载重量 (kg)
            center: 负载重心坐标 [x,y,z] (mm)，不传则只设置重量
        """
        if center is not None:
            if len(center) != 3:
                raise ValueError("center需要3个参数[x,y,z]")
            return self._send_cmd(f"SetPayload({load:.6f},{{{center[0]:.6f},{center[1]:.6f},{center[2]:.6f}}})")
        return self._send_cmd(f"SetPayload({load:.6f})")

    # ==================== 碰撞检测设置====================

    def set_collision_level(self, level: int) -> str:
        """
        SetCollisionLevel设置碰撞检测等级（队列指令）        
        Args:
            level: 碰撞检测等级(0-5)，0为关闭碰撞检测，1~5数字越大灵敏度越高
        """
        if not 0 <= level <= 5:
            raise ValueError("碰撞检测等级必须在0-5之间")
        return self._send_cmd(f"SetCollisionLevel({level})")

    def set_back_distance(self, distance: float) -> str:
        """
        SetBackDistance设置碰撞回退距离（队列指令）
        
        Args:
            distance: 碰撞回退距离 (mm)
        """
        return self._send_cmd(f"SetBackDistance({distance:.6f})")

    def set_post_collision_mode(self, mode: int) -> str:
        """
        SetPostCollisionMode设置碰撞后处理方式（队列指令）        
        Args:
            mode: 碰撞后处理模式(0-2)
                  0: 下使能并停止运动
                  1: 暂停运动
                  2: 忽略碰撞继续运动
        """
        if mode not in [0, 1, 2]:
            raise ValueError("碰撞后处理模式必须是0或2")
        return self._send_cmd(f"SetPostCollisionMode({mode})")

    # ==================== 安全皮肤与安全区域====================

    def enable_safe_skin(self, status: int) -> str:
        """
        EnableSafeSkin开启或关闭安全皮肤功能（队列指令）
        
        Args:
            status: 0-关闭, 1-开启        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"EnableSafeSkin({status})")

    def set_safe_skin(self, part: int, sensitivity: int) -> str:
        """
        SetSafeSkin设置安全皮肤各个部位的灵敏度（队列指令）
        
        Args:
            part: 安全皮肤部位编号 (0-...)
            sensitivity: 灵敏度(0-10)
        """
        if not 0 <= sensitivity <= 10:
            raise ValueError("灵敏度必须在0-10之间")
        return self._send_cmd(f"SetSafeSkin({part},{sensitivity})")

    def set_safe_wall_enable(self, index: int, status: int) -> str:
        """
        SetSafeWallEnable开启或关闭指定的安全墙（队列指令）
        
        Args:
            index: 安全墙编号            status: 0-关闭, 1-开启        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"SetSafeWallEnable({index},{status})")

    def set_work_zone_enable(self, index: int, status: int) -> str:
        """
        SetWorkZoneEnable开启或关闭指定的安全区域（队列指令）        
        Args:
            index: 安全区域编号
            status: 0-关闭, 1-开启        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"SetWorkZoneEnable({index},{status})")

    # ==================== 状态查询====================

    def robot_mode(self) -> str:
        """RobotMode获取机器人当前状态（立即指令）"""
        return self._send_cmd("RobotMode()")

    def get_pose(self, user: int = None, tool: int = None) -> str:
        """
        GetPose获取机器人当前位姿在指定坐标系下的笛卡尔坐标（立即指令）
        
        Args:
            user: 用户坐标系索引(0-50)
            tool: 工具坐标系索引(0-50)
        """
        has_coord = user is not None or tool is not None
        if has_coord and (user is None or tool is None):
            raise ValueError("user 和 tool 参数必须同时设置或都不设置")

        if has_coord:
            if not (0 <= user <= 50):
                raise ValueError("user 必须在0-50 之间")
            if not (0 <= tool <= 50):
                raise ValueError("tool 必须在0-50 之间")
            return self._send_cmd(f"GetPose(user={user},tool={tool})")
        else:
            return self._send_cmd("GetPose()")

    def get_angle(self) -> str:
        """GetAngle获取机器人当前位姿的关节坐标（立即指令）"""
        return self._send_cmd("GetAngle()")

    def get_error_id(self) -> str:
        """GetErrorID获取机器人当前报错的错误码（立即指令）"""
        return self._send_cmd("GetErrorID()")

    def get_scr_name(self) -> str:
        """GetScrName获取当前机器人正在运行的脚本名称（立即指令）"""
        return self._send_cmd("GetScrName()")

    # ==================== 运动学计算====================

    def positive_kin(self, joints: Sequence[float]) -> str:
        """
        PositiveKin进行正解运算（立即指令）
        
        Args:
            joints: 6个关节角度[j1,j2,j3,j4,j5,j6]
        """
        if len(joints) != 6:
            raise ValueError("需要6个关节角度")
        joint_str = ",".join([f"{j:.6f}" for j in joints])
        return self._send_cmd(f"PositiveKin({joint_str})")

    def inverse_kin(self, pose: Sequence[float]) -> str:
        """
        InverseKin进行逆解运算（立即指令）
        
        Args:
            pose: 6个笛卡尔坐标 [x,y,z,rx,ry,rz]
        """
        if len(pose) != 6:
            raise ValueError("需要6个位姿参数")
        pose_str = ",".join([f"{p:.6f}" for p in pose])
        return self._send_cmd(f"InverseKin({pose_str})")

    # ==================== 可达性检测====================

    def check_odd_movl(self, joints_start: Sequence[float], joints_end: Sequence[float]) -> str:
        """
        CheckOddMovL检查直线运动的点位可达性（立即指令）        
        Args:
            joints_start: 起点关节角度[j1,j2,j3,j4,j5,j6]
            joints_end: 终点关节角度[j1,j2,j3,j4,j5,j6]
        """
        if len(joints_start) != 6:
            raise ValueError("起点需要6个关节角度")
        if len(joints_end) != 6:
            raise ValueError("终点需要6个关节角度")
        joint_str1 = "joint={" + ",".join([f"{j:.6f}" for j in joints_start]) + "}"
        joint_str2 = "joint={" + ",".join([f"{j:.6f}" for j in joints_end]) + "}"
        return self._send_cmd(f"CheckOddMovL({joint_str1},{joint_str2})")

    def check_odd_movj(self, joints_start: Sequence[float], joints_end: Sequence[float]) -> str:
        """
        CheckOddMovJ检查关节运动的点位可达性（立即指令）        
        Args:
            joints_start: 起点关节角度[j1,j2,j3,j4,j5,j6]
            joints_end: 终点关节角度[j1,j2,j3,j4,j5,j6]
        """
        if len(joints_start) != 6:
            raise ValueError("起点需要6个关节角度")
        if len(joints_end) != 6:
            raise ValueError("终点需要6个关节角度")
        joint_str1 = "joint={" + ",".join([f"{j:.6f}" for j in joints_start]) + "}"
        joint_str2 = "joint={" + ",".join([f"{j:.6f}" for j in joints_end]) + "}"
        return self._send_cmd(f"CheckOddMovJ({joint_str1},{joint_str2})")

    def check_odd_movc(self, joints_start: Sequence[float], joints_via: Sequence[float], joints_end: Sequence[float]) -> str:
        """
        CheckOddMovC检查圆弧运动的点位可达性（立即指令）        
        Args:
            joints_start: 起点关节角度[j1,j2,j3,j4,j5,j6]
            joints_via: 中间点关节角度[j1,j2,j3,j4,j5,j6]
            joints_end: 终点关节角度[j1,j2,j3,j4,j5,j6]
        """
        if len(joints_start) != 6:
            raise ValueError("起点需要6个关节角度")
        if len(joints_via) != 6:
            raise ValueError("中间点需要6个关节角度")
        if len(joints_end) != 6:
            raise ValueError("终点需要6个关节角度")
        joint_str1 = "joint={" + ",".join([f"{j:.6f}" for j in joints_start]) + "}"
        joint_str2 = "joint={" + ",".join([f"{j:.6f}" for j in joints_via]) + "}"
        joint_str3 = "joint={" + ",".join([f"{j:.6f}" for j in joints_end]) + "}"
        return self._send_cmd(f"CheckOddMovC({joint_str1},{joint_str2},{joint_str3})")

    # ==================== 托盘相关 ====================

    def create_tray(self, name: str, dimensions: Sequence[int],
                    points: list) -> str:
        """
        CreateTray创建托盘（立即指令）
        支持一维、二维、三维托盘。
        
        Args:
            name: 托盘名称（最长32字节字符串，不允许纯数字或纯空格）
            dimensions: 维度参数
                - 一维: [count] 点位数量[2,50]
                - 二维: [row, col] 行数和列数
                - 三维: [row, col, layer] 行数、列数、层数
            points: 端点列表，每个端点为[x,y,z,rx,ry,rz]格式
                - 一维: 2个端点 [p1, p2]
                - 二维: 4个端点 [p1, p2, p3, p4]
                - 三维: 8个端点 [p1, p2, p3, p4, p5, p6, p7, p8]
        """
        dims = ",".join([str(d) for d in dimensions])
        point_strs = []
        for p in points:
            if len(p) != 6:
                raise ValueError(f"每个点位需要6个值[x,y,z,rx,ry,rz]，当前传入{len(p)}个")
            point_strs.append("{pose = {" + ",".join([f"{v:.6f}" for v in p]) + "}}")
        cmd = f"CreateTray({name},{{{dims}}}," + ",".join(point_strs) + ")"
        return self._send_cmd(cmd)

    def get_tray_point(self, tray_index: int, row: int, col: int) -> str:
        """
        GetTrayPoint获取托盘点（立即指令）        
        Args:
            tray_index: 托盘编号
            row: 行号
            col: 列号
        """
        return self._send_cmd(f"GetTrayPoint({tray_index},{row},{col})")

    # ==================== 日志导出 ====================

    def log_export_usb(self) -> str:
        """LogExportUSB将机器人日志导出至U盘（立即指令）"""
        return self._send_cmd("LogExportUSB()")

    def get_export_status(self) -> str:
        """GetExportStatus获取日志导出状态（立即指令）"""
        return self._send_cmd("GetExportStatus()")

    # ==================== 原有接口保持兼容 ====================

    def kinematics_forward(self, joints: Tuple[float, ...]) -> str:
        """正运动学计算（兼容旧接口，建议使用positive_kin）"""
        return self.positive_kin(joints)

    def kinematics_inverse(self, pose: Tuple[float, ...]) -> str:
        """逆运动学计算（兼容旧接口，建议使用inverse_kin）"""
        return self.inverse_kin(pose)

    def is_in_drag_teach(self) -> str:
        """查询是否在拖动示教模式"""
        return self._send_cmd("IsInDragTeach()")

    def get_run_mode(self) -> str:
        """获取运行模式"""
        return self._send_cmd("GetRunMode()")

    def get_error_data(self) -> str:
        """获取错误数据"""
        return self._send_cmd("GetErrorData()")

    def get_log_state(self) -> str:
        """获取日志状态"""
        return self._send_cmd("GetLogState()")

    def self_collision_check(self, joints: Tuple[float, ...]) -> str:
        """自碰撞检测"""
        if len(joints) != 6:
            raise ValueError(f"需要6个关节角度")
        joint_str = ",".join([f"{j:.6f}" for j in joints])
        return self._send_cmd(f"SelfCollisionCheck({joint_str})")

    def orthogonal_move_check(self, pose: Tuple[float, ...]) -> str:
        """垂直移动检测"""
        if len(pose) != 6:
            raise ValueError(f"需要6个位姿参数")
        pose_str = ",".join([f"{p:.6f}" for p in pose])
        return self._send_cmd(f"OrthogonalMoveCheck({pose_str})")

    def angle_limit_check(self, joints: Tuple[float, ...]) -> str:
        """角度限位检测"""
        if len(joints) != 6:
            raise ValueError(f"需要6个关节角度")
        joint_str = ",".join([f"{j:.6f}" for j in joints])
        return self._send_cmd(f"AngleLimitCheck({joint_str})")

    def joint_limit_check(self, joints: Tuple[float, ...]) -> str:
        """关节限位检测"""
        if len(joints) != 6:
            raise ValueError(f"需要6个关节角度")
        joint_str = ",".join([f"{j:.6f}" for j in joints])
        return self._send_cmd(f"JointLimitCheck({joint_str})")

    def workspace_check(self, pose: Tuple[float, ...]) -> str:
        """工作空间检测"""
        if len(pose) != 6:
            raise ValueError(f"需要6个位姿参数")
        pose_str = ",".join([f"{p:.6f}" for p in pose])
        return self._send_cmd(f"WorkspaceCheck({pose_str})")

    def singularity_check(self, joints: Tuple[float, ...]) -> str:
        """奇异点检测"""
        if len(joints) != 6:
            raise ValueError(f"需要6个关节角度")
        joint_str = ",".join([f"{j:.6f}" for j in joints])
        return self._send_cmd(f"SingularityCheck({joint_str})")
