from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Photo Crypto")
        self.setGeometry(100, 100, 850, 600)
        self.downloadPath = None

        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl("http://localhost:8080/photo-rsa/build/"))
        self.browser.reload()
        self.browser.page().profile().downloadRequested.connect(self.download)

        self.setCentralWidget(self.browser)

        self.show()
    
    def download(self, item):
        if not self.downloadPath:
            self.downloadPath = str(QFileDialog.getExistingDirectory(self, "select directory to download files"))
        item.setDownloadDirectory(self.downloadPath)
        print('downloading to', item.path())
        item.accept()

def startgui():
    app = QApplication(sys.argv)
    window = MainWindow()

    app.exec_()

if __name__ == "__main__":
    startgui()