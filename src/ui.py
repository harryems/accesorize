# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Mon Mar 11 17:05:12 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTest = QtGui.QMenu(self.menubar)
        self.menuTest.setObjectName(_fromUtf8("menuTest"))
        self.menuCatalogo = QtGui.QMenu(self.menubar)
        self.menuCatalogo.setObjectName(_fromUtf8("menuCatalogo"))
        self.menuConfiguracion = QtGui.QMenu(self.menubar)
        self.menuConfiguracion.setObjectName(_fromUtf8("menuConfiguracion"))
        self.menuCaptura = QtGui.QMenu(self.menubar)
        self.menuCaptura.setObjectName(_fromUtf8("menuCaptura"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionMore_tes = QtGui.QAction(MainWindow)
        self.actionMore_tes.setObjectName(_fromUtf8("actionMore_tes"))
        self.actionCargar_Catalogo = QtGui.QAction(MainWindow)
        self.actionCargar_Catalogo.setObjectName(_fromUtf8("actionCargar_Catalogo"))
        self.actionCaptura_de_articulos = QtGui.QAction(MainWindow)
        self.actionCaptura_de_articulos.setObjectName(_fromUtf8("actionCaptura_de_articulos"))
        self.actionCargar_Catalogo_2 = QtGui.QAction(MainWindow)
        self.actionCargar_Catalogo_2.setObjectName(_fromUtf8("actionCargar_Catalogo_2"))
        self.menuTest.addAction(self.actionMore_tes)
        self.menuTest.addSeparator()
        self.menuCatalogo.addAction(self.actionCargar_Catalogo)
        self.menuCaptura.addAction(self.actionCaptura_de_articulos)
        self.menubar.addAction(self.menuTest.menuAction())
        self.menubar.addAction(self.menuCatalogo.menuAction())
        self.menubar.addAction(self.menuCaptura.menuAction())
        self.menubar.addAction(self.menuConfiguracion.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionCargar_Catalogo, QtCore.SIGNAL(_fromUtf8("changed()")), MainWindow.close)
        QtCore.QObject.connect(self.actionMore_tes, QtCore.SIGNAL(_fromUtf8("changed()")), self.centralwidget.deleteLater)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuTest.setTitle(_translate("MainWindow", "Archivo", None))
        self.menuCatalogo.setTitle(_translate("MainWindow", "Catalogo", None))
        self.menuConfiguracion.setTitle(_translate("MainWindow", "Configuracion", None))
        self.menuCaptura.setTitle(_translate("MainWindow", "Captura", None))
        self.actionMore_tes.setText(_translate("MainWindow", "Abrir Sesion", None))
        self.actionCargar_Catalogo.setText(_translate("MainWindow", "Cargar Catalogo", None))
        self.actionCaptura_de_articulos.setText(_translate("MainWindow", "Captura de articulos", None))
        self.actionCargar_Catalogo_2.setText(_translate("MainWindow", "Cargar Catalogo", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

