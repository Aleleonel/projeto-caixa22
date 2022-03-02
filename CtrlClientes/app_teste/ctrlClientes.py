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


class InsertDialog(QDialog):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Cliente :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Dados do Cliente :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.addcliente)

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.branchinput = QComboBox()
        self.branchinput.addItem("Pessoa Física")
        self.branchinput.addItem("Empresa")
        layout.addWidget(self.branchinput)

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nome / Razão")
        layout.addWidget(self.nameinput)

        self.cpfinput = QLineEdit()
        self.cpfinput.setPlaceholderText("Cpf")
        layout.addWidget(self.cpfinput)

        self.rginput = QLineEdit()
        self.rginput.setPlaceholderText("R.G")
        layout.addWidget(self.rginput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Telefone NO.")
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Endereço")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addcliente(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        nome = ""
        tipo = ""
        cpf = ""
        rg = ""
        tel = ""
        endereco = ""

        nome = self.nameinput.text()
        tipo = self.branchinput.itemText(self.branchinput.currentIndex())
        cpf = self.cpfinput.text()
        rg = self.rginput.text()
        # sem = -self.seminput.itemText(self.seminput.currentIndex())
        tel = self.mobileinput.text()
        endereco = self.addressinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO clientes (tipo, nome, cpf, rg, telefone, endereco)" \
                          "VALUES (%s,%s,%s,%s,%s,%s)"
            dados = tipo, nome, cpf, rg, tel, endereco
            self.cursor.execute(comando_sql, dados)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')


class SearchDialog(QDialog):
    """
        Define uma nova janela onde executaremos 
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.QBtn = QPushButton()
        self.QBtn.setText("Procurar")

        self.setWindowTitle("Pesquisar Cliente")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de busca
        self.QBtn.clicked.connect(self.searchcliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitaçãoe e
        # verifica se é um numero
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Codigo do cliente - somente número")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # busca o cliente pelo codigo
    def searchcliente(self):
        searchroll = ""
        searchroll = self.searchinput.text()

        try:
            consulta_sql = "SELECT * FROM clientes WHERE codigo = " + str(searchroll)
            self.cursor.execute(consulta_sql)
            result = self.cursor.fetchall()

            for row in range(len(result)):
                searchresult = "Codigo : " + str(result[0][0]) \
                               + '\n' + "Tipo : " + str(result[0][1]) \
                               + '\n' + "Nome : " + str(result[0][2]) \
                               + '\n' + "CPF : " + str(result[0][3]) \
                               + '\n' + "R.G : " + str(result[0][4]) \
                               + '\n' + "Tel : " + str(result[0][5]) \
                               + '\n' + "Ender. : " + str(result[0][6])

            QMessageBox.information(QMessageBox(), 'Pesquisa realizada com sucesso!', searchresult)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A pesquisa falhou!')

        # finally:
        #     if conexao.banco.is_connected():
        #         conexao.banco.close()
        #         self.cursor.close()
        #         print("Conexão ao MySQL encerrada")


class DeleteDialog(QDialog):
    """
        Define uma nova janela onde executaremos 
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Cliente")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deletecliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do cliente - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletecliente(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM clientes WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Deleção realizada com sucesso!', 'DELETADO COM SUCESSO!')
            self.close()

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A Deleção falhou!')


class AboutDialog(QDialog):
    """
        Define uma nova janela onde mostra as informações
        do botão sobre
    """

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(500)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Configurações do titulo da Janela
        layout = QVBoxLayout()

        self.setWindowTitle("Sobre")
        title = QLabel("SCC - Sistema de Controle de Clientes")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        # Configurações de atribuição de imagem
        labelpic = QLabel()
        pixmap = QPixmap('../Icones/perfil.png')
        # pixmap = pixmap.scaledToWidth(400)
        pixmap = pixmap.scaled(QSize(500, 500))
        labelpic.setPixmap(pixmap)
        # labelpic.setFixedHeight(400)
        layout.addWidget(title)
        layout.addWidget(labelpic)

        layout.addWidget(QLabel("Versão:V1.0"))
        layout.addWidget(QLabel("Nome: Alexandre Leonel de Oliveira"))
        layout.addWidget(QLabel("Nascido em: São Paulo em 26 de Junho de 1974"))
        layout.addWidget(QLabel("Profissão: Bacharel em Sistemas de Informação"))
        layout.addWidget(QLabel("Copyright Bi-Black-info 2021"))

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('../Icones/dollars.png'))

        # cria banco de dados se ele não existir
        self.cursor = conexao.banco.cursor()
        self.comando_sql = "CREATE TABLE IF NOT EXISTS clientes(\
                            codigo INT PRIMARY KEY AUTO_INCREMENT,\
                            tipo VARCHAR(15),\
                            nome VARCHAR(60),\
                            cpf VARCHAR(20),\
                            rg VARCHAR(20),\
                            telefone VARCHAR(15),\
                            endereco VARCHAR(100))"
        self.cursor.execute(self.comando_sql)
        self.cursor.close()

        # cria um menu
        file_menu = self.menuBar().addMenu("&Arquivo")
        help_menu = self.menuBar().addMenu("&Ajuda")

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(6)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Codigo", "Tipo", "Nome", "CPF", "RG", "Tel", "Endereco",))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("../Icones/add.png"), "Add Cliente", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Cliente")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("../Icones/atualizar.png"), "Atualizar dados do Cliente", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("../Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_caixa = QAction(QIcon("../Icones/dollars.png"), "Caixa - abre o Caixa", self)
        btn_ac_caixa.setStatusTip("Caixa")
        toolbar.addAction(btn_ac_caixa)

        btn_ac_delete = QAction(QIcon("../Icones/deletar.png"), "Deletar o Cliente", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        # Abre controle de caixa
        caixa_action = QAction(QIcon("../Icones/dollars.png"), "Caixa - abre o Caixa", self)
        caixa_action.setStatusTip("Caixa")
        file_menu.addAction(caixa_action)

        # Arquivo >> Adicionar
        adduser_action = QAction(QIcon("../Icones/add.png"), "Add Cliente", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        # Arquivo >> Busca
        search_action = QAction(QIcon("../Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        search_action.triggered.connect(self.search)
        file_menu.addAction(btn_ac_search)

        # Deleta Clientes
        delete_action = QAction(QIcon("../Icones/deletar.png"), "Deletar o Cliente", self)
        delete_action.triggered.connect(self.delete)
        file_menu.addAction(delete_action)

        #
        about_action = QAction(QIcon("../Icones/sobre-nos.png"), "Desenvolvedores", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM clientes"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        for i in range(0, len(result)):
            for j in range(0, 7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()


app = QApplication(sys.argv)
if QDialog.Accepted:
    window = MainWindow()
    window.show()
    window.loaddata()

sys.exit((app.exec_()))