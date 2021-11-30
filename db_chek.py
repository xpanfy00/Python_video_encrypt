import MySQLdb
import hashlib
from PyQt5.QtWidgets import QMessageBox



def db_reg(login, password):
    conn = MySQLdb.connect('remotemysql.com', 'yxJuVD43CW', '3jSzCrLc0S', 'yxJuVD43CW')
    cursor = conn.cursor()
    sql = "SELECT * FROM User WHERE Login = %s"
    val = (login,)
    cursor.execute(sql, val)
    chek_login = cursor.fetchall()
    print(len(chek_login))

    if len(chek_login) == 0 :
        encoded = password.encode()
        result = hashlib.sha256(encoded)

        sql = "INSERT INTO User (Login, Pass) VALUES (%s, %s)"
        val = (login, result.hexdigest())

        cursor.execute(sql, val)
        conn.commit()
        print("Add to database")
        conn.close()
        msg = QMessageBox()
        msg.setWindowTitle("Registration")
        msg.setText("Successfully add to database")
        msg.exec_()
    elif login == chek_login[0][1]:
        message = chek_login[0][1]
        msg = QMessageBox()
        msg.setWindowTitle("Registration")
        msg.setText(message + "Already exists")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

def db_login(login, password):
    conn = MySQLdb.connect('remotemysql.com', 'yxJuVD43CW', '3jSzCrLc0S', 'yxJuVD43CW')
    cursor = conn.cursor()
    sql = "SELECT * FROM User WHERE Login = %s"
    val = (login,)
    cursor.execute(sql, val)
    chek_login = cursor.fetchall()
    encoded = password.encode()
    result = hashlib.sha256(encoded)

    if len(chek_login) == 0:
        message = login + " do not exists into database"
        msg = QMessageBox()
        msg.setWindowTitle("Login in")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
    elif chek_login[0][1] == login and chek_login[0][2] == result.hexdigest():
        message = "successfully login in"
        msg = QMessageBox()
        msg.setWindowTitle("Login in")
        msg.setText(message)
        msg.exec_()
        return 1
    else:
        message = "Wrong login or password"
        msg = QMessageBox()
        msg.setWindowTitle("Login in")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
