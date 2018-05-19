########################################################
# 再使用 cipher.py 去封装一个加密传输的 SecureSocket，以方便直接加解密 TCP Socket 中的流式数据（data flow）
# 这个 SecureSocket 用于 local 端和 server 端之间进行 TCP 通信，并且只使用 SecureSocket 通信时中间传输的数据会被加密，防火墙无法读到原数据
########################################################


import logging
import socket
import asyncio

from .cipher import Cipher
from ..utils.xlog import getLogger
Connection = socket.socket
logger = getLogger('local')


class SecureSocket:
    """
    SecureSocket is a socket,
    that has the ability to decode read and encode write.
    """

    # 加密传输的 TCP Socket
    def __init__(self, loop: asyncio.AbstractEventLoop, cipher: Cipher) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.cipher = cipher

    # 读取,解密
    async def decodeRead(self, conn: Connection):
        data = await self.loop.sock_recv(conn, 1024)
        decode_data = self.cipher.decode(data)
        return decode_data

    # 加密,写入
    async def encodeWrite(self, conn: Connection, bs: bytearray):
        encode_bs = self.cipher.encode(bs)
        await self.loop.sock_sendall(conn, encode_bs)

    async def encodeCopy(self, dst: Connection, src: Connection):
        """
        It encodes the data flow from the src and sends to dst.
        """
        while True:
            data = await self.loop.sock_recv(src, 1024)
            if not data:
                break
            await self.encodeWrite(dst, data)

    # 从 src 中源源不断的读取加密后的数据，解密后写入到 dst，直到 src 中没有数据可以再读取
    async def decodeCopy(self, dst: Connection, src: Connection):
        """
        It decodes the data flow from the src and sends to dst.
        """

        # logger.debug(' %s:%d => %s:%d', *src.getsockname(), *dst.getsockname())

        while True:
            bs = await self.decodeRead(src)
            if not bs:
                break
            await self.loop.sock_sendall(dst, bs)
