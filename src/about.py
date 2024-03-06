# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\about.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_about_dialog(QtWidgets.QDialog):
    def setupUi(self):
        self.setObjectName("about_dialog")
        self.resize(400, 300)
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.setMaximumSize(QtCore.QSize(400, 300))
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(120, 130, 200, 61))
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.text_label = QtWidgets.QLabel(self.frame)
        self.text_label.setGeometry(QtCore.QRect(140, 80, 200, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.text_label.setFont(font)
        self.text_label.setScaledContents(False)
        self.text_label.setObjectName("text_label")
        self.hsb_logo_label = QtWidgets.QLabel(self.frame)
        self.hsb_logo_label.setGeometry(QtCore.QRect(130, 0, 150, 80))
        self.hsb_logo_label.setText("")
        self.hsb_logo_label.setPixmap(QtGui.QPixmap("../ui/HSB_Logo_Farbe_sRGB.svg"))
        self.hsb_logo_label.setScaledContents(True)
        self.hsb_logo_label.setObjectName("hsb_logo_label")
        self.ok_button = QtWidgets.QDialogButtonBox(self.frame)
        self.ok_button.setGeometry(QtCore.QRect(140, 260, 130, 30))
        self.ok_button.setOrientation(QtCore.Qt.Horizontal)
        self.ok_button.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.ok_button.setCenterButtons(True)
        self.ok_button.setObjectName("ok_button")

        self.retranslateUi()
        self.setWindowIcon(QtGui.QIcon('../ui/favicon.png'))
        self.ok_button.accepted.connect(self.accept) # type: ignore
        self.ok_button.rejected.connect(self.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("about_dialog", "About"))
        self.label.setText(_translate("about_dialog", "Created by                             Yusuf Akbulut & Gunnar Martens"))
        self.text_label.setText(_translate("about_dialog", "Brick Detector"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     about_dialog = QtWidgets.QDialog()
#     ui = Ui_about_dialog()
#     ui.setupUi(about_dialog)
#     about_dialog.show()
#     sys.exit(app.exec_())
