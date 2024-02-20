from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_BrickDetector
from model.camera import BrickDetector

import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_BrickDetector()
    detector = BrickDetector(ui)
    ui.setupUi(detector)
    ui.show()
    sys.exit(app.exec_())