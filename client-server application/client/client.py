from email import message
import socket
import socket
import sys
from _thread import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import time

ui,_=loadUiType('client.ui')

class MainApp(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Server Window")
        self.setupUi(self)
        
        self.show()
        self.key=0
        self.handlebuttons()
        self.handleui()
        #self.connect()
        
    def handlebuttons(self):
        self.pushButton_2.clicked.connect(self.connect)
        self.pushButton.clicked.connect(self.sendmessage1)
        self.pushButton.setShortcut('enter')
    def handleui(self):
        self.tabWidget.setCurrentIndex(0)
        
        self.plainTextEdit_2.setEnabled(False)
    def connect(self):
        
        ip=self.lineEdit.text()
        if ip !="":
            try:
                self.clientsocket=socket.socket(family= socket.AF_INET ,type=socket.SOCK_STREAM)
                if(self.key==1):
                    self.clientsocket.close()
                    self.key=0
                    
                
                self.clientsocket.connect((ip,12345))
                self.label_2.setText("Connected")
                name=socket.gethostname()
                self.clientsocket.send(name.encode('utf-8'))
                self.plainTextEdit_2.appendPlainText("connected to Server")
                self.key=1
                time.sleep(2)
                self.tabWidget.setCurrentIndex(1)
                start_new_thread( self.recvmessage,())

                
            except:
                self.label_2.setText("Offline")
        else:
            self.label_2.setText("Enter IP")
                
        
    def recvmessage(self):
        while True:
            try:
                message=self.clientsocket.recv(2048).decode('utf-8')
                #message="server : "+message
                self.plainTextEdit_2.appendPlainText(message)
            except:     
                self.plainTextEdit_2.appendPlainText('Disconnected')
                self.clientsocket.close()
                self.key=0
                break
    
    def sendmessage1(self):

        message=self.plainTextEdit.toPlainText()
        if (message !=""):
            self.clientsocket.send(message.encode('utf-8'))
            self.plainTextEdit.setPlainText("")
            
            message="you : "+message
            self.plainTextEdit_2.appendPlainText(message)
           
    def setdata(self,message):
        self.plainTextEdit_2.appendPlainText(message)



def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__=="__main__":
    main()


#clientsocket=socket.socket(family= socket.AF_INET ,type=socket.SOCK_STREAM)
#clientsocket.connect(("172.31.6.88",12345))
#message=input('enter message to send :')
# def recv_message(client):
#   while True:
#        print(clientsocket.recv(1024).decode('utf-8'))
# def send_message(client):
#    while True:
 #       print(clientsocket.send(input().encode('utf-8')))

#message=socket.gethostname()
#clientsocket.send(message.encode('utf-8'))
#start_new_thread(recv_message,(clientsocket,))
#start_new_thread(send_message,(clientsocket,))

#while True:
    #print(clientsocket.recv(2048).decode('utf-8'))
    #clientsocket.send(input().encode('utf-8'))

#clientsocket.close()
