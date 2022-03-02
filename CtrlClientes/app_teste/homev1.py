from unicodedata import decimal

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *

import time, datetime
import os
import sys
import csv

import mysql.connector
from mysql.connector import OperationalError

import conexao

global loginok


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


class CadastroEstoque(QDialog):
    """
        Define uma nova janela onde cadastramos os produtos
        no estoque
    """

    def __init__(self, *args, **kwargs):
        super(CadastroEstoque, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Estoque :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Descição do Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.cursor = conexao.banco.cursor()
        consulta_sql = "SELECT * FROM produtos"
        self.cursor.execute(consulta_sql)
        result = self.cursor.fetchall()

        # conexao.banco.commit()
        # self.cursor.close()

        self.QBtn.clicked.connect(self.addproduto)

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.codigoinput = QComboBox()
        busca = []
        for row in range(len(result)):
            busca.append(str(result[row][0]))
        for i in range(len(busca)):
            self.codigoinput.addItem(str(busca[i]))

        layout.addWidget(self.codigoinput)

        self.statusinput = QLineEdit()
        self.statusinput.setPlaceholderText("E")
        layout.addWidget(self.statusinput)

        # Insere o ramo ou tipo /

        self.descricaoinput = QLineEdit()
        self.descricaoinput.setPlaceholderText("Descrição")
        layout.addWidget(self.descricaoinput)

        self.precoinput = QLineEdit()
        self.precoinput.setPlaceholderText("Preço de Compra")
        layout.addWidget(self.precoinput)

        self.qtdinput = QLineEdit()
        self.qtdinput.setPlaceholderText("Quantidade")
        layout.addWidget(self.qtdinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addproduto(self):
        """
        captura as informações digitadas
        no COMBOBOX e armazena nas variaveis
        :return:
        codigo = ""
        quantidade = ""
        preco = ""
        status = "E"
        E da entrada na tabela estoque
        e preço de compra
        """
        self.cursor = conexao.banco.cursor()
        consulta_sql = ("SELECT * FROM produtos WHERE codigo =" + str(self.codigoinput.itemText(
            self.codigoinput.currentIndex())))
        self.cursor.execute(consulta_sql)
        valor_codigo = self.cursor.fetchall()

        for i in range(len(valor_codigo)):
            dados_lidos = valor_codigo[i][1]

        codigo = ""
        quantidade = ""
        preco = ""
        status = "E"

        codigo = self.codigoinput.itemText(self.codigoinput.currentIndex())
        self.descricaoinput.setText(dados_lidos)
        preco = self.precoinput.text()
        quantidade = self.qtdinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO estoque (idproduto, estoque, status)" \
                          "VALUES (%s, %s, %s)"
            dados = codigo, quantidade, status
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()
            self.cursor.close()

            self.cursor = conexao.banco.cursor()
            consulta_sql_preco = "INSERT INTO precos (idprecos, preco) VALUES (%s, %s)"
            dados_preco = codigo, preco
            self.cursor.execute(consulta_sql_preco, dados_preco)
            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')

        self.cursor = conexao.banco.cursor()
        consulta_sql_estoque = "SELECT idproduto, estoque FROM estoque WHERE idproduto =" + codigo
        self.cursor.execute(consulta_sql_estoque)
        dados_estoque = self.cursor.fetchall()

        total_estoque = 0
        soma = []
        for i in range(len(dados_estoque)):
            if dados_estoque[i][1]:
                total_estoque = int(dados_estoque[i][1])
                soma.append(total_estoque)
        saldo = sum(soma)
        print(sum(soma))
        print(saldo)

        # consulta_sql_saldo = "UPDATE itens_estoque a " \
        #                      "SET a.total = %s" \
        #                      "WHERE a.idprodutos = %s"
        #
        # dados = saldo, codigo
        # self.cursor.execute(consulta_sql_saldo, dados)
        # conexao.banco.commit()
        # self.cursor.close()


class ListEstoque(QMainWindow):
    def __init__(self):
        super(ListEstoque, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE ESTOQUE")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(5)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ("Codigo", "Descrição", "Preço de Compra", "Quantidade", "Atualização",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, b.preco, e.estoque, e.ultupdate FROM controle_clientes.produtos" \
                      " as a" \
                      " LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo" \
                      " LEFT JOIN controle_clientes.estoque as e ON e.idproduto = a.codigo;"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("../Icones/add.png"), "Cadastro Estoque morto", self)
        btn_ac_adduser.triggered.connect(self.cadEstoque)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("../Icones/atualizar.png"), "Atualizar dados do Cliente", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("../Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("../Icones/deletar.png"), "Deletar o Cliente", self)
        # btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        self.show()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, b.preco, e.estoque, e.ultupdate FROM controle_clientes.produtos" \
                      " as a" \
                      " LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo" \
                      " LEFT JOIN controle_clientes.estoque as e ON e.idproduto = a.codigo;"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadEstoque(self):
        dlg = CadastroEstoque()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchEstoque()
        dlg.exec_()

    # def delete(self):
    #     dlg = DeleteEstoque()
    #     dlg.exec_()


class SearchEstoque(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchEstoque, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.QBtn = QPushButton()
        self.QBtn.setText("Procurar")

        self.setWindowTitle("Pesquisar Produto em Estoque")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de busca
        self.QBtn.clicked.connect(self.searchProdEstoque)

        layout = QVBoxLayout()

        # Cria as caixas de digitaçãoe e
        # verifica se é um numero
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Codigo do Produto - somente número")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # busca o produto pelo codigo
    def searchProdEstoque(self):
        searchroll = ""
        searchroll = self.searchinput.text()

        try:
            consulta_estoque = "SELECT * FROM controle_clientes.estoque WHERE idproduto=" + str(searchroll)
            self.cursor.execute(consulta_estoque)
            result_estoque = self.cursor.fetchall()
            for row in range(len(result_estoque)):
                searchresult1 = "Codigo : " + str(result_estoque[0][0]) + '\n'

            consulta_produto = "SELECT * FROM controle_clientes.produtos WHERE codigo=" + str(searchroll)
            self.cursor.execute(consulta_produto)
            result_produto = self.cursor.fetchall()
            for row in range(len(result_produto)):
                searchresult2 = "Descrição : " + str(result_produto[0][1])

            mostra = searchresult1 + searchresult2

            QMessageBox.information(QMessageBox(), 'Pesquisa realizada com sucesso!', mostra)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A pesquisa falhou!')


class CadastroClientes(QDialog):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(CadastroClientes, self).__init__(*args, **kwargs)

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


class DeleteClientes(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteClientes, self).__init__(*args, **kwargs)

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


class CadastroProdutos(QDialog):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(CadastroProdutos, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Descição do Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.addproduto)

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.uninput = QComboBox()
        self.uninput.addItem("UN")
        self.uninput.addItem("PÇ")
        self.uninput.addItem("KG")
        self.uninput.addItem("LT")
        self.uninput.addItem("PT")
        self.uninput.addItem("CX")
        layout.addWidget(self.uninput)

        self.descricaoinput = QLineEdit()
        self.descricaoinput.setPlaceholderText("Descrição")
        layout.addWidget(self.descricaoinput)

        self.ncminput = QLineEdit()
        self.ncminput.setPlaceholderText("NCM")
        layout.addWidget(self.ncminput)

        self.precoinput = QLineEdit()
        self.precoinput.setPlaceholderText("Preço.")
        layout.addWidget(self.precoinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addproduto(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        descricao = ""
        ncm = ""
        un = ""
        preco = ""

        descricao = self.descricaoinput.text()
        ncm = self.ncminput.text()
        un = self.uninput.itemText(self.uninput.currentIndex())
        preco = self.precoinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO produtos (descricao, ncm, un, preco)" \
                          "VALUES (%s,%s,%s,%s)"
            dados = descricao, ncm, un, str(preco)
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')

        self.cursor = conexao.banco.cursor()
        consulta_prod = "SELECT * FROM produtos"
        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()

        itens_codigo = 0
        for i in range(len(result_prod)):
            itens_codigo = result_prod[i][0]

        print(itens_codigo)
        total = 0
        total_estoque = 0

        self.cursor = conexao.banco.cursor()
        comando_sql_itens = "INSERT INTO itens_estoque (idprodutos, total, total_estoque) VALUES (%s, %s, %s)"
        dados = itens_codigo, total, total_estoque
        self.cursor.execute(comando_sql_itens, dados)
        conexao.banco.commit()
        self.cursor.close()


class ListProdutos(QMainWindow):
    def __init__(self):
        super(ListProdutos, self).__init__()
        self.setWindowIcon(QIcon('../Icones/produtos2.png'))

        # cria banco de dados se ele não existir
        self.cursor = conexao.banco.cursor()
        self.comando_sql = "CREATE TABLE IF NOT EXISTS produtos(\
                                    codigo INT PRIMARY KEY AUTO_INCREMENT,\
                                    descricao VARCHAR(60),\
                                    ncm VARCHAR(20),\
                                    un VARCHAR(2),\
                                    preco FLOAT)"
        self.cursor.execute(self.comando_sql)
        self.cursor.close()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PRODUTOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

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
        self.tableWidget.setHorizontalHeaderLabels(("Codigo", "Descrição", "NCM", "UN", "Preço", "Estoque",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, a.ncm, a.un, a.preco, e.estoque FROM " \
                      "controle_clientes.produtos " \
                      "as a LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo LEFT JOIN " \
                      "controle_clientes.estoque as e ON e.idproduto = a.codigo; "
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)

        for i in range(0, len(result)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("../Icones/add.png"), "Add Produto", self)
        btn_ac_adduser.triggered.connect(self.cadProdutos)
        btn_ac_adduser.setStatusTip("Add Produto")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("../Icones/atualizar.png"), "Atualizar dados do produto", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_delete = QAction(QIcon("../Icones/deletar.png"), "Deletar o Produto", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        btn_ac_search = QAction(QIcon("../Icones/pesquisa.png"), "Pesquisar dados por produto", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        self.show()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, a.ncm, a.un, a.preco, e.estoque FROM " \
                      "controle_clientes.produtos " \
                      "as a LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo LEFT JOIN " \
                      "controle_clientes.estoque as e ON e.idproduto = a.codigo; "
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)

        for i in range(0, len(result)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadProdutos(self):
        dlg = CadastroProdutos()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchProdutos()
        dlg.exec_()

    def delete(self):
        dlg = DeleteProduto()
        dlg.exec_()
        self.loaddata()


class SearchProdutos(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchProdutos, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.QBtn = QPushButton()
        self.QBtn.setText("Procurar")

        self.setWindowTitle("Pesquisar Produto")
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
        self.searchinput.setPlaceholderText("Codigo do Produto - somente número")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # busca o cliente pelo codigo
    def searchcliente(self):
        searchroll = ""
        searchroll = self.searchinput.text()

        try:
            consulta_sql = "SELECT * FROM produtos WHERE codigo = " + str(searchroll)
            self.cursor.execute(consulta_sql)
            result = self.cursor.fetchall()

            for row in range(len(result)):
                searchresult = "Codigo : " + str(result[0][0]) \
                               + '\n' + "Descrição : " + str(result[0][1]) \
                               + '\n' + "NCM : " + str(result[0][2]) \
                               + '\n' + "UN : " + str(result[0][3]) \
                               + '\n' + "Preço : " + str(result[0][4])

            QMessageBox.information(QMessageBox(), 'Pesquisa realizada com sucesso!', searchresult)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A pesquisa falhou!')


class DeleteProduto(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteProduto, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Produto")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deleteproduto)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do produto - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteproduto(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM produtos WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Deleção realizada com sucesso!', 'PRODUTO DELETADO COM SUCESSO!')
            self.close()

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A Deleção falhou!')


class ListClientes(QMainWindow):
    def __init__(self):
        super(ListClientes, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(7)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Codigo", "Tipo", "Nome", "CPF", "RG", "Tel", "Endereco",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM clientes"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        for i in range(0, len(result)):
            for j in range(0, 7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("../Icones/add.png"), "Cadastro de Cliente", self)
        btn_ac_adduser.triggered.connect(self.cadClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("../Icones/atualizar.png"), "Atualizar dados do Cliente", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("../Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("../Icones/deletar.png"), "Deletar o Cliente", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        btn_ac_sair = QAction(QIcon("../Icones/sair.png"), "Sair", self)
        # btn_ac_sair.triggered.connect(self.fechaTela)
        btn_ac_sair.setStatusTip("Sair ")
        toolbar.addAction(btn_ac_sair)

        self.show()

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

    def cadClientes(self):
        dlg = CadastroClientes()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchClientes()
        dlg.exec_()

    def delete(self):
        dlg = DeleteCliente()
        dlg.exec_()
        self.loaddata()


class SearchClientes(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchClientes, self).__init__(*args, **kwargs)

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


class DeleteCliente(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteCliente, self).__init__(*args, **kwargs)

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


# Tela principal onde eu chamo as telas de
# cadastro de clientes
# cadastro de Produtos

class DataEntryForm(QWidget):
    def __init__(self):
        super().__init__()

        self.cursor = conexao.banco.cursor()
        consulta_sql = "SELECT * FROM clientes"
        self.cursor.execute(consulta_sql)
        result = self.cursor.fetchall()
        self.close()

        self.cursor = conexao.banco.cursor()
        consulta_prod = "SELECT * FROM produtos"
        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()
        self.close()

        self.preco = 0
        self.TOTAL = 0

        self.items = 0
        self.total = list()
        self.calculaitens = list()
        self._data = {}
        # self._data = {"Phone bill": 50.5, "Gas": 30.0, "Rent": 1850.0,
        #                       "Car Payment": 420.0, "Comcast": 105.0,
        #                       "Public transportation": 60.0, "Coffee": 90.5}

        # DATA DO PEDIDO
        d = QDate.currentDate()
        dataAtual = d.toString(Qt.ISODate)
        data_pedido = str(dataAtual)

        # left side
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        #                                       0         1          2        3            4
        self.table.setHorizontalHeaderLabels(('Cod.', 'Descrição', 'Qtd', 'Preço Un.', 'Sub Total'))
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.layoutRight = QVBoxLayout()

        self.layoutRight.setSpacing(20)

        self.lbl_titulo = QLabel("Caixa")
        self.lbl_titulo.setFont(QFont("Times", 42, QFont.Bold))
        # self.lbl_titulo.setPixmap(QPixmap('Icones/add.png'))
        # self.lbl_titulo.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.layoutRight.addWidget(self.lbl_titulo)

        self.lineEditdata = QLineEdit()
        self.lineEditdata.setText(data_pedido)
        self.layoutRight.addWidget(self.lineEditdata)

        clientes = []
        for i in range(len(result)):
            if result[i][2]:
                clientes.append(result[i][2])

        self.lineEditCliente = QLineEdit()
        self.lineEditCliente.setPlaceholderText('Nome / Razão')
        self.model = QStandardItemModel()
        self.model = clientes
        completer = QCompleter(self.model, self)
        self.lineEditCliente.setCompleter(completer)
        self.lineEditCliente.editingFinished.connect(self.addCliente)
        self.layoutRight.addWidget(self.lineEditCliente)

        produtos = []

        for i in range(len(result_prod)):
            if result_prod[i][1]:
                produtos.append(result_prod[i][1])

        self.lineEditDescription = QLineEdit()
        self.lineEditDescription.setPlaceholderText('Descrição / Produto')
        self.model_prod = QStandardItemModel()
        self.model_prod = produtos
        completer_prod = QCompleter(self.model_prod, self)
        self.lineEditDescription.setCompleter(completer_prod)
        self.lineEditDescription.editingFinished.connect(self.addProdutos)
        self.layoutRight.addWidget(self.lineEditDescription)

        self.lineEditQtd = QLineEdit()
        self.onlyInt = QIntValidator()
        self.lineEditQtd.setValidator(self.onlyInt)
        self.lineEditQtd.setPlaceholderText('Quantidade')

        self.layoutRight.addWidget(self.lineEditQtd)

        self.lineEditPrice = QLineEdit()
        self.onlyFloat = QDoubleValidator()
        self.lineEditPrice.setValidator(self.onlyFloat)
        self.lineEditPrice.setPlaceholderText('R$: Preço')
        self.layoutRight.addWidget(self.lineEditPrice)

        self.lbl_total = QLabel()
        self.lbl_total.setText('R$ 0.00')
        self.lbl_total.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_total.setAlignment(Qt.AlignCenter)
        # self.lbl_total.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.layoutRight.addWidget(self.lbl_total)

        self.buttonAdd = QPushButton("Adicionar", self)
        self.buttonAdd.setIcon(QIcon("../Icones/add.png"))
        self.buttonAdd.setIconSize(QSize(40, 40))
        self.buttonAdd.setMinimumHeight(40)

        self.buttonClear = QPushButton("Cancelar", self)
        self.buttonClear.setIcon(QIcon("../Icones/clear.png"))
        self.buttonClear.setIconSize(QSize(40, 40))
        self.buttonClear.setMinimumHeight(40)

        self.buttonClearOne = QPushButton("Remove", self)
        self.buttonClearOne.setIcon(QIcon("../Icones/clear.png"))
        self.buttonClearOne.setIconSize(QSize(40, 40))
        self.buttonClearOne.setMinimumHeight(40)

        self.buttonefetivar = QPushButton("Efetivar", self)
        self.buttonefetivar.setIcon(QIcon("../Icones/dollars.png"))
        self.buttonefetivar.setIconSize(QSize(40, 40))
        self.buttonefetivar.setMinimumHeight(40)

        self.butotnCupon = QPushButton("Cupon", self)
        self.butotnCupon.setIcon(QIcon("../Icones/impressora.png"))
        self.butotnCupon.setIconSize(QSize(40, 40))
        self.butotnCupon.setMinimumHeight(40)

        self.buttonQuit = QPushButton("Sair", self)
        self.buttonQuit.setIcon(QIcon("../Icones/sair.png"))
        self.buttonQuit.setIconSize(QSize(40, 40))
        self.buttonQuit.setMinimumHeight(40)

        self.buttonAdd.setEnabled(False)

        self.layoutRight.addWidget(self.buttonAdd)
        self.layoutRight.addWidget(self.butotnCupon)
        self.layoutRight.addWidget(self.buttonefetivar)
        self.layoutRight.addWidget(self.buttonClear)
        self.layoutRight.addWidget(self.buttonClearOne)
        self.layoutRight.addWidget(self.buttonQuit)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table, 0)
        self.layout.addLayout(self.layoutRight, 0)

        self.setLayout(self.layout)

        self.buttonQuit.clicked.connect(lambda: self.hide())
        self.buttonClear.clicked.connect(self.reset_table)
        self.buttonClearOne.clicked.connect(self.excluir_dados)
        self.butotnCupon.clicked.connect(self.cupom)
        self.buttonefetivar.clicked.connect(self.efetiva)
        self.buttonAdd.clicked.connect(self.add_entry)

        self.lineEditDescription.textChanged[str].connect(self.check_disable)
        self.lineEditPrice.textChanged[str].connect(self.check_disable)

        self.fill_table()

    def addCliente(self):
        entryItem = self.lineEditCliente.text()
        # print(entryItem[0::])

    def addProdutos(self):

        self.cursor = conexao.banco.cursor()
        consulta_prod = "SELECT * FROM produtos"
        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()

        entryItem = self.lineEditDescription.text()

        for i in range(len(result_prod)):
            if result_prod[i][1] == entryItem:
                self.codigo = result_prod[i][0]
                self.preco = result_prod[i][4]
                self.TOTAL += self.preco
                self.lineEditPrice.setText(str(self.preco))

    def fill_table(self, data=None):
        data = self._data if not data else data

        for desc, price in data.items():
            descItem = QTableWidgetItem(desc)
            priceItem = QTableWidgetItem('${0:.2f}'.format(price))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, descItem)
            self.table.setItem(self.items, 1, priceItem)
            self.items += 1

    def add_entry(self):
        self.sub_total = 0
        if self.table.rowCount() > 0:
            self.calculaitens = []
            linha = self.table.rowCount()
            row = linha
            while row > 0:
                row -= 1
                col = self.table.columnCount()
                resultado = 0
                for x in range(0, col, 1):
                    self.headertext = self.table.horizontalHeaderItem(x).text()
                    if self.headertext == 'Sub Total':
                        cabCol = x
                        resultado = self.table.item(row, cabCol).text()
                        recebe = resultado.replace("R$", "0")
                        self.calculaitens.append(float(recebe))

                self.ttotal = 0
                self.ttotal += sum(self.calculaitens)
                tot_format = ('R${0:.2f} '.format(float(self.ttotal)))
                self.lbl_total.setText(str(tot_format))

        self.cod = self.codigo
        self.desc = self.lineEditDescription.text()
        self.qtd = int(self.lineEditQtd.text())
        self.price = float(self.lineEditPrice.text())
        self.sub_total = float(self.qtd * self.price)
        self.sub_ttotal = str(self.sub_total)

        try:
            codItem = QTableWidgetItem(str(self.cod))
            descItem = QTableWidgetItem(self.desc)

            qtdItem = QTableWidgetItem(str(self.qtd))
            qtdItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            subItem = QTableWidgetItem('R${0:.2f} '.format(float(self.sub_ttotal)))
            subItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            priceItem = QTableWidgetItem('R${0:.2f} '.format(float(self.price)))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, codItem)
            self.table.setItem(self.items, 1, descItem)
            self.table.setItem(self.items, 2, qtdItem)
            self.table.setItem(self.items, 3, priceItem)
            self.table.setItem(self.items, 4, subItem)

            # teste de calculo celula
            # dado um qtablewidget que tem uma linha selecionada ...
            # retorna o valor da coluna na mesma linha que corresponde a um determinado nome de coluna
            # fyi: o nome da coluna diferencia maiúsculas de minúsculas
            row = self.items
            col = self.table.columnCount()
            resultado = 0
            for x in range(0, col, 1):
                self.headertext = self.table.horizontalHeaderItem(x).text()
                if self.headertext == 'Sub Total':
                    cabCol = x
                    resultado = self.table.item(row, cabCol).text()
                    recebe = resultado.replace("R$", "0")
                    self.calculaitens.append(float(recebe))
            self.items += 1
            self.ttotal = 0
            self.ttotal += sum(self.calculaitens)
            tot_format = ('R${0:.2f} '.format(float(self.ttotal)))
            self.lbl_total.setText(str(tot_format))

            self.lineEditDescription.setText('')
            self.lineEditQtd.setText('')
            self.lineEditPrice.setText('')
        except ValueError:
            pass

    def check_disable(self):
        if self.lineEditDescription.text() and self.lineEditPrice.text():
            self.buttonAdd.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)

    def reset_table(self):
        self.table.setRowCount(0)
        self.items = 0
        self.ttotal = 0
        self.preco = 0
        self.TOTAL = 0
        # self.total = []
        self.calculaitens = []
        self.lineEditCliente.setText('')
        self.lineEditDescription.setText('')
        self.lineEditQtd.setText('')
        self.lineEditPrice.setText('')
        self.lbl_total.setText('R$ 0.00')

    # @QtCore.pyqtSlot()
    def excluir_dados(self):
        if self.table.rowCount() > 0:
            linha = self.table.currentRow()
            self.table.removeRow(linha)
            self.items -= 1
            self.lineEditDescription.setText('')
            self.lineEditQtd.setText('')
            self.lineEditPrice.setText('')

            self.calculaitens = []
            linha = self.table.rowCount()
            row = linha
            if row > 0:
                while row > 0:
                    row -= 1
                    col = self.table.columnCount()
                    resultado = 0
                    for x in range(0, col, 1):
                        self.headertext = self.table.horizontalHeaderItem(x).text()
                        if self.headertext == 'Sub Total':
                            cabCol = x
                            resultado = self.table.item(row, cabCol).text()
                            recebe = resultado.replace("R$", "0")
                            self.calculaitens.append(float(recebe))
                    self.ttotal = 0
                    self.ttotal += sum(self.calculaitens)
                    tot_format = ('R${0:.2f} '.format(float(self.ttotal)))
                    self.lbl_total.setText(str(tot_format))
            else:
                self.lbl_total.setText('R$ 0.00')
        else:
            self.lbl_total.setText('R$ 0.00')

    def cupom(self):
        """
        precisa ser implementado ainda
        :return:
        """
        for i in range(self.table.rowCount()):
            cod = self.table.item(i, 0).text()
            text = self.table.item(i, 1).text()
            qtd = float(self.table.item(i, 2).text())
            valUn = float(self.table.item(i, 3).text().replace('R$', ''))
            valTot = float(self.table.item(i, 4).text().replace('R$', ''))

            print(cod)
            print(text)
            print(qtd)
            print(valUn)
            print(valTot)
        print('CUPOM IMPRESSO')

    def numeroPedido(self):
        d = QDate.currentDate()
        data_anterior = str(d.addDays(-1).toString(Qt.ISODate))
        nr_caixa = 0

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM pedidocaixa "
        self.cursor.execute(comando_sql)
        result_data = self.cursor.fetchall()

        print(result_data)
        # datacaixa = result_data[0][7]
        # if datacaixa == :
        #     nr_caixa = result_data[1]
        #     nr_caixa += 1
        # else:
        #     nr_caixa = 1
        # return nr_caixa

    def codigoclientepedido(self):
        nome = self.lineEditCliente.text()
        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT codigo FROM clientes WHERE nome ='{}' ".format(nome)
        self.cursor.execute(comando_sql)
        cod_cli = self.cursor.fetchall()
        codigo = cod_cli[0][0]
        return codigo

    def efetiva(self):

        d = QDate.currentDate()
        dataAtual = d.toString(Qt.ISODate)

        dataAtual = str(dataAtual)
        nr_caixa = self.numeroPedido()
        codigo = self.codigoclientepedido()

        self.cursor = conexao.banco.cursor()
        for i in range(self.table.rowCount()):
            self.cod_prod = self.table.item(i, 0).text()
            self.text = self.table.item(i, 1).text()
            self.qtd = float(self.table.item(i, 2).text())
            self.valUn = float(self.table.item(i, 3).text().replace('R$', ''))
            self.valTot = float(self.table.item(i, 4).text().replace('R$', ''))

            comando_sql = "INSERT INTO pedidocaixa (nr_caixa, cod_produto, cod_vendedor, cod_cliente, quantidade," \
                          "valor_total, ultupdate) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            dados = nr_caixa, self.cod_prod, 1, codigo, self.qtd, self.valTot, dataAtual
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()

        print('PEDIDO EFETIVADO')


class MainWindow(QMainWindow):
    def __init__(self, w):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon('../Icones/perfil.png'))

        # cria um menu
        file_menu = self.menuBar().addMenu("&Arquivo")
        help_menu = self.menuBar().addMenu("&Ajuda")
        self.setCentralWidget(w)

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE")
        self.setMinimumSize(800, 600)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("../Icones/clientes.png"), "Listar/Cadastrar de Cliente", self)
        btn_ac_adduser.triggered.connect(self.listClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_produto = QAction(QIcon("../Icones/produtos2.png"), "Lista/Cadastrar Produtos", self)
        btn_ac_produto.triggered.connect(self.listProdutos)
        btn_ac_produto.setStatusTip("Produtos")
        toolbar.addAction(btn_ac_produto)

        btn_ac_estoque = QAction(QIcon("../Icones/estoque.png"), "Lista/Cadastro Estoque", self)
        btn_ac_estoque.triggered.connect(self.listEstoque)
        btn_ac_estoque.setStatusTip("Estoque")
        toolbar.addAction(btn_ac_estoque)

        btn_ac_caixa = QAction(QIcon("../Icones/dollars.png"), "Caixa - abre o Caixa", self)
        btn_ac_caixa.triggered.connect(self.caixa)
        btn_ac_caixa.setStatusTip("Caixa")
        toolbar.addAction(btn_ac_caixa)

        btn_ac_fechar = QAction(QIcon("../Icones/sair.png"), "Sair", self)
        btn_ac_fechar.triggered.connect(self.fechaTela)
        btn_ac_fechar.setStatusTip("Sair")
        toolbar.addAction(btn_ac_fechar)

        # Arquivo >> Adicionar
        adduser_action = QAction(QIcon("../Icones/clientes.png"), "Listar/Cadastrar de Cliente", self)
        adduser_action.triggered.connect(self.listClientes)
        file_menu.addAction(adduser_action)

        btn_ac_produto = QAction(QIcon("../Icones/produtos2.png"), "Listar/Cadastrar Produtos", self)
        btn_ac_produto.triggered.connect(self.listProdutos)
        file_menu.addAction(btn_ac_produto)

        btn_ac_estoque = QAction(QIcon("../Icones/estoque.png"), "Lista/Cadastro Estoque", self)
        btn_ac_estoque.triggered.connect(self.listEstoque)
        file_menu.addAction(btn_ac_estoque)

        btn_ac_caixa = QAction(QIcon("../Icones/dollars.png"), "Caixa", self)
        btn_ac_caixa.triggered.connect(self.caixa)
        file_menu.addAction(btn_ac_caixa)

        btn_ac_fechar = QAction(QIcon("../Icones/sair.png"), "Sair", self)
        btn_ac_fechar.setShortcut('Ctrl+Q')
        btn_ac_fechar.triggered.connect(self.fechaTela)
        file_menu.addAction(btn_ac_fechar)

        about_action = QAction(QIcon("../Icones/sobre-nos.png"), "Desenvolvedores", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # export to csv file action
        export_Action = QAction('Export to CSV', self)
        export_Action.setShortcut('Ctrl+E')
        export_Action.triggered.connect(self.export_to_csv)
        file_menu.addAction(export_Action)

        self.show()
        # self.showFullScreen()

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def caixa(self):
        self.hide()
        dlg = telaprincipal()
        dlg.exec()

    def listClientes(self):
        dlg = ListClientes()
        dlg.exec()

    def listProdutos(self):
        dlg = ListProdutos()
        dlg.exec()

    def listEstoque(self):
        dlg = ListEstoque()
        dlg.exec()

    def fechaTela(self, event):
        replay = QMessageBox.question(self, 'Window close', 'Tem certeza de que deseja sair?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            sys.exit()

        else:
            event.ignore()

    def export_to_csv(self, w):
        try:
            with open('../sql/Expense Report.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((w.table.horizontalHeaderItem(0).text(), w.table.horizontalHeaderItem(1).text()))
                for rowNumber in range(w.table.rowCount()):
                    writer.writerow([w.table.item(rowNumber, 0).text(), w.table.item(rowNumber, 1).text()])
                print('CSV file exported.')
            file.close()
        except Exception as e:
            print(e)


def telaprincipal():
    w = DataEntryForm()
    dlg = MainWindow(w)
    dlg.exec_()


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

        usuario = self.lineEdit_username.text()
        senha = self.lineEdit_senha.text()
        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT senha FROM usuarios WHERE nome ='{}' ".format(usuario)

        try:
            self.cursor.execute(comando_sql)
            senha_bd = self.cursor.fetchall()

        except Exception as e:
            msg.setText("Credenciais Incorretas")
            msg.exec_()

        if senha == senha_bd[0][0]:
            self.hide()
            telaprincipal()
            msg.setText("Sucesso")
            msg.exec_()
            conexao.banco.close()
        else:
            msg.setText("Credenciais Incorretas")
            msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

if QDialog.Accepted:
    form = LoginForm()
    form.show()

sys.exit((app.exec_()))
