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
        remoteServer = await self.dialRemote()

        def cleanUp(task):
            """
            Close the socket when they succeeded or had an exception.
            """
            # 退出本次工作
            remoteServer.close()
            local_sock.close()

        # 从 localUser 读取数据发送到 dstServer

        logger.debug(f"接到请求,链接到远程服务器: {local_sock.getpeername()} ==> {local_sock.getsockname()} ==> {remoteServer.getsockname()} ==> {remoteServer.getpeername()}")
        # 从 localUser 发送数据发送到 proxyServer，这里因为处在翻墙阶段出现网络错误的概率更大
        local2remote = asyncio.ensure_future(self.encodeCopy(remoteServer, local_sock))

        remote2local = asyncio.ensure_future(self.decodeCopy(local_sock, remoteServer))
        task = asyncio.ensure_future(asyncio.gather(local2remote, remote2local, loop=self.loop, return_exceptions=True))
        task.add_done_callback(cleanUp)

    async def dialRemote(self):
        """
        Create a socket that connects to the Remote Server.
        """
        try:
            remoteConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remoteConn.setblocking(False)
            await self.loop.sock_connect(remoteConn, self.remoteAddr)
        except Exception as err:
            raise ConnectionError('链接到远程服务器 %s:%d 失败:\n%r' % (*self.remoteAddr, err))

        return remoteConn
