# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lhy.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVtkWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 60))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.niiPath = QtWidgets.QLineEdit(self.widget)
        self.niiPath.setObjectName("niiPath")
        self.horizontalLayout.addWidget(self.niiPath)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout_3.addWidget(self.widget)
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.paintMethod = QtWidgets.QComboBox(self.widget_3)
        self.paintMethod.setObjectName("paintMethod")
        self.paintMethod.addItem("")
        self.paintMethod.addItem("")
        self.horizontalLayout_3.addWidget(self.paintMethod)
        self.runButton = QtWidgets.QPushButton(self.widget_3)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout_3.addWidget(self.runButton)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.vtkWidget = QVtkWidget(self.widget_2)
        self.vtkWidget.setObjectName("openGLWidget")
        self.horizontalLayout_2.addWidget(self.vtkWidget)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LHY"))
        self.label.setText(_translate("MainWindow", "nii路径"))
        self.pushButton.setText(_translate("MainWindow", "打开"))
        self.label_2.setText(_translate("MainWindow", "渲染方式"))
        self.paintMethod.setItemText(0, _translate("MainWindow", "管线投影算法"))
        self.paintMethod.setItemText(1, _translate("MainWindow", "移动立方算法"))
        self.runButton.setText(_translate("MainWindow", "渲染"))
