import sys
import db_chek
import socket,cv2, pickle,struct
from cryptography.fernet import Fernet
from PyQt5 import QtCore, QtGui, QtWidgets
from des import *
from des1 import *

with open('Key.key','rb') as f:
    key = f.read()

fernet = Fernet(key)

class MainForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)




class LoginForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)

def startclient():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = MainForm.ui.lineEdit.text()
    port = 9999
    client_socket.connect((host_ip, port))
    if client_socket:
        MainForm.ui.label.setText("Server conectied")
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)  # 4KB
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4096)  # получение зашифрованных данных от клиента
        frame_data = data[:msg_size]  # разбиение данных на сегменты равного размера
        frame_data = fernet.decrypt(frame_data)  # расшифровка полученных данных
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            MainForm.ui.label.setText("Disconected from server: ")
            break
    client_socket.close()

def one_click_reg():
    login = LoginForm.ui.lineEdit.text()
    password = LoginForm.ui.lineEdit_2.text()
    db_chek.db_reg(login, password)


def one_click_log():
    login = LoginForm.ui.lineEdit.text()
    password = LoginForm.ui.lineEdit_2.text()

    if db_chek.db_login(login, password) == 1:
        LoginForm.close()
        MainForm.show()
        MainForm.ui.pushButton_client.clicked.connect(startclient)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    LoginForm = LoginForm()
    MainForm = MainForm()
    LoginForm.show()
    LoginForm.ui.pushButton.clicked.connect(one_click_reg)
    LoginForm.ui.pushButton_2.clicked.connect(one_click_log)



    sys.exit(app.exec())
