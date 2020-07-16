#!/usr/bin/env python
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib as mpl
import math
mpl.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import calculation as calc
import material

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

UsingMaterial = material.steel
accuracy = 1000

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyStaticMplCanvas(MyMplCanvas):

    def update_compute(self, n):
        global UsingMaterial
        x, y = calc.calc(n, UsingMaterial)
        self.axes.plot(x, y, '+')
        self.axes.plot(x, y)
        self.draw()

    def build(self):
        global UsingMaterial, accuracy
        x, y = calc.calc(accuracy, UsingMaterial)
        self.axes.plot(x, y)
        self.draw()

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("МКЭ")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        self.sc = MyStaticMplCanvas(self.main_widget, width=10, height=8, dpi=100)
        l.addWidget(self.sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Задайте N", 50000)

        self.button = QtWidgets.QPushButton('ВЫЧИСЛИТЬ', self)
        self.input = QtWidgets.QLineEdit(self)
        self.button.clicked.connect(self.handleButton)
        self.button1 = QtWidgets.QPushButton('Aluminum', self)
        self.button1.clicked.connect(self.chooseAluminum)
        self.button2 = QtWidgets.QPushButton('Steel', self)
        self.button2.clicked.connect(self.chooseSteel)
        self.button3 = QtWidgets.QPushButton('Silver', self)
        self.button3.clicked.connect(self.chooseSilver)
        self.button4 = QtWidgets.QPushButton('Plumbum', self)
        self.button4.clicked.connect(self.choosePlumbum)
        self.button5 = QtWidgets.QPushButton('Cuprum', self)
        self.button5.clicked.connect(self.chooseCuprum)
        l.addWidget(self.input)
        l.addWidget(self.button)
        l.addWidget(self.button1)
        l.addWidget(self.button2)
        l.addWidget(self.button3)
        l.addWidget(self.button4)
        l.addWidget(self.button5)

    def chooseAluminum(self):
        global UsingMaterial
        UsingMaterial = material.aluminum
        self.sc.build()

       
    def chooseSteel(self):
        global UsingMaterial
        UsingMaterial = material.steel
        self.sc.build()
      
    def choosePlumbum(self):
        global UsingMaterial
        UsingMaterial = material.plumbum
        self.sc.build()
     
    def chooseSilver(self):
        global UsingMaterial
        UsingMaterial = material.silver
        self.sc.build()
       
    def chooseCuprum(self):
        global UsingMaterial
        UsingMaterial = material.cuprum
        self.sc.build()

    def handleButton(self):
        number = self.input.text()
        try:
            number = int(number)
            self.sc.update_compute(number)
        except Exception:
            print(Exception)
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Введите целое число')
            pass

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", 'ВМК')


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % "PracticeProject")
aw.show()
sys.exit(qApp.exec_())
