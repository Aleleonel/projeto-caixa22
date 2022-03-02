#!/usr/bin/env python3
import sys, os
from prettytable import PrettyTable
from prettytable import PLAIN_COLUMNS  # MSWORD_FRIENDLY
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QTextEdit


class SendMessage(QWidget):
    def __init__(self):
        super().__init__()
        self.black = "#000000"
        self.yellow = "#cfb119"
        """self.setStyleSheet(
              f"background-color:{self.black}; color: {self.yellow}"
              )"""
        self.hbox = QHBoxLayout()

        self.rw = PrettyTable()
        self.rw.field_names = ["Cod.", "Descrição", "Quant.", "Preco unit.", "Subtotal"]
        try:
            with open("print.pdf", "r") as msg:
                self.lin = [x.strip().split(",") for x in msg]

                self.a = [self.lin[x] for x in range(len(self.lin))]

                total = 0
                for x in self.a:
                    total += float(x[len(self.a) - 1])
                    self.rw.set_style(PLAIN_COLUMNS)
                    self.rw.add_row(x)
                print(self.rw)
                msg.close()
        except Exception as e:
            self.errors(e)

        empresa = "LOJA VENDEDORA"
        text = f'\nTOTAL {total:>80} \n{empresa:^90} \nEndereço: \nTelefone: '

        newGroup = QGroupBox("LISTA DE PRODUTOS")
        newGroup.setStyleSheet(f"background-color: {self.black}; color: {self.yellow}")

        self.hbox2 = QHBoxLayout()
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setText(f"{self.rw} \n{text}")
        self.hbox2.addWidget(self.text)

        newGroup.setLayout(self.hbox2)
        layout = QVBoxLayout(self)
        layout.addWidget(newGroup)
        layout.addLayout(self.hbox)
        self.show()

    def errors(self, e):
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err = f"{e} \n{exc_type} \n{fname} \n{exc_tb.tb_lineno} \n"
        print(err)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sm = SendMessage()
    sm.show()
    app.exec()
