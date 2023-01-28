
from asyncio import windows_events
from json import load
import socket
from _thread import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys

ui,_=loadUiType('server.ui')

class MainApp(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Server Window")
        self.setupUi(self)
        self.handlebuttons()
        self.handleUi()
        self.connections={}
        
        
        self.show()
    
    def handleUi(self):
        self.plainTextEdit_2.setEnabled(False)
        self.tabWidget.setCurrentIndex(0)
        self.server=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        self.servername=socket.gethostname()
        self.ip=socket.gethostbyname(self.servername)
        print("server started")
        self.server.bind((self.ip,12345))
        self.server.listen(5)
        start_new_thread(self.getconnection)
        
        
    def handlebuttons(self):
        self.pushButton_2.clicked.connect(self.returnip)
        self.pushButton.clicked.connect(self.sendmessage)
        self.pushButton.setShortcut('enter')


    # ACTIONS

    def getconnection(self):
        while True:
            print("waiting for connection")
            self.client,self.addr=self.server.accept()
            print('connected to ',self.addr)
            self.plainTextEdit_2.appendPlainText('connected to '+self.addr[0]+" at "+str(self.addr[1]))
            
            start_new_thread(self.recvmessage,(self.client,))



    def returnip(self):
        self.lineEdit.setText(self.ip)

    def sendmessage(self):
        message=self.plainTextEdit.toPlainText()
        if message!="":
            message='server : '+message
            self.client.send(message.encode('utf-8'))
            self.plainTextEdit.setPlainText("")
            message="you : "+message.replace("server : ","")
            self.plainTextEdit_2.appendPlainText(message)
    def recvmessage(self,client):
        name=self.client.recv(1024).decode('utf-8')
        self.connections[self.client]=name
        print(self.connections)

        start_new_thread(self.recvmessage1,(self.client,))
        
    def recvmessage1(self,client):
        while True:
            try:
                message=client.recv(1024).decode('utf-8')
                name=str(self.connections[client])
                message=name+' : '+message
                self.plainTextEdit_2.appendPlainText(message)
                client.sendAll(message.encode('utf-8'))
                #self.plainTextEdit_2.appendPlainText(self.connections[client]+" "+message.encode('utf-8'))
            except:
                pass



def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__=="__main__":
    main()







