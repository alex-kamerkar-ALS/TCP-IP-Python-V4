# Copyright (c) 2026 Dobot
# Licensed under the MIT License

"""IO相关模块 - 数字IO、模拟IO、末端IO控制"""

from typing import List, Union
from ..core.connection import DobotConnection


class IO:
    """IO模块 - 处理所有IO相关指令"""

    def __init__(self, connection: DobotConnection):
        self.connection = connection

    def _send_cmd(self, command: str) -> str:
        """发送命令并接收响应"""
        return self.connection.send_receive_text(command)

    # ==================== 数字输出端口 ====================

    def do(self, index: int, status: int) -> str:
        """
        设置数字输出端口状态（队列指令）
        Args:
            index: DO端口索引 (1-based)
            status: 状态(0=Off, 1=On)

        Returns:
            str: ErrorID,{ResultID},DO(index,status);
        """
        if status not in [0, 1]:
            raise ValueError("DO状态必须是0或1")
        return self._send_cmd(f"DO({index},{status})")

    def do_instant(self, index: int, status: int) -> str:
        """
        设置数字输出端口状态（立即指令）
        Args:
            index: DO端口索引 (1-based)
            status: 状态(0=Off, 1=On)

        Returns:
            str: ErrorID,{},DOInstant(index,status);
        """
        if status not in [0, 1]:
            raise ValueError("DO状态必须是0或1")
        return self._send_cmd(f"DOInstant({index},{status})")

    def get_do(self, index: int) -> str:
        """
        获取数字输出端口状态（立即指令）
        Args:
            index: DO端口索引 (1-based)

        Returns:
            str: ErrorID,{status},GetDO(index);
        """
        return self._send_cmd(f"GetDO({index})")

    def do_group(self, group_index: int, status: Union[List[int], str]) -> str:
        """
        设置多个数字输出端口状态（队列指令）
        Args:
            group_index: IO组索引(0-3)
            status: 端口状态列表，如[0,1,0,1] 或字符串 "{0,1,0,1}"

        Returns:
            str: ErrorID,{ResultID},DOGroup(groupIndex,status);
        """
        if isinstance(status, list):
            status_str = "{" + ",".join(str(s) for s in status) + "}"
        else:
            status_str = status
        
        return self._send_cmd(f"DOGroup({group_index},{status_str})")

    def do_group_dec(self, group_index: int, value: int) -> str:
        """
        通过赋值十进制设置多个数字输出端口状态（队列指令）
        Args:
            group_index: IO组索引(0-3)
            value: 十进制值
        Returns:
            str: ErrorID,{ResultID},DOGroupDEC(groupIndex,value);
        """
        return self._send_cmd(f"DOGroupDEC({group_index},{value})")

    # ==================== 别名方法（提高易用性）====================

    def do_on(self, index: int) -> str:
        """
        开启数字输出端口（队列指令）
        Args:
            index: DO端口索引 (1-based)
        Returns:
            str: ErrorID,{ResultID},DO(index,1);
        """
        return self.do(index, 1)

    def do_off(self, index: int) -> str:
        """
        关闭数字输出端口（队列指令）
        Args:
            index: DO端口索引 (1-based)
        Returns:
            str: ErrorID,{ResultID},DO(index,0);
        """
        return self.do(index, 0)

    def get_di(self, index: int) -> str:
        """
        获取DI端口的状态（立即指令）- 别名方法
        Args:
            index: DI端口索引 (1-based)
        Returns:
            str: ErrorID,{status},DI(index);
        """
        return self.di(index)

    def get_ai(self, index: int) -> str:
        """
        获取AI端口的值（立即指令）- 别名方法
        Args:
            index: AI端口索引 (1-based)
        Returns:
            str: ErrorID,{value},AI(index);
        """
        return self.ai(index)

    def get_do_group(self, group_index: int) -> str:
        """
        获取多个数字输出端口状态（立即指令）
        Args:
            group_index: IO组索引(0-3)

        Returns:
            str: ErrorID,{status1,status2,...},GetDOGroup(groupIndex);
        """
        return self._send_cmd(f"GetDOGroup({group_index})")

    def get_do_group_dec(self, group_index: int) -> str:
        """
        获取多个数字输出端口当前状态，返回值为十进制数（立即指令）

        Args:
            group_index: IO组索引(0-3)

        Returns:
            str: ErrorID,{value},GetDOGroupDEC(groupIndex);
        """
        return self._send_cmd(f"GetDOGroupDEC({group_index})")

    # ==================== 数字输入端口 ====================

    def di(self, index: int) -> str:
        """
        获取DI端口的状态（立即指令）
        Args:
            index: DI端口索引 (1-based)

        Returns:
            str: ErrorID,{status},DI(index);
        """
        return self._send_cmd(f"DI({index})")

    def di_group(self, group_index: int) -> str:
        """
        获取多个DI端口的状态（立即指令）
        Args:
            group_index: IO组索引(0-3)

        Returns:
            str: ErrorID,{status1,status2,...},DIGroup(groupIndex);
        """
        return self._send_cmd(f"DIGroup({group_index})")

    def di_group_dec(self, group_index: int) -> str:
        """
        获取多个DI端口的状态，返回值为十进制数（队列指令）

        Args:
            group_index: IO组索引(0-3)

        Returns:
            str: ErrorID,{value},DIGroupDEC(groupIndex);
        """
        return self._send_cmd(f"DIGroupDEC({group_index})")

    # ==================== 模拟输出端口 ====================

    def ao(self, index: int, value: float) -> str:
        """
        设置模拟输出端口的值（队列指令）
        Args:
            index: AO端口索引 (1-based)
            value: 模拟值(0.0-10.0V)

        Returns:
            str: ErrorID,{ResultID},AO(index,value);
        """
        return self._send_cmd(f"AO({index},{value:.2f})")

    def ao_instant(self, index: int, value: float) -> str:
        """
        设置模拟输出端口的值（立即指令）
        Args:
            index: AO端口索引 (1-based)
            value: 模拟值(0.0-10.0V)

        Returns:
            str: ErrorID,{},AOInstant(index,value);
        """
        return self._send_cmd(f"AOInstant({index},{value:.2f})")

    def get_ao(self, index: int) -> str:
        """
        获取模拟输出端口的值（立即指令）
        Args:
            index: AO端口索引 (1-based)

        Returns:
            str: ErrorID,{value},GetAO(index);
        """
        return self._send_cmd(f"GetAO({index})")

    # ==================== 模拟输入端口 ====================

    def ai(self, index: int) -> str:
        """
        获取AI端口的值（立即指令）
        Args:
            index: AI端口索引 (1-based)

        Returns:
            str: ErrorID,{value},AI(index);
        """
        return self._send_cmd(f"AI({index})")

    # ==================== 末端数字输出端口 ====================

    def tool_do(self, index: int, status: int) -> str:
        """
        设置末端数字输出端口状态（队列指令）
        Args:
            index: 末端DO端口索引 (0-1)
            status: 状态(0=Off, 1=On)

        Returns:
            str: ErrorID,{ResultID},ToolDO(index,status);
        """
        if status not in [0, 1]:
            raise ValueError("DO状态必须是0或1")
        return self._send_cmd(f"ToolDO({index},{status})")

    def tool_do_instant(self, index: int, status: int) -> str:
        """
        设置末端数字输出端口状态（立即指令）
        Args:
            index: 末端DO端口索引 (0-1)
            status: 状态(0=Off, 1=On)

        Returns:
            str: ErrorID,{},ToolDOInstant(index,status);
        """
        if status not in [0, 1]:
            raise ValueError("DO状态必须是0或1")
        return self._send_cmd(f"ToolDOInstant({index},{status})")

    def get_tool_do(self, index: int) -> str:
        """
        获取末端数字输出端口状态（立即指令）
        Args:
            index: 末端DO端口索引 (0-1)

        Returns:
            str: ErrorID,{status},GetToolDO(index);
        """
        return self._send_cmd(f"GetToolDO({index})")

    # ==================== 末端数字输入端口 ====================

    def tool_di(self) -> str:
        """
        获取末端DI端口的状态（立即指令）
        Returns:
            str: ErrorID,{status},ToolDI();
        """
        return self._send_cmd("ToolDI()")

    # ==================== 末端模拟输入端口 ====================

    def tool_ai(self) -> str:
        """
        获取末端AI端口的值（立即指令）
        Returns:
            str: ErrorID,{value},ToolAI();
        """
        return self._send_cmd("ToolAI()")

    # ==================== 末端工具设置 ====================

    def set_tool_485(self, baud: int, parity: int, data_bit: int, stop_bit: int) -> str:
        """
        设置末端485通信格式（立即指令）

        Args:
            baud: 波特率            parity: 校验位(0-无 1-奇 2-偶)
            data_bit: 数据位            stop_bit: 停止位
        Returns:
            str: ErrorID,{},SetTool485(baud,parity,dataBit,stopBit);
        """
        return self._send_cmd(f"SetTool485({baud},{parity},{data_bit},{stop_bit})")

    def set_tool_power(self, status: int) -> str:
        """
        设置末端工具供电状态（立即指令）
        Args:
            status: 供电状态(0-关闭, 1-开启)

        Returns:
            str: ErrorID,{},SetToolPower(status);
        """
        if status not in [0, 1]:
            raise ValueError("状态必须是0或1")
        return self._send_cmd(f"SetToolPower({status})")

    def set_tool_mode(self, mode: int) -> str:
        """
        设置末端复用端子的模式（立即指令）
        Args:
            mode: 模式值
        Returns:
            str: ErrorID,{},SetToolMode(mode);
        """
        return self._send_cmd(f"SetToolMode({mode})")