import asyncio
import socket


import sys
sys.path.append("..")
from module.cipher import Cipher
from module.securesocket import SecureSocket
from utils.xlog import getLogger
logger = getLogger('local')


class LsLocal(SecureSocket):
    # 新建一个本地端
    def __init__(self, loop, password, listenAddr, remoteAddr):
        super().__init__(loop=loop, cipher=Cipher.NewCipher(password))
        self.listenAddr = listenAddr
        self.remoteAddr = remoteAddr

    # 本地端启动监听，接收来自本机浏览器的连接
    async def listen(self):
        # ipv4,tcp模式
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(self.listenAddr)
            sock.listen(socket.SOMAXCONN)
            sock.setblocking(False)

            logger.info(f'正在监听: {self.listenAddr.ip}: {self.listenAddr.port}')

            while True:
                local_sock, address = await self.loop.sock_accept(sock)
                asyncio.ensure_future(self.handleConn(local_sock))

    async def handleConn(self, local_sock: socket.socket):
        remote_sock = await self.dialRemote()

        def cleanUp(task):
            """
            Close the socket when they succeeded or had an exception.
            """
            # 退出本次工作
            remote_sock.close()
            local_sock.close()

        logger.debug(f"数据发送流程: {local_sock.getpeername()} ==> {local_sock.getsockname()} ==> {remote_sock.getsockname()} ==> {remote_sock.getpeername()}")
        # 两个协程工作,加密发送,解密接收
        tasks = (self.encodeCopy(dst=remote_sock, src=local_sock),
                 self.decodeCopy(dst=local_sock, src=remote_sock)
                 )
        task = asyncio.gather(*tasks, loop=self.loop, return_exceptions=True)
        task.add_done_callback(cleanUp)

    async def dialRemote(self):
        """
        Create a socket that connects to the Remote _sock.
        """
        try:
            remoteConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remoteConn.setblocking(False)
            await self.loop.sock_connect(remoteConn, self.remoteAddr)
            return remoteConn
        except Exception as e:
            raise ConnectionError(f'链接到远程服务器 {self.remoteAddr}失败:{e}')
