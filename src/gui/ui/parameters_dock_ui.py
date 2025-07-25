# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameters_dock.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ParametersDock(object):
    def setupUi(self, ParametersDock):
        ParametersDock.setObjectName("ParametersDock")
        ParametersDock.resize(189, 396)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.matrixLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.matrixLabel.setObjectName("matrixLabel")
        self.horizontalLayout_4.addWidget(self.matrixLabel)
        self.matrixLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.matrixLineEdit.setObjectName("matrixLineEdit")
        self.horizontalLayout_4.addWidget(self.matrixLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.mutationLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.mutationLabel.setObjectName("mutationLabel")
        self.horizontalLayout_9.addWidget(self.mutationLabel)
        self.mutationLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.mutationLineEdit.setObjectName("mutationLineEdit")
        self.horizontalLayout_9.addWidget(self.mutationLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.crossoverLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.crossoverLabel.setObjectName("crossoverLabel")
        self.horizontalLayout_10.addWidget(self.crossoverLabel)
        self.crossoverineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.crossoverineEdit.setObjectName("crossoverineEdit")
        self.horizontalLayout_10.addWidget(self.crossoverineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.stepsAmountLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.stepsAmountLabel.setObjectName("stepsAmountLabel")
        self.horizontalLayout_7.addWidget(self.stepsAmountLabel)
        self.stepsAmountSpinBox = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.stepsAmountSpinBox.setObjectName("stepsAmountSpinBox")
        self.horizontalLayout_7.addWidget(self.stepsAmountSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.populationLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.populationLabel.setObjectName("populationLabel")
        self.horizontalLayout_12.addWidget(self.populationLabel)
        self.populationSpinBox = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.populationSpinBox.setObjectName("populationSpinBox")
        self.horizontalLayout_12.addWidget(self.populationSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.mutation = QtWidgets.QCheckBox(self.dockWidgetContents)
        self.mutation.setObjectName("mutation")
        self.verticalLayout.addWidget(self.mutation)
        self.crossing = QtWidgets.QCheckBox(self.dockWidgetContents)
        self.crossing.setObjectName("crossing")
        self.verticalLayout.addWidget(self.crossing)
        spacerItem = QtWidgets.QSpacerItem(20, 118, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.goButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.goButton.setMinimumSize(QtCore.QSize(0, 50))
        self.goButton.setObjectName("goButton")
        self.verticalLayout.addWidget(self.goButton)
        ParametersDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(ParametersDock)
        QtCore.QMetaObject.connectSlotsByName(ParametersDock)

    def retranslateUi(self, ParametersDock):
        _translate = QtCore.QCoreApplication.translate
        ParametersDock.setWindowTitle(_translate("ParametersDock", "Parameters"))
        self.matrixLabel.setText(_translate("ParametersDock", "Matrix:"))
        self.mutationLabel.setText(_translate("ParametersDock", "Mutation rate:"))
        self.crossoverLabel.setText(_translate("ParametersDock", "Crossover rate:"))
        self.stepsAmountLabel.setText(_translate("ParametersDock", "Steps amount"))
        self.populationLabel.setText(_translate("ParametersDock", "Population size"))
        self.mutation.setText(_translate("ParametersDock", "Mutation by reversal"))
        self.crossing.setText(_translate("ParametersDock", "Use Tournament"))
        self.goButton.setText(_translate("ParametersDock", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParametersDock = QtWidgets.QDockWidget()
    ui = Ui_ParametersDock()
    ui.setupUi(ParametersDock)
    ParametersDock.show()
    sys.exit(app.exec_())
