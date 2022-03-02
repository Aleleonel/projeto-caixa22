from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *

import time
import os
import sys

import mysql.connector
from mysql.connector import OperationalError

import conexao


class LoginForm(QWidget):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setWindowTitle('Login')
        self.resize(500, 120)

        layout = QGridLayout()

        label_nome = QLabel('<font size="4"> Usuário </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Nome de Usuário')
        layout.addWidget(label_nome, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_senha = QLabel('<font size="4"> Senha </font>')
        self.lineEdit_senha = QLineEdit()
        self.lineEdit_senha.setPlaceholderText('sua senha aqui')
        layout.addWidget(label_senha, 1, 0)
        layout.addWidget(self.lineEdit_senha, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_senha)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def check_senha(self):
        msg = QMessageBox()

        if self.lineEdit_username.text() == 'Alexandre' and self.lineEdit_senha.text() == '1234':
            msg.setText("Sucesso")
            msg.exec_()
            app.quit()
        else:
            msg.setText("Credenciais Incorretas")
            msg.exec_()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())