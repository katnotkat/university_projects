from StartPage import *
import sys
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    sys.exit(app.exec_())
