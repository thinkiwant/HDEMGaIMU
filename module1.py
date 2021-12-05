#!/usr/bin/env python3

import sys, time, imuThread
from PyQt5.Qt import *
from PyQt5 import QtWidgets, uic,QtGui
from PyQt5.QtCore import *

from PythonSocketServer import SocketServer
from mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    ipPref = '192.168.1.1'
    ipList = {ipPref+'1':0, ipPref+'2':1,ipPref+'3':2,ipPref+'4':3}

    def __init__(self,app, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        super().setWindowTitle("HD sEMG")
        self.app = app
        
        self.label.setText("File Name (5 alphabetic characters).")
        self.lcdNumber.display(123456)


        self.moduleList = [self.label_4,self.label_6, self.label_8,self.label_10]
        for i in self.moduleList:
            i.setPixmap(QPixmap('off.jpg'))


        defaultFileNamePrfx = 'AAAA'
        self.name = defaultFileNamePrfx
        # Start button
        self.pushButton.setCheckable(True)
        self.pushButton.clicked.connect(self.the_button1_clicked)

        # Stop button
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setDisabled(True)
        self.pushButton_2.clicked.connect(self.the_button2_clicked)

        # Apply button
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.clicked.connect(self.the_button3_clicked)

        # checkBox

        self.lcdNumber.display(0)

        # Line Edit

        # Recording Time
        self.time = [4, 176]
        self.sckServer = SocketServer(4,fuc = self.updateMStatus, filename = self.name)
        self.sckServer.setRecordTime(self.time)


        print(self.ipList)

    def the_button1_clicked(self):


        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_behave)
        self.imu()
        self.sckServer.startRecording()
        self.timer.start()

        #self.imuThread.join()

        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(False)




    def the_button2_clicked(self):
        self.sckServer.stopRecording()
        self.timer.stop()
        self.imuT.imu.Stop()

        print('Stop recording.')

        self.pushButton.setDisabled(False)
        self.pushButton_2.setDisabled(True)


    def the_button3_clicked(self):
        name = self.lineEdit.text()
        if name.isalpha() & (len(name)==4):
            self.name = name
            self.sckServer.setFileName(name)
        else:
            print('Invalid name format. Please change another file name.')

    def apply_fileName(self,s):
        print(s)

    def timer_behave(self):
        self.counter += 1
        self.lcdNumber.display(self.counter)
        if self.counter == self.time[0]*256 + self.time[1]:
            self.the_button2_clicked()

    def updateMStatus(self, ip, state):
        print(ip)
        if ip in MainWindow.ipList:
            if state == 1:
                pic = 'on.jpg'
            elif state == 0:
                pic = 'off.jpg'
            self.moduleList[MainWindow.ipList[ip]].setPixmap(QPixmap(pic))
            self.app.processEvents()
        else:
            print('ip status wasn\'t updated.')

    def imu(self):
        self.imuT = imuThread.imuThread(self.name+'1')
        self.imuT.start()





if __name__=='__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(app)
    window.show()
    app.exec()
