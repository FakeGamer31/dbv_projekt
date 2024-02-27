# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiTest.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from model.camera import ImageMode
from about import Ui_about_dialog

import re


class Ui_BrickDetector(QtWidgets.QMainWindow):
    def setupUi(self, detector):
        self.detector = detector
        self.setObjectName("BrickDetector")
        self.resize(960, 720)
        self.setMinimumSize(QtCore.QSize(960, 720))
        self.setMaximumSize(QtCore.QSize(960, 720))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.camera_settings_box = QtWidgets.QGroupBox(self.centralwidget)
        self.camera_settings_box.setEnabled(True)
        self.camera_settings_box.setGeometry(QtCore.QRect(680, 30, 251, 251))
        self.camera_settings_box.setObjectName("camera_settings_box")
        self.focus_slider = QtWidgets.QSlider(self.camera_settings_box)
        self.focus_slider.setEnabled(False)
        self.focus_slider.setGeometry(QtCore.QRect(10, 60, 181, 22))
        self.focus_slider.setMouseTracking(False)
        self.focus_slider.setMaximum(255)
        self.focus_slider.setSingleStep(5)
        self.focus_slider.setOrientation(QtCore.Qt.Horizontal)
        self.focus_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.focus_slider.setObjectName("focus_slider")
        self.focus_label = QtWidgets.QLabel(self.camera_settings_box)
        self.focus_label.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.focus_label.setObjectName("focus_label")
        self.autofocus_checkbox = QtWidgets.QCheckBox(self.camera_settings_box)
        self.autofocus_checkbox.setGeometry(QtCore.QRect(10, 20, 100, 17))
        self.autofocus_checkbox.setChecked(True)
        self.autofocus_checkbox.setObjectName("autofocus_checkbox")
        self.static_radio = QtWidgets.QRadioButton(self.camera_settings_box)
        self.static_radio.setGeometry(QtCore.QRect(10, 224, 82, 17))
        self.static_radio.setObjectName("static_radio")
        self.image_mode_group = QtWidgets.QButtonGroup(self)
        self.image_mode_group.setObjectName("image_mode_group")
        self.image_mode_group.addButton(self.static_radio)
        self.live_radio = QtWidgets.QRadioButton(self.camera_settings_box)
        self.live_radio.setGeometry(QtCore.QRect(10, 204, 82, 17))
        self.live_radio.setChecked(True)
        self.live_radio.setObjectName("live_radio")
        self.image_mode_group.addButton(self.live_radio)
        self.image_label = QtWidgets.QLabel(self.camera_settings_box)
        self.image_label.setGeometry(QtCore.QRect(10, 184, 81, 16))
        self.image_label.setObjectName("image_label")
        self.contrast_slider = QtWidgets.QSlider(self.camera_settings_box)
        self.contrast_slider.setGeometry(QtCore.QRect(10, 110, 181, 22))
        self.contrast_slider.setMouseTracking(False)
        self.contrast_slider.setMaximum(255)
        self.contrast_slider.setSingleStep(5)
        self.contrast_slider.setOrientation(QtCore.Qt.Horizontal)
        self.contrast_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.contrast_slider.setObjectName("contrast_slider")
        self.contrast_slider.setValue(128)
        self.contrast_label = QtWidgets.QLabel(self.camera_settings_box)
        self.contrast_label.setGeometry(QtCore.QRect(10, 90, 100, 13))
        self.contrast_label.setObjectName("contrast_label")
        self.brigthness_label = QtWidgets.QLabel(self.camera_settings_box)
        self.brigthness_label.setGeometry(QtCore.QRect(10, 140, 100, 20))
        self.brigthness_label.setObjectName("brigthness_label")
        self.brigthness_slider = QtWidgets.QSlider(self.camera_settings_box)
        self.brigthness_slider.setGeometry(QtCore.QRect(10, 160, 181, 22))
        self.brigthness_slider.setMouseTracking(False)
        self.brigthness_slider.setMaximum(255)
        self.brigthness_slider.setSingleStep(5)
        self.brigthness_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brigthness_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.brigthness_slider.setObjectName("brigthness_slider")
        self.brigthness_slider.setValue(128)
        self.focus_line_edit = QtWidgets.QLineEdit(self.camera_settings_box)
        self.focus_line_edit.setMaxLength(3)
        self.focus_line_edit.setGeometry(QtCore.QRect(200, 60, 31, 20))
        self.focus_line_edit.setObjectName("focus_line_edit")
        self.focus_line_edit.setReadOnly(True)
        self.contrast_line_edit = QtWidgets.QLineEdit(self.camera_settings_box)
        self.contrast_line_edit.setGeometry(QtCore.QRect(200, 110, 31, 20))
        self.contrast_line_edit.setMaxLength(3)
        self.contrast_line_edit.setObjectName("contrast_line_edit")
        self.brigthness_line_edit = QtWidgets.QLineEdit(self.camera_settings_box)
        self.brigthness_line_edit.setGeometry(QtCore.QRect(200, 160, 31, 20))
        self.brigthness_line_edit.setMaxLength(3)
        self.brigthness_line_edit.setClearButtonEnabled(False)
        self.brigthness_line_edit.setObjectName("brigthness_line_edit")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(830, 530, 341, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.video_image_label = QtWidgets.QLabel(self.centralwidget)
        self.video_image_label.setGeometry(QtCore.QRect(10, 20, 640, 480))
        self.video_image_label.setMinimumSize(QtCore.QSize(640, 480))
        self.video_image_label.setMaximumSize(QtCore.QSize(640, 480))
        self.video_image_label.setText("")
        self.video_image_label.setPixmap(QtGui.QPixmap(""))
        self.video_image_label.setScaledContents(True)
        self.video_image_label.setObjectName("video_image_label")
        self.brick_list_text_area = QtWidgets.QTextEdit(self.centralwidget)
        self.brick_list_text_area.setGeometry(QtCore.QRect(5, 510, 951, 161))
        self.brick_list_text_area.setReadOnly(True)
        self.brick_list_text_area.setOverwriteMode(False)
        self.brick_list_text_area.setObjectName("brick_list_text_area")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(750, 290, 101, 51))
        self.search_button.setObjectName("search_button")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHow_to_use = QtWidgets.QAction(self)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.menuFile.addAction(self.actionOpen)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionHow_to_use)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.focus_label.setBuddy(self.focus_slider)
        self.contrast_label.setBuddy(self.focus_slider)
        self.brigthness_label.setBuddy(self.focus_slider)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(detector.loop)
        self.timer.start(30)  # Aktualisiere alle 30 Millisekunden

        self.retranslateUi()
        self.search_button.clicked['bool'].connect(self.startDetection)

        self.live_radio.toggled['bool'].connect(self.set_image_mode)

        self.autofocus_checkbox.stateChanged.connect(self.disable_enable_autofocus_slider)
        self.autofocus_checkbox.stateChanged.connect(self.toggle_autofocus)

        self.focus_slider.valueChanged.connect(self.set_slider_values)
        self.contrast_slider.valueChanged.connect(self.set_slider_values)
        self.brigthness_slider.valueChanged.connect(self.set_slider_values)

        self.focus_line_edit.textEdited.connect(self.set_box_values)
        self.contrast_line_edit.textEdited.connect(self.set_box_values)
        self.brigthness_line_edit.textEdited.connect(self.set_box_values)

        self.actionAbout.triggered.connect(self.open_about)

        self.actionOpen.triggered.connect(self.open_file)
        QtCore.QMetaObject.connectSlotsByName(self)

    def open_about(self):
        about_dialog = Ui_about_dialog()
        about_dialog.setupUi()
        about_dialog.exec_()

    def open_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', 'Images files (*.jpg *.png)')
        self.video_image_label.setPixmap(QtGui.QPixmap(fname[0]))
        self.detector.img_path = fname[0]
        self.detector.detect_flag = True
        self.static_radio.toggle()

    def set_image_mode(self):
        if self.live_radio.isChecked():
            self.detector.image_mode = ImageMode.live
        else:
            self.detector.image_mode = ImageMode.static
            self.detector.detect_flag = True

    def disable_enable_autofocus_slider(self):
        if (self.autofocus_checkbox.checkState() == 0):
            self.focus_slider.setEnabled(True)
            self.focus_line_edit.setReadOnly(False)
        else:
            self.focus_slider.setDisabled(True)
            self.focus_line_edit.setReadOnly(True)

    def set_slider_values(self):
        self.detector.focus = self.focus_slider.value()
        self.detector.brigthness = self.brigthness_slider.value()
        self.detector.contrast = self.contrast_slider.value()

        self.focus_line_edit.setText(str(self.focus_slider.value()))
        self.brigthness_line_edit.setText(str(self.brigthness_slider.value()))
        self.contrast_line_edit.setText(str(self.contrast_slider.value()))

    def set_box_values(self):
        if (re.search("^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})?$", self.focus_line_edit.text())):
            if (self.focus_line_edit.text() == ''):
                self.focus_slider.setValue(0)
            else:
                self.focus_slider.setValue(int(self.focus_line_edit.text()))
        else:
            self.focus_slider.setValue(0)
            
        if (re.search("^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})?$", self.brigthness_line_edit.text())):
            if (self.brigthness_line_edit.text() == ''):
                self.brigthness_slider.setValue(0)
            else:
                self.brigthness_slider.setValue(int(self.brigthness_line_edit.text()))
        else:
            self.brigthness_slider.setValue(0)
                
        if (re.search("^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})?$", self.contrast_line_edit.text())):
            if (self.contrast_line_edit.text() == ''):
                self.contrast_slider.setValue(0)
            else:
                self.contrast_slider.setValue(int(self.contrast_line_edit.text()))
        else:
            self.contrast_slider.setValue(0)
           

    def toggle_autofocus(self):
        self.detector.autofocus = self.autofocus_checkbox.isChecked()

    def startDetection(self):
        self.detector.show_brick_list = True

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("BrickDetector", "Brick Detector"))
        self.setWindowIcon(QtGui.QIcon('ui/favicon.png'))
        self.camera_settings_box.setTitle(_translate("BrickDetector", "Camera settings"))
        self.focus_label.setText(_translate("BrickDetector", "Focus"))
        self.autofocus_checkbox.setText(_translate("BrickDetector", "Autofocus"))
        self.static_radio.setText(_translate("BrickDetector", "Static"))
        self.live_radio.setText(_translate("BrickDetector", "Live"))
        self.image_label.setText(_translate("BrickDetector", "Image mode"))
        self.contrast_label.setText(_translate("BrickDetector", "Contrast"))
        self.brigthness_label.setText(_translate("BrickDetector", "Brigthness"))
        self.focus_line_edit.setText(_translate("BrickDetector", "128"))
        self.contrast_line_edit.setText(_translate("BrickDetector", "128"))
        self.brigthness_line_edit.setText(_translate("BrickDetector", "128"))
        self.brick_list_text_area.setPlaceholderText(_translate("BrickDetector", "Bricklist:"))
        self.search_button.setText(_translate("BrickDetector", "Search"))
        self.menuFile.setTitle(_translate("BrickDetector", "File"))
        self.menuAbout.setTitle(_translate("BrickDetector", "Help"))
        self.actionOpen.setText(_translate("BrickDetector", "Open"))
        self.actionAbout.setText(_translate("BrickDetector", "About"))
        self.actionHow_to_use.setText(_translate("BrickDetector", "How to use"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     BrickDetector = QtWidgets.QMainWindow()
#     ui = Ui_BrickDetector()
#     ui.setupUi(BrickDetector)
#     BrickDetector.show()
#     sys.exit(app.exec_())
