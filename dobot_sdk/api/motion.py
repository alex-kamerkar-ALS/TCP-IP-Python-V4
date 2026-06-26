# Copyright (c) 2026 Dobot
# Licensed under the MIT License

"""运动相关模块 - 所有运动指令、轨迹控制"""

from typing import Sequence
from enum import IntEnum
from ..core.connection import DobotConnection


class CoordinateType(IntEnum):
    """坐标系类型枚举"""
    CARTESIAN = 0  # 笛卡尔坐标
    JOINT = 1      # 关节角度


class Motion:
    """运动模块 - 处理所有运动相关指令"""
    
    def __init__(self, connection: DobotConnection):
        self.connection = connection
    
    def _fmt_pose(self, pose: Sequence[float], coord_type: CoordinateType) -> str:
        """格式化位姿为 joint={...} 或 pose={...}"""
        if len(pose) != 6:
            raise ValueError(f"位姿需要6个参数，实际{len(pose)}个")
        
        values = ",".join([f"{v:.6f}" for v in pose])
        if coord_type == CoordinateType.JOINT:
            return f"joint={{{values}}}"
        else:
            return f"pose={{{values}}}"
    
    def _send_cmd(self, command: str) -> str:
        """发送命令并接收响应"""
        return self.connection.send_receive_text(command)
    
    # ==================== 基础运动 ====================
    
    def movj(self, pose: Sequence[float], 
             coord_type: CoordinateType,
             user: int = -1, tool: int = -1,
             a: int = -1, v: int = -1, cp: int = -1) -> str:
        """
        MovJ关节运动（队列指令）
        
        Args:
            pose: 6个坐标值[x,y,z,rx,ry,rz] 或[j1,j2,j3,j4,j5,j6]
            coord_type: 坐标系类型(CoordinateType.CARTESIAN 或 CoordinateType.JOINT)
            user: 用户坐标系编号(0-50, -1表示使用当前)
            tool: 工具坐标系编号(0-50, -1表示使用当前)
            a: 加速度比例 (1-100, -1表示使用全局)
            v: 速度比例 (1-100, -1表示使用全局)
            cp: 平滑过渡比例 (0-100, -1表示不使用)

        Returns:
            str: ErrorID,{ResultID},MovJ(...);
        """
        pose_str = self._fmt_pose(pose, coord_type)
        
        params = [pose_str]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if v != -1:
            params.append(f"v={v}")
        if cp != -1:
            params.append(f"cp={cp}")
        
        cmd = f"MovJ({','.join(params)})"
        return self._send_cmd(cmd)
    
    def movl(self, pose: Sequence[float],
             coord_type: CoordinateType,
             user: int = -1, tool: int = -1,
             a: int = -1, v: int = -1, speed: int = -1,
             cp: int = -1, r: int = -1) -> str:
        """
        MovL直线运动（队列指令）
        
        Args:
            pose: 6个笛卡尔坐标 [x,y,z,rx,ry,rz]
            coord_type: 坐标系类型(必须指定)
            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100), 与speed互斥
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥

        Returns:
            str: ErrorID,{ResultID},MovL(...);
        """
        pose_str = self._fmt_pose(pose, coord_type)
        
        params = [pose_str]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if speed != -1:
            params.append(f"speed={speed}")
        elif v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        elif cp != -1:
            params.append(f"cp={cp}")
        
        cmd = f"MovL({','.join(params)})"
        return self._send_cmd(cmd)
    
    def movl_io(self, pose: Sequence[float], do_index: int, do_status: int,
                coord_type: CoordinateType,
                user: int = -1, tool: int = -1,
                a: int = -1, v: int = -1, speed: int = -1,
                cp: int = -1, r: int = -1) -> str:
        """
        MovLIO直线运动并输出DO（队列指令）
        
        Args:
            pose: 6个笛卡尔坐标 [x,y,z,rx,ry,rz]
            do_index: DO端口索引
            do_status: DO输出状态(0/1)
            coord_type: 坐标系类型            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100), 与speed互斥
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥

        Returns:
            str: ErrorID,{ResultID},MovLIO(...);
        """
        pose_str = self._fmt_pose(pose, coord_type)
        
        params = [pose_str, str(do_index), str(do_status)]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if speed != -1:
            params.append(f"speed={speed}")
        elif v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        elif cp != -1:
            params.append(f"cp={cp}")
        
        cmd = f"MovLIO({','.join(params)})"
        return self._send_cmd(cmd)
    
    def movj_io(self, pose: Sequence[float], do_index: int, do_status: int,
                coord_type: CoordinateType,
                user: int = -1, tool: int = -1,
                a: int = -1, v: int = -1, cp: int = -1) -> str:
        """
        MovJIO关节运动并输出DO（队列指令）
        
        Args:
            pose: 6个坐标值[x,y,z,rx,ry,rz] 或[j1,j2,j3,j4,j5,j6]
            do_index: DO端口索引
            do_status: DO输出状态(0/1)
            coord_type: 坐标系类型            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100)
            cp: 平滑过渡比例 (0-100)

        Returns:
            str: ErrorID,{ResultID},MovJIO(...);
        """
        pose_str = self._fmt_pose(pose, coord_type)
        
        params = [pose_str, str(do_index), str(do_status)]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if v != -1:
            params.append(f"v={v}")
        if cp != -1:
            params.append(f"cp={cp}")
        
        cmd = f"MovJIO({','.join(params)})"
        return self._send_cmd(cmd)
    
    def arc(self, p1: Sequence[float], p2: Sequence[float],
            coord_type: CoordinateType,
            user: int = -1, tool: int = -1,
            a: int = -1, v: int = -1, speed: int = -1,
            cp: int = -1, r: int = -1, mode: int = 0) -> str:
        """
        Arc圆弧插补运动（队列指令）
        
        Args:
            p1: 圆弧中间点            p2: 目标点位姿            coord_type: 坐标系类型            user: 用户坐标系编号(0-50, -1表示使用当前)
            tool: 工具坐标系编号(0-50, -1表示使用当前)
            a: 加速度比例 (1-100, -1表示使用全局)
            v: 速度比例 (1-100, -1表示使用全局)
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥
            mode: 姿态控制模式(0-线性 1-过中间点, 2-固定)

        Returns:
            str: ErrorID,{ResultID},Arc(...);
        """
        if len(p1) != 6 or len(p2) != 6:
            raise ValueError(f"位姿需要6个参数")
        
        if coord_type == CoordinateType.JOINT:
            p1_str = f"joint={{{','.join([f'{v:.6f}' for v in p1])}}}"
            p2_str = f"joint={{{','.join([f'{v:.6f}' for v in p2])}}}"
        else:
            p1_str = f"pose={{{','.join([f'{v:.6f}' for v in p1])}}}"
            p2_str = f"pose={{{','.join([f'{v:.6f}' for v in p2])}}}"
        
        params = [p1_str, p2_str]
        
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if speed != -1:
            params.append(f"speed={speed}")
        elif v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        elif cp != -1:
            params.append(f"cp={cp}")
        if mode != 0:
            params.append(f"mode={mode}")
        
        cmd = f"Arc({','.join(params)})"
        return self._send_cmd(cmd)
    
    def arc_io(self, p1: Sequence[float], p2: Sequence[float],
               do_index: int, do_status: int,
               coord_type: CoordinateType,
               user: int = -1, tool: int = -1,
               a: int = -1, v: int = -1, speed: int = -1,
               cp: int = -1, r: int = -1, mode: int = 0) -> str:
        """
        ArcIO圆弧运动并输出DO（队列指令）
        
        Args:
            p1: 圆弧中间点            p2: 目标点位姿            do_index: DO端口索引
            do_status: DO输出状态(0/1)
            coord_type: 坐标系类型            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100)
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥
            mode: 姿态控制模式(0-2)

        Returns:
            str: ErrorID,{ResultID},ArcIO(...);
        """
        if len(p1) != 6 or len(p2) != 6:
            raise ValueError(f"位姿需要6个参数")
        
        if coord_type == CoordinateType.JOINT:
            p1_str = f"joint={{{','.join([f'{v:.6f}' for v in p1])}}}"
            p2_str = f"joint={{{','.join([f'{v:.6f}' for v in p2])}}}"
        else:
            p1_str = f"pose={{{','.join([f'{v:.6f}' for v in p1])}}}"
            p2_str = f"pose={{{','.join([f'{v:.6f}' for v in p2])}}}"
        
        params = [p1_str, p2_str, str(do_index), str(do_status)]
        
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if speed != -1:
            params.append(f"speed={speed}")
        elif v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        elif cp != -1:
            params.append(f"cp={cp}")
        if mode != 0:
            params.append(f"mode={mode}")
        
        cmd = f"ArcIO({','.join(params)})"
        return self._send_cmd(cmd)
    
    def circle(self, p1: Sequence[float], p2: Sequence[float],
               count: int, coord_type: CoordinateType,
               user: int = -1, tool: int = -1,
               a: int = -1, v: int = -1, speed: int = -1,
               cp: int = -1, r: int = -1, mode: int = 0) -> str:
        """
        Circle整圆插补运动（队列指令）
        
        Args:
            p1: 整圆中间点位姿            p2: 整圆结束点位姿（应与起点相同）            count: 圈数 (1-999)
            coord_type: 坐标系类型            user: 用户坐标系编号(0-50)
            tool: 工具坐标系编号(0-50)
            a: 加速度比例 (1-100)
            v: 速度比例 (1-100)
            speed: 目标速度 (mm/s), 与v互斥
            cp: 平滑过渡比例 (0-100), 与r互斥
            r: 平滑过渡半径 (mm), 与cp互斥
            mode: 姿态控制模式(0-2)

        Returns:
            str: ErrorID,{ResultID},Circle(...);
        """
        if not 1 <= count <= 999:
            raise ValueError(f"圈数必须在1-999之间")
        
        if len(p1) != 6 or len(p2) != 6:
            raise ValueError(f"位姿需要6个参数")
        
        if coord_type == CoordinateType.JOINT:
            p1_str = f"joint={{{','.join([f'{v:.6f}' for v in p1])}}}"
            p2_str = f"joint={{{','.join([f'{v:.6f}' for v in p2])}}}"
        else:
            p1_str = f"pose={{{','.join([f'{v:.6f}' for v in p1])}}}"
            p2_str = f"pose={{{','.join([f'{v:.6f}' for v in p2])}}}"
        
        params = [p1_str, p2_str, str(count)]
        
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        if a != -1:
            params.append(f"a={a}")
        if speed != -1:
            params.append(f"speed={speed}")
        elif v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        elif cp != -1:
            params.append(f"cp={cp}")
        if mode != 0:
            params.append(f"mode={mode}")
        
        cmd = f"Circle({','.join(params)})"
        return self._send_cmd(cmd)
    
    # ==================== 伺服运动 ====================
    
    def servo_j(self, joints: Sequence[float],
                t: float = 0.1, aheadtime: float = 50.0, gain: float = 500.0) -> str:
        """
        ServoJ基于关节空间的动态跟随命令（队列指令）        
        Args:
            joints: 6个关节角度 [j1,j2,j3,j4,j5,j6]
            t: 运行时间 (秒) 0.004-3600.0
            aheadtime: 提前量(20.0-100.0), 类似PID的D参数
            gain: 比例增益 (200.0-1000.0), 类似PID的P参数
        Returns:
            str: ErrorID,{ResultID},ServoJ(...);
        """
        if len(joints) != 6:
            raise ValueError("joints需要6个关节角度")
        if not 0.004 <= t <= 3600.0:
            raise ValueError(f"t必须在0.004-3600.0之间")
        if not 20.0 <= aheadtime <= 100.0:
            raise ValueError(f"aheadtime必须在20.0-100.0之间")
        if not 200.0 <= gain <= 1000.0:
            raise ValueError(f"gain必须在200.0-1000.0之间")
        
        cmd = f"ServoJ({joints[0]:.6f},{joints[1]:.6f},{joints[2]:.6f},{joints[3]:.6f},{joints[4]:.6f},{joints[5]:.6f},t={t:.3f},aheadtime={aheadtime:.1f},gain={gain:.1f})"
        return self._send_cmd(cmd)
    
    def servo_p(self, pose: Sequence[float],
                t: float = 0.1, aheadtime: float = 50.0, gain: float = 500.0) -> str:
        """
        ServoP基于笛卡尔空间的动态跟随命令（队列指令）        
        Args:
            pose: 笛卡尔位姿 [x,y,z,rx,ry,rz]
            t: 运行时间 (秒) 0.004-3600.0
            aheadtime: 提前量(20.0-100.0)
            gain: 比例增益 (200.0-1000.0)

        Returns:
            str: ErrorID,{ResultID},ServoP(...);
        """
        if len(pose) != 6:
            raise ValueError("pose需要6个笛卡尔位姿参数")
        if not 0.004 <= t <= 3600.0:
            raise ValueError(f"t必须在0.004-3600.0之间")
        if not 20.0 <= aheadtime <= 100.0:
            raise ValueError(f"aheadtime必须在20.0-100.0之间")
        if not 200.0 <= gain <= 1000.0:
            raise ValueError(f"gain必须在200.0-1000.0之间")
        
        cmd = f"ServoP({pose[0]:.6f},{pose[1]:.6f},{pose[2]:.6f},{pose[3]:.6f},{pose[4]:.6f},{pose[5]:.6f},t={t:.3f},aheadtime={aheadtime:.1f},gain={gain:.1f})"
        return self._send_cmd(cmd)
    
    # ==================== 点动 ====================
    
    def move_jog(self, axis: str = "", coord_type: CoordinateType = CoordinateType.JOINT,
                 user: int = 0, tool: int = 0) -> str:
        """
        MoveJog点动机械臂（立即指令)        
        Args:
            axis: "X+", "X-", "J1+" 等，空字符串停止
            coord_type: 坐标系类型(默认JOINT)
            user: 用户坐标系编号            tool: 工具坐标系编号
        Returns:
            str: ErrorID,{},MoveJog(...);
        """
        if axis:
            cmd = f"MoveJog({axis},coordtype={int(coord_type)},user={user},tool={tool})"
        else:
            cmd = "MoveJog()"
        
        return self._send_cmd(cmd)
    
    # ==================== 运动至点位====================
    
    def run_to(self, point_name: str, user: int = -1, tool: int = -1) -> str:
        """
        RunTo运动至指定点位（立即指令)        
        Args:
            point_name: 点位名称
            user: 用户坐标系编号(0-50, -1表示使用当前)
            tool: 工具坐标系编号(0-50, -1表示使用当前)

        Returns:
            str: ErrorID,{ResultID},RunTo(...);
        """
        params = [f"\"{point_name}\""]
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        
        cmd = f"RunTo({','.join(params)})"
        return self._send_cmd(cmd)
    
    # ==================== 轨迹复现 ====================
    
    def get_start_pose(self, trace_name: str, path_type: int = 1) -> str:
        """
        GetStartPose获取指定轨迹的第一个点位（立即指令)        
        Args:
            trace_name: 轨迹文件名（含后缀.csv）            path_type: 轨迹类型 (1-用于复现的轨迹 2-用于拟合的轨迹，默认为1)

        Returns:
            str: ErrorID,{X,Y,Z,Rx,Ry,Rz},GetStartPose(traceName,pathType);
        """
        if path_type not in [1, 2]:
            raise ValueError("path_type 必须是1 或 2")
        
        cmd = f"GetStartPose(\"{trace_name}\",{path_type})"
        return self._send_cmd(cmd)
    
    def movs(self, trace_name: str, is_const: int = 0, 
             multi: float = 1.0, sample: int = 50,
             freq: float = 0.2, user: int = -1, tool: int = -1) -> str:
        """
        MovS拟合导入的轨迹（队列指令)        
        Args:
            trace_name: 轨迹文件名（含后缀）            is_const: 是否匀速复现(0-原始 1-匀速)
            multi: 速度倍数 (仅is_const=0时有意义 范围0.25-2)
            sample: 采样间隔 (ms, 范围8-1000)
            freq: 滤波系数 (范围0-1, 1表示关闭滤波)
            user: 用户坐标系索引(0-50, -1表示使用当前)
            tool: 工具坐标系索引(0-50, -1表示使用当前)

        Returns:
            str: ErrorID,{ResultID},MovS(...);
        """
        params = [f"\"{trace_name}\""]
        params.append(f"isConst={is_const}")
        params.append(f"multi={multi}")
        params.append(f"sample={sample}")
        params.append(f"freq={freq}")
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        
        cmd = f"MovS({','.join(params)})"
        return self._send_cmd(cmd)
    
    def start_path(self, trace_name: str, is_const: int = 0, 
                   multi: float = 1.0, sample: int = 50,
                   freq: float = 0.2, user: int = -1, tool: int = -1) -> str:
        """
        StartPath复现录制的运动轨迹（队列指令)        
        Args:
            trace_name: 轨迹文件名（含后缀）            is_const: 是否匀速复现(0-原始 1-匀速)
            multi: 速度倍数 (仅is_const=0时有意义 范围0.25-2)
            sample: 采样间隔 (ms, 范围8-1000)
            freq: 滤波系数 (范围0-1, 1表示关闭滤波)
            user: 用户坐标系索引(0-50, -1表示使用当前)
            tool: 工具坐标系索引(0-50, -1表示使用当前)

        Returns:
            str: ErrorID,{ResultID},StartPath(...);
        """
        params = [f"\"{trace_name}\""]
        params.append(f"isConst={is_const}")
        params.append(f"multi={multi}")
        params.append(f"sample={sample}")
        params.append(f"freq={freq}")
        if user != -1:
            params.append(f"user={user}")
        if tool != -1:
            params.append(f"tool={tool}")
        
        cmd = f"StartPath({','.join(params)})"
        return self._send_cmd(cmd)
    
    # ==================== 相对运动 ====================
    
    def rel_movj_tool(self, offset: Sequence[float], v: int = -1) -> str:
        """
        RelMovJTool沿工具坐标系进行相对关节运动（队列指令）
        
        Args:
            offset: 6个关节偏移量 [j1,j2,j3,j4,j5,j6]
            v: 速度比例 (1-100, -1表示使用全局)

        Returns:
            str: ErrorID,{ResultID},RelMovJTool(...);
        """
        if len(offset) != 6:
            raise ValueError(f"偏移量需要6个参数")
        
        offset_str = "{" + ",".join([f"{v:.6f}" for v in offset]) + "}"
        params = [offset_str]
        if v != -1:
            params.append(f"v={v}")
        
        cmd = f"RelMovJTool({','.join(params)})"
        return self._send_cmd(cmd)
    
    def rel_movl_tool(self, offset: Sequence[float], v: int = -1, r: int = -1) -> str:
        """
        RelMovLTool沿工具坐标系进行相对直线运动（队列指令）
        
        Args:
            offset: 笛卡尔空间偏移量 [x,y,z,rx,ry,rz]
            v: 速度比例 (1-100, -1表示使用全局)
            r: 过渡半径 (mm)

        Returns:
            str: ErrorID,{ResultID},RelMovLTool(...);
        """
        if len(offset) != 6:
            raise ValueError(f"偏移量需要6个参数")
        
        offset_str = "{" + ",".join([f"{v:.6f}" for v in offset]) + "}"
        params = [offset_str]
        if v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        
        cmd = f"RelMovLTool({','.join(params)})"
        return self._send_cmd(cmd)
    
    def rel_movj_user(self, offset: Sequence[float], v: int = -1) -> str:
        """
        RelMovJUser沿用户坐标系进行相对关节运动（队列指令）
        
        Args:
            offset: 6个关节偏移量 [j1,j2,j3,j4,j5,j6]
            v: 速度比例 (1-100, -1表示使用全局)

        Returns:
            str: ErrorID,{ResultID},RelMovJUser(...);
        """
        if len(offset) != 6:
            raise ValueError(f"偏移量需要6个参数")
        
        offset_str = "{" + ",".join([f"{v:.6f}" for v in offset]) + "}"
        params = [offset_str]
        if v != -1:
            params.append(f"v={v}")
        
        cmd = f"RelMovJUser({','.join(params)})"
        return self._send_cmd(cmd)
    
    def rel_movl_user(self, offset: Sequence[float], v: int = -1, r: int = -1) -> str:
        """
        RelMovLUser沿用户坐标系进行相对直线运动（队列指令）
        
        Args:
            offset: 笛卡尔空间偏移量 [x,y,z,rx,ry,rz]
            v: 速度比例 (1-100, -1表示使用全局)
            r: 过渡半径 (mm)

        Returns:
            str: ErrorID,{ResultID},RelMovLUser(...);
        """
        if len(offset) != 6:
            raise ValueError(f"偏移量需要6个参数")
        
        offset_str = "{" + ",".join([f"{v:.6f}" for v in offset]) + "}"
        params = [offset_str]
        if v != -1:
            params.append(f"v={v}")
        if r != -1:
            params.append(f"r={r}")
        
        cmd = f"RelMovLUser({','.join(params)})"
        return self._send_cmd(cmd)
    
    def rel_joint_movj(self, offset: Sequence[float], v: int = -1) -> str:
        """
        RelJointMovJ沿关节坐标系进行相对关节运动（队列指令）
        
        Args:
            offset: 6个关节偏移量 [j1,j2,j3,j4,j5,j6]
            v: 速度比例 (1-100, -1表示使用全局)

        Returns:
            str: ErrorID,{ResultID},RelJointMovJ(...);
        """
        if len(offset) != 6:
            raise ValueError(f"偏移量需要6个参数")
        
        offset_str = ",".join([f"{v:.6f}" for v in offset])
        params = [offset_str]
        if v != -1:
            params.append(f"v={v}")
        
        cmd = f"RelJointMovJ({','.join(params)})"
        return self._send_cmd(cmd)

    def rel_movl(self, offset: Sequence[float], v: int = -1, r: int = -1) -> str:
        """
        rel_movl沿工具坐标系进行相对直线运动（队列指令）- 别名方法
        
        Args:
            offset: 笛卡尔空间偏移量 [x,y,z,rx,ry,rz]
            v: 速度比例 (1-100, -1表示使用全局)
            r: 平滑过渡半径 (mm, -1表示使用全局)

        Returns:
            str: ErrorID,{ResultID},RelMovLTool(...);
        """
        return self.rel_movl_tool(offset, v, r)
    
    def rel_point_tool(self, index: int) -> str:
        """
        RelPointTool沿工具坐标系笛卡尔点偏移（立即指令）
        
        Args:
            index: 点位索引

        Returns:
            str: ErrorID,{X,Y,Z,Rx,Ry,Rz},RelPointTool(index);
        """
        return self._send_cmd(f"RelPointTool({index})")
    
    def rel_point_user(self, index: int) -> str:
        """
        RelPointUser沿用户坐标系笛卡尔点偏移（立即指令）
        
        Args:
            index: 点位索引

        Returns:
            str: ErrorID,{X,Y,Z,Rx,Ry,Rz},RelPointUser(index);
        """
        return self._send_cmd(f"RelPointUser({index})")
    
    def rel_joint(self, index: int) -> str:
        """
        RelJoint关节点位偏移（立即指令）
        
        Args:
            index: 关节点位索引

        Returns:
            str: ErrorID,{J1,J2,J3,J4,J5,J6},RelJoint(index);
        """
        return self._send_cmd(f"RelJoint({index})")
    
    # ==================== 指令ID查询 ====================
    
    def get_current_command_id(self) -> str:
        """
        GetCurrentCommandID获取当前执行指令的算法队列ID（立即指令）
        
        Returns:
            str: ErrorID,{ResultID},GetCurrentCommandID();
        """
        return self._send_cmd("GetCurrentCommandID()")
    
    # ==================== 坐标系偏移====================
    
    def start_rt_offset(self, offset: Sequence[float]) -> str:
        """
        StartRTOffset启动坐标系偏移（队列指令）        
        Args:
            offset: 偏移量 [x,y,z,rx,ry,rz]
        Returns:
            str: ErrorID,{ResultID},StartRTOffset(...);
        """
        if len(offset) != 6:
            raise ValueError("offset需要6个参数")
        cmd = f"StartRTOffset({offset[0]:.6f},{offset[1]:.6f},{offset[2]:.6f},{offset[3]:.6f},{offset[4]:.6f},{offset[5]:.6f})"
        return self._send_cmd(cmd)
    
    def end_rt_offset(self) -> str:
        """
        EndRTOffset结束坐标系偏移（队列指令)        
        Returns:
            str: ErrorID,{ResultID},EndRTOffset();
        """
        return self._send_cmd("EndRTOffset()")
    
    def offset_para(self, freq: float = 0.2) -> str:
        """
        OffsetPara设置坐标系偏移值（立即指令)        
        Args:
            freq: 滤波系数 (0-1)

        Returns:
            str: ErrorID,{},OffsetPara(freq);
        """
        return self._send_cmd(f"OffsetPara({freq:.2f})")
    
    # ==================== 轨迹恢复 ====================
    
    def set_resume_offset(self, distance: float) -> str:
        """
        SetResumeOffset设置轨迹恢复的回退距离（立即指令）
        
        Args:
            distance: 回退距离 (mm)

        Returns:
            str: ErrorID,{},SetResumeOffset(distance);
        """
        return self._send_cmd(f"SetResumeOffset({distance:.6f})")
    
    def path_recovery(self) -> str:
        """
        PathRecovery开始轨迹恢复（立即指令)        
        Returns:
            str: ErrorID,{},PathRecovery();
        """
        return self._send_cmd("PathRecovery()")
    
    def path_recovery_stop(self) -> str:
        """
        PathRecoveryStop轨迹恢复过程中停止机器人（立即指令）
        
        Returns:
            str: ErrorID,{},PathRecoveryStop();
        """
        return self._send_cmd("PathRecoveryStop()")
    
    def path_recovery_status(self) -> str:
        """
        PathRecoveryStatus查询轨迹恢复状态（立即指令)        
        Returns:
            str: ErrorID,{status},PathRecoveryStatus();
                 status: 0-已回到暂停位置 1-偏差较小, 2-偏差较大
        """
        return self._send_cmd("PathRecoveryStatus()")
    

    
    def init_pose(self) -> str:
        """
        InitPose回到初始位置（队列指令）
        
        Returns:
            str: ErrorID,{ResultID},InitPose();
        """
        return self._send_cmd("InitPose()")
    
    def stop(self) -> str:
        """
        Stop停止运动（立即指令）
        
        Returns:
            str: ErrorID,{},Stop();
        """
        return self._send_cmd("Stop()")
    
    def pause(self) -> str:
        """
        Pause暂停运动（立即指令）
        
        Returns:
            str: ErrorID,{},Pause();
        """
        return self._send_cmd("Pause()")
    
    def continue_motion(self) -> str:
        """
        Continue继续运动（立即指令）
        
        Returns:
            str: ErrorID,{},Continue();
        """
        return self._send_cmd("Continue()")
    
    # ==================== 速度加速度设置 ====================
    
    def speed_factor(self, speed: int) -> str:
        """
        SpeedFactor设置全局速度比例（立即指令）
        
        Args:
            speed: 速度比例 (0-100)

        Returns:
            str: ErrorID,{},SpeedFactor(speed);
        """
        if not 0 <= speed <= 100:
            raise ValueError(f"速度必须在0-100之间，当前值 {speed}")
        return self._send_cmd(f"SpeedFactor({speed})")
    
    def j_speed_factor(self, joint: int, speed: int) -> str:
        """
        JSpeedFactor设置关节速度比例（立即指令）
        
        Args:
            joint: 关节编号 (1-6)
            speed: 速度比例 (0-100)

        Returns:
            str: ErrorID,{},JSpeedFactor(joint,speed);
        """
        if not 1 <= joint <= 6:
            raise ValueError(f"关节编号必须在1-6之间")
        if not 0 <= speed <= 100:
            raise ValueError(f"速度必须在0-100之间")
        return self._send_cmd(f"JSpeedFactor({joint},{speed})")
    
    def l_speed_factor(self, speed: int) -> str:
        """
        LSpeedFactor设置直线速度比例（立即指令）
        
        Args:
            speed: 速度比例 (0-100)

        Returns:
            str: ErrorID,{},LSpeedFactor(speed);
        """
        if not 0 <= speed <= 100:
            raise ValueError(f"速度必须在0-100之间")
        return self._send_cmd(f"LSpeedFactor({speed})")
    
    def acc_j(self, joint: int, acc: int) -> str:
        """
        AccJ设置关节加速度比例（立即指令）
        
        Args:
            joint: 关节编号 (1-6)
            acc: 加速度比例 (0-100)

        Returns:
            str: ErrorID,{},AccJ(joint,acc);
        """
        if not 1 <= joint <= 6:
            raise ValueError(f"关节编号必须在1-6之间")
        if not 0 <= acc <= 100:
            raise ValueError(f"加速度必须在0-100之间")
        return self._send_cmd(f"AccJ({joint},{acc})")
    
    def acc_l(self, acc: int) -> str:
        """
        AccL设置直线加速度比例（立即指令）
        
        Args:
            acc: 加速度比例 (0-100)

        Returns:
            str: ErrorID,{},AccL(acc);
        """
        if not 0 <= acc <= 100:
            raise ValueError(f"加速度必须在0-100之间")
        return self._send_cmd(f"AccL({acc})")
    
    # ==================== 坐标系/负载设置====================
    
    def set_work_load(self, index: int, weight: float, 
                      center: Sequence[float]) -> str:
        """
        SetWorkLoad设置负载参数（立即指令）
        
        Args:
            index: 负载编号 (0-9)
            weight: 负载重量 (kg)
            center: 负载重心坐标 [x,y,z] (mm)

        Returns:
            str: ErrorID,{},SetWorkLoad(...);
        """
        if not 0 <= index <= 9:
            raise ValueError(f"负载编号必须在0-9之间")
        if len(center) != 3:
            raise ValueError("center需要3个参数[x,y,z]")
        return self._send_cmd(
            f"SetWorkLoad({index},{weight:.6f},{{{center[0]:.6f},{center[1]:.6f},{center[2]:.6f}}})"
        )
    
    def set_collision_level(self, level: int) -> str:
        """
        SetCollisionLevel设置碰撞检测等级（立即指令)        
        Args:
            level: 碰撞等级 (0-5, 0为关闭)

        Returns:
            str: ErrorID,{},SetCollisionLevel(level);
        """
        if not 0 <= level <= 5:
            raise ValueError(f"碰撞等级必须在0-5之间")
        return self._send_cmd(f"SetCollisionLevel({level})")
    
    # ==================== 模式设置 ====================
    
    def set_run_mode(self, mode: int) -> str:
        """
        RunMode设置运行模式（立即指令）
        
        Args:
            mode: 0-拖动示教, 1-正常运行, 2-模拟运行, 3-空载示教,
                  4-力控拖动, 5-协作示教, 6-绝对拖动, 7-相对拖动

        Returns:
            str: ErrorID,{},RunMode(mode);
        """
        if mode not in [0, 1, 2, 3, 4, 5, 6, 7]:
            raise ValueError(f"无效的运行模式 {mode}")
        return self._send_cmd(f"RunMode({mode})")
    
    def drag_teach_switch(self, status: int) -> str:
        """
        DragTeachSwitch开启关闭拖动示教（立即指令）
        
        Args:
            status: 0-关闭, 1-开启
        Returns:
            str: ErrorID,{},DragTeachSwitch(status);
        """
        if status not in [0, 1]:
            raise ValueError(f"状态必须是0或1")
        return self._send_cmd(f"DragTeachSwitch({status})")
    
    # ==================== 抱闸控制 ====================
    
    def brake_control(self, axis: int, status: int) -> str:
        """
        BrakeControl抱闸控制（立即指令）
        
        Args:
            axis: 轴编号(1-6)
            status: 0-松开, 1-抱紧

        Returns:
            str: ErrorID,{},BrakeControl(axis,status);
        """
        if not 1 <= axis <= 6:
            raise ValueError(f"轴编号必须在1-6之间")
        if status not in [0, 1]:
            raise ValueError(f"状态必须是0或1")
        return self._send_cmd(f"BrakeControl({axis},{status})")
    
    # ==================== 末端控制 ====================
    
    def tool_voltage(self, voltage: int) -> str:
        """
        ToolVoltage设置末端电压（立即指令）
        
        Args:
            voltage: 0-0V, 1-5V, 2-12V, 3-24V

        Returns:
            str: ErrorID,{},ToolVoltage(voltage);
        """
        if voltage not in [0, 1, 2, 3]:
            raise ValueError(f"电压值必须是0/1/2/3")
        return self._send_cmd(f"ToolVoltage({voltage})")
    

