from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.setWindowTitle("Photo Crypto")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl("http://localhost:8080/photo-rsa/build/"))
        self.browser.page().profile().downloadRequested.connect(self.download)

        self.setCentralWidget(self.browser)

        self.show()
    
    def download(self, item):
        print('downloading to', item.path())
        item.accept()

def startgui():
    app = QApplication(sys.argv)
    window = MainWindow()

    app.exec_()

if __name__ == "__main__":
    startgui()