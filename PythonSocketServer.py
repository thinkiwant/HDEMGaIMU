
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

from threading import Timer
import socket               # 导入 socket 模块
from struct import *
import time
class SocketServer():

    ipPref = '192.168.1.1'
    ipList = {ipPref+'1':0, ipPref+'2':1,ipPref+'3':2,ipPref+'4':3}

    # The first command byte
    GETSET = 0
    FSAMP1 = 0b10
    NCH = 0b11
    MODE = 0

    cmd1 = GETSET*0b10000000 + FSAMP1*0b100000 + NCH*0b1000 + MODE*0b1
    print(cmd1)
    # The second command byte
    HRES = 0
    HPF = 1
    EXT = 0
    TRIG = 0b11
    REC = 1
    GO = 0

    cmd2 = HRES*0b10000000 + HPF*0b1000000 + EXT*0b10000 + TRIG*0b100 + REC*0b10 + GO*0b1
    cmd3 = HRES*0b10000000 + HPF*0b1000000 + EXT*0b10000 + TRIG*0b100 + 0  *0b10 + GO*0b1
    print(cmd2)

    cmdO = pack('2B', cmd1, cmd2)
    cmdF = pack('2B', cmd1, cmd3)

    # Time Bytes


    ##print(cmd)


    def __init__(self, *args, **kwargs):
        self.s = socket.socket()         # 创建 socket 对象
        self.host = socket.gethostname() # 获取本地主机名
        self.port = 45454    
        print('主机名:',self.host)# 设置端口
        self.s.bind((self.host, self.port))        # 绑定端口
        self.s.listen(5)                 # 等待客户端连接
        self.num = args[0]
        self.accList = []
        self.f = kwargs['fuc']
        self.fileName= kwargs['filename']
        self.time  = pack('2B', 4,176) # first byte: 256 seconds,  second Byte: 1 second

    def __del__(self):
        print("End Socket.")
        self.s.close()

    def setFileName(self, name):
        self.fileName = name
            
        print('set file name: ', self.fileName)

    def startRecording(self):
        self.sendCommand(self.cmdO, 1)

    def stopRecording(self):
        self.sendCommand(self.cmdF, 0)

    def setRecordTime(self, t):
        self.time = pack('2B', t[0], t[1])

    def sendCommand(self, cmdB, state = 1):
        while True:
            if (len(self.accList)==self.num):
                self.accList = []
                break
            c,addr = self.s.accept()     # 建立客户端连接
            ip = addr[0]
            if (ip not in self.accList):
                ModleSig = (self.ipList[ip] + 65).to_bytes(1,byteorder = 'little')
                a ='A'
                print ('连接地址：', ip)
                if state == 1:
                    fileNameCode = self.fileName.encode()
                    timeStamp = self.getTimeStampBytes()
                    cmd = cmdB + self.time + fileNameCode + ModleSig
                else:
                    cmd = cmdB
                c.send(cmd)
                self.accList.append(ip)
                self.f(ip, state)
            else:
                print('address already exists:', ip)
            c.close()                # 关闭连接

    def getTimeStampBytes(self):
        localtime = time.localtime()

        y = localtime[0]-1980
        m = localtime[1]
        d = localtime[2]
        h = localtime[3]
        m = localtime[4]
        s = localtime[5]

        r1 = (y<<1) + (m>>7)
        r2 = ((m&7)<<5) + d
        r3 = (h<<3) + ((m&56)>>3)
        r4 = ((m&7)<<5) + s

        r = pack('4B', r1,r2,r3,r4)
        return r