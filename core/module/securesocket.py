########################################################
# 再使用 cipher.py 去封装一个加密传输的 SecureSocket，以方便直接加解密 TCP Socket 中的流式数据（data flow）
# 这个 SecureSocket 用于 local 端和 server 端之间进行 TCP 通信，并且只使用 SecureSocket 通信时中间传输的数据会被加密，防火墙无法读到原数据
########################################################


import logging
import socket
import asyncio

from ..utils.xlog import getLogger
Connection = socket.socket
logger = getLogger('local')


class SecureSocket:
    def __init__(self, loop):
        self.loop = loop

    async def encodeWrite(self, con, data):
        await self.loop.sock_sendall(con, data)

    async def Copy(self, dst, src):
        while True:
            data = await self.loop.sock_recv(src, 1024)
            if not data:
                break
            await self.loop.sock_sendall(dst, data)
