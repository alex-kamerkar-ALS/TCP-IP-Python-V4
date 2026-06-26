# Copyright (c) 2026 Dobot
# Licensed under the MIT License

"""插件相关模块 - 力控、传送带等扩展功能"""

from typing import Sequence
from ..core.connection import DobotConnection


class Plugins:
    """插件模块 - 处理力控、传送带等扩展功能"""

    def __init__(self, connection: DobotConnection):
        self.connection = connection

    def _send_cmd(self, command: str) -> str:
        """发送命令并接收响应"""
        return self.connection.send_receive_text(command)

    # ==================== 力传感器基础指令 ====================

    def enable_ft_sensor(self, status: int) -> str:
        """
        EnableFTSensor开启关闭力传感器（立即指令）
        
        Args:
            status: 0-关闭, 1-开启        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"EnableFTSensor({status})")

    def six_force_home(self) -> str:
        """SixForceHome力传感器回零（立即指令）"""
        return self._send_cmd("SixForceHome()")

    def get_force(self, tool: int = -1) -> str:
        """
        GetForce获取力传感器数值（立即指令）        
        Args:
            tool: 工具坐标系编号(-1表示使用当前工具坐标系)
        """
        if tool == -1:
            return self._send_cmd("GetForce()")
        return self._send_cmd(f"GetForce({tool})")

    # ==================== 力控拖拽模式 ====================

    def force_drive_mode(self, status: int) -> str:
        """
        ForceDriveMode进入力控拖拽模式（立即指令）
        
        Args:
            status: 0-退出拖拽模式 1-进入拖拽模式
        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"ForceDriveMode({status})")

    def force_drive_speed(self, speed: int) -> str:
        """
        ForceDriveSpeed设置力控拖拽速度（立即指令）
        
        Args:
            speed: 力控拖拽速度比例 (0-100)
        """
        if not 0 <= speed <= 100:
            raise ValueError("速度比例必须在0-100之间")
        return self._send_cmd(f"ForceDriveSpeed({speed})")

    # ==================== 力控模式参数设置 ====================

    def fc_force_mode(self, pose: Sequence[float], force: Sequence[float],
                      reference: int = -1, user: int = -1, tool: int = -1) -> str:
        """
        FCForceMode以用户指定的参数开启力控（队列指令)        
        Args:
            pose: 6个方向的刚度系数 [x,y,z,rx,ry,rz]
            force: 6个方向的目标力[fx,fy,fz,frx,fry,frz]
            reference: 参考坐标系类型 (-1-工具坐标系 1-用户坐标系)
            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
        """
        if len(pose) != 6:
            raise ValueError("pose需要6个参数")
        if len(force) != 6:
            raise ValueError("force需要6个参数")
        pose_str = "{" + ",".join([f"{v}" for v in pose]) + "}"
        force_str = "{" + ",".join([f"{v}" for v in force]) + "}"
        params = [pose_str, force_str]
        if reference != -1:
            params.append(f"reference={reference}")
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        return self._send_cmd(f"FCForceMode({','.join(params)})")

    def fc_set_deviation(self, deviation: Sequence[float], control_type: int = -1) -> str:
        """
        FCSetDeviation设置力控模式下的位移和姿态偏差（立即指令）        
        Args:
            deviation: 6个方向的偏差 [x,y,z,rx,ry,rz]，位移单位mm，姿态单位度
            control_type: 控制类型 (-1表示默认)
        """
        if len(deviation) != 6:
            raise ValueError("偏差需要6个参数")
        dev_str = "{" + ",".join([f"{v}" for v in deviation]) + "}"
        if control_type == -1:
            return self._send_cmd(f"FCSetDeviation({dev_str})")
        return self._send_cmd(f"FCSetDeviation({dev_str},{control_type})")

    def fc_set_force_limit(self, x: float, y: float, z: float,
                           rx: float, ry: float, rz: float) -> str:
        """
        FCSetForceLimit设置最大力限制（立即指令）
        
        Args:
            x,y,z: 位移方向最大力限制 (N)
            rx,ry,rz: 姿态方向最大力限制 (N/m)
        """
        return self._send_cmd(f"FCSetForceLimit({x},{y},{z},{rx},{ry},{rz})")

    def fc_set_mass(self, x: float, y: float, z: float,
                    rx: float, ry: float, rz: float) -> str:
        """
        FCSetMass设置力控模式下各方向的惯性系数（立即指令）        
        Args:
            x,y,z: 位移方向惯性系数(kg)
            rx,ry,rz: 姿态方向惯性系数(kg·m²)
        """
        return self._send_cmd(f"FCSetMass({x},{y},{z},{rx},{ry},{rz})")

    def fc_set_stiffness(self, x: float, y: float, z: float,
                         rx: float, ry: float, rz: float) -> str:
        """
        FCSetStiffness设置力控模式下各方向的弹性系数（立即指令）        
        Args:
            x,y,z: 位移方向弹性系数(N/mm)
            rx,ry,rz: 姿态方向弹性系数(N/m·deg)
        """
        return self._send_cmd(f"FCSetStiffness({x},{y},{z},{rx},{ry},{rz})")

    def fc_set_damping(self, x: float, y: float, z: float,
                       rx: float, ry: float, rz: float) -> str:
        """
        FCSetDamping设置力控模式下各方向的阻尼系数（立即指令）        
        Args:
            x,y,z: 位移方向阻尼系数 (N·s/mm)
            rx,ry,rz: 姿态方向阻尼系数(N·s/m·deg)
        """
        return self._send_cmd(f"FCSetDamping({x},{y},{z},{rx},{ry},{rz})")

    def fc_off(self) -> str:
        """FCOff退出力控模式（队列指令）"""
        return self._send_cmd("FCOff()")

    def fc_set_force_speed_limit(self, x: float, y: float, z: float,
                                 rx: float, ry: float, rz: float) -> str:
        """
        FCSetForceSpeedLimit设置各方向的力控调节速度（立即指令）
        
        Args:
            x,y,z: 位移方向力控调节速度 (mm/s)
            rx,ry,rz: 姿态方向力控调节速度 (deg/s)
        """
        return self._send_cmd(f"FCSetForceSpeedLimit({x},{y},{z},{rx},{ry},{rz})")

    def fc_set_force(self, fx: float, fy: float, fz: float,
                     frx: float, fry: float, frz: float) -> str:
        """
        FCSetForce实时调整恒力设置（立即指令）
        
        Args:
            fx,fy,fz: 位移方向目标力(N)
            frx,fry,frz: 姿态方向目标力 (N/m)
        """
        return self._send_cmd(f"FCSetForce({fx},{fy},{fz},{frx},{fry},{frz})")

    # ==================== 力传感器碰撞检测（仅适用CRAF机型）====================

    def set_fc_collision(self, sensitivity: int, threshold: float) -> str:
        """
        SetFCCollision设置力传感器碰撞检测的阈值参数（仅适用CRAF机型，立即指令）
        
        Args:
            sensitivity: 碰撞检测灵敏度 (0-10)
            threshold: 碰撞检测阈值(N)
        """
        if not 0 <= sensitivity <= 10:
            raise ValueError("灵敏度必须在0-10之间")
        return self._send_cmd(f"SetFCCollision({sensitivity},{threshold})")

    def fc_collision_switch(self, status: int) -> str:
        """
        FCCollisionSwitch开启关闭力传感器碰撞检测开关（仅适用CRAF机型，立即指令）
        
        Args:
            status: 0-关闭碰撞检测 1-开启碰撞检测        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"FCCollisionSwitch({status})")

    # ==================== 传送带跟踪 ====================

    def cnv_init(self, index: int) -> str:
        """
        CnvInit开启传送带（立即指令）
        
        Args:
            index: 传送带索引 (0-1)
        """
        if index not in [0, 1]:
            raise ValueError("传送带索引必须在0-1之间")
        return self._send_cmd(f"CnvInit({index})")

    def get_cnv_object(self, obj_id: int) -> str:
        """
        GetCnvObject等待指定工件进入传送带的抓取区域（立即指令）        
        Args:
            obj_id: 工件类型，取值范围[0, 15]
                    0：不指定工件类型，获取最先进入队列的工件信息
        """
        if not 0 <= obj_id <= 15:
            raise ValueError("工件类型必须在0-15之间")
        return self._send_cmd(f"GetCnvObject({obj_id})")

    def start_sync_cnv(self) -> str:
        """StartSyncCnv开启传送带跟踪功能（立即指令）"""
        return self._send_cmd("StartSyncCnv()")

    def cnv_movl(self, pose: Sequence[float], user: int = -1, tool: int = -1,
                 a: int = -1, v: int = -1, speed: int = -1,
                 cp: int = -1, r: int = -1) -> str:
        """
        CnvMovL执行传送带跟随，采取直线轨迹插补（队列指令)        
        Args:
            pose: 6个笛卡尔坐标 [x,y,z,rx,ry,rz]
            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100), 与speed互斥
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥
        """
        if len(pose) != 6:
            raise ValueError("pose需要6个参数")
        pose_str = "{" + ",".join([f"{v:.6f}" for v in pose]) + "}"
        params = [pose_str]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if v != -1:
            params.append(f"v={v}")
        if speed != -1:
            params.append(f"speed={speed}")
        if cp != -1:
            params.append(f"cp={cp}")
        if r != -1:
            params.append(f"r={r}")
        return self._send_cmd(f"CnvMovL({','.join(params)})")

    def cnv_movc(self, pose: Sequence[float], via_pose: Sequence[float],
                 user: int = -1, tool: int = -1,
                 a: int = -1, v: int = -1, speed: int = -1,
                 cp: int = -1, r: int = -1) -> str:
        """
        CnvMovC执行传送带跟随，采取圆弧轨迹插补（队列指令)        
        Args:
            pose: 目标力个笛卡尔坐标 [x,y,z,rx,ry,rz]
            via_pose: 中间点个笛卡尔坐标 [x,y,z,rx,ry,rz]
            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100), 与speed互斥
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥
        """
        if len(pose) != 6:
            raise ValueError("pose需要6个参数")
        if len(via_pose) != 6:
            raise ValueError("via_pose需要6个参数")
        pose_str = "{" + ",".join([f"{v:.6f}" for v in pose]) + "}"
        via_str = "{" + ",".join([f"{v:.6f}" for v in via_pose]) + "}"
        params = [pose_str, via_str]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if v != -1:
            params.append(f"v={v}")
        if speed != -1:
            params.append(f"speed={speed}")
        if cp != -1:
            params.append(f"cp={cp}")
        if r != -1:
            params.append(f"r={r}")
        return self._send_cmd(f"CnvMovC({','.join(params)})")

    def stop_sync_cnv(self) -> str:
        """StopSyncCnv停止传送带跟踪功能（立即指令）"""
        return self._send_cmd("StopSyncCnv()")

    def set_cnv_point_offset(self, x_offset: float, y_offset: float) -> str:
        """
        SetCnvPointOffset设置传送带用户坐标系下X、Y方向的偏移量（立即指令）
        
        Args:
            x_offset: X方向偏移量(mm)
            y_offset: Y方向偏移量(mm)
        """
        return self._send_cmd(f"SetCnvPointOffset({x_offset},{y_offset})")

    def set_cnv_time_compensation(self, compensation: float) -> str:
        """
        SetCnvTimeCompensation设置补偿时间（立即指令）
        
        Args:
            compensation: 补偿时间 (ms)
        """
        return self._send_cmd(f"SetCnvTimeCompensation({compensation})")

    # ==================== 原有接口保持兼容（已废弃，建议使用新接口）====================

    def set_ft_sensor(self, status: int) -> str:
        """
        开启关闭力传感器（已废弃，建议使用enable_ft_sensor）        
        Args:
            status: 0-关闭, 1-开启        """
        return self.enable_ft_sensor(status)

    def zero_ft_sensor(self) -> str:
        """力传感器清零（已废弃，建议使用six_force_home）"""
        return self.six_force_home()

    def get_ft_sensor(self) -> str:
        """获取力传感器数据（已废弃，建议使用get_force）"""
        return self.get_force()

    # ==================== 拖动示教 ====================

    def set_drag_param(self, axis: int, kp: float, ki: float, kd: float) -> str:
        """
        设置拖动示教参数

        Args:
            axis: 轴编号(0-6)
            kp: 比例系数
            ki: 积分系数
            kd: 微分系数
        """
        if not 0 <= axis <= 6:
            raise ValueError("轴编号必须在0-6之间")
        return self._send_cmd(f"SetDragParam({axis},{kp:.4f},{ki:.4f},{kd:.4f})")

    def get_drag_param(self, axis: int) -> str:
        """
        获取拖动示教参数

        Args:
            axis: 轴编号(0-6)
        """
        if not 0 <= axis <= 6:
            raise ValueError("轴编号必须在0-6之间")
        return self._send_cmd(f"GetDragParam({axis})")

    # ==================== 视觉通信 ====================

    def vision_send(self, data: str) -> str:
        """
        发送视觉数据
        Args:
            data: 视觉数据字符串        """
        return self._send_cmd(f"VisionSend(\"{data}\")")

    def vision_recv(self) -> str:
        """接收视觉数据"""
        return self._send_cmd("VisionRecv()")
