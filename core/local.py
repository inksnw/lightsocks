import sys
import asyncio
import socket
import os
from .module.cipher import Cipher
from .module.securesocket import SecureSocket
from .utils.xlog import getLogger
logger = getLogger('local')


class LsLocal(SecureSocket):
    # 新建一个本地端

    def __init__(self, loop, listenAddr, remoteAddr):
        super().__init__(loop=loop)
        self.listenAddr = listenAddr
        self.remoteAddr = remoteAddr

    async def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.listenAddr)
        sock.listen(socket.SOMAXCONN)
        sock.setblocking(False)

        logger.info(f'正在监听: {self.listenAddr}')

        while True:
            local_sock, address = await self.loop.sock_accept(sock)
            asyncio.ensure_future(self.handleConn(local_sock))
        sock.close()

    async def handleConn(self, local_sock):
        remote_sock = await self.dialRemote()

        def cleanUp(task):
            remote_sock.close()
            local_sock.close()

        logger.debug(f"数据发送流程: {local_sock.getpeername()} ==> {local_sock.getsockname()} ==> {remote_sock.getsockname()} ==> {remote_sock.getpeername()}")
        tasks = (self.Copy(dst=remote_sock, src=local_sock), self.Copy(dst=local_sock, src=remote_sock))
        task = asyncio.gather(*tasks, loop=self.loop, return_exceptions=True)
        task.add_done_callback(cleanUp)

    async def dialRemote(self):
        try:
            remoteConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remoteConn.setblocking(False)
            await self.loop.sock_connect(remoteConn, self.remoteAddr)
            return remoteConn
        except Exception as e:
            raise e
            raise ConnectionError(f'链接到远程服务器 {self.remoteAddr}失败:{e}')
