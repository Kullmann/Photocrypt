"""
GUI Program
"""

from os.path import dirname, realpath, join, isfile
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QPushButton, QMessageBox, QErrorMessage
from PyQt5.QtGui import QPixmap
from photocrypt.crypto.RSA import generate_key, save_keypair

GREEN_BUTTON_STYLE = """
QPushButton {
background-color: #28a745;
color: #ffffff;
border-radius: 10px;
}
QPushButton:hover { background-color: #218838 }
QPushButton:pressed {
    background-color: #218838;
    border: 3px solid #1e7e34;
}
"""
BLUE_BUTTON_STYLE = """
QPushButton {
    background-color: #007bff;
    color: #ffffff;
    border-radius: 10px;
}
QPushButton:hover { background-color: #0069d9 }
QPushButton:pressed {
    background-color: #0069d9;
    border: 3px solid #0062cc;
}
"""


class MainWindow(QMainWindow):
    """
    Main window
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color:#315d90; font: 12pt Helvetica;")
        self.setWindowTitle("Photo Crypto")
        self.setGeometry(3500, 500, 850, 600)
        self.workingdir = dirname(realpath(__file__))

        self.title = QLabel(
            "AES-128 Photo Encryption wrapped with RSA-2048", self)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 30pt; color: #d3e1ed")
        self.title.resize(700, 200)
        self.title.move(120, 30)

        icon_image = QPixmap()
        icon_image.load(join(self.workingdir, 'resource', 'icon.png'))
        self.icon = QLabel(self)
        self.icon.setPixmap(icon_image)
        self.icon.resize(icon_image.width(), icon_image.height())
        self.icon.move(60, 80)

        self.subtitle = QLabel("Created by Hosung Lee and Sean Kullmann", self)
        self.subtitle.setStyleSheet("font: 10pt; color: #d3e1ed")
        self.subtitle.resize(self.subtitle.sizeHint().width(),
                             self.subtitle.sizeHint().height())
        self.subtitle.move(self.width() // 2 -
                           self.subtitle.sizeHint().width() // 2, 220)

        self.rbutton = QPushButton("Generate RSA public and private key", self)
        self.rbutton.resize(self.rbutton.sizeHint().width(),
                            self.rbutton.sizeHint().height())
        self.rbutton.setStyleSheet(GREEN_BUTTON_STYLE)
        self.rbutton.move(self.width() // 2 -
                          self.rbutton.sizeHint().width() // 2, 300)
        self.rbutton.clicked.connect(self.generate_key)

        self.ebutton = QPushButton("Encrypt", self)
        self.ebutton.resize(self.ebutton.sizeHint().width(),
                            self.ebutton.sizeHint().height())
        self.ebutton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.ebutton.move(120, 350)

        self.dbutton = QPushButton("Decrypt", self)
        self.dbutton.resize(self.dbutton.sizeHint().width(),
                            self.dbutton.sizeHint().height())
        self.dbutton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.dbutton.move(220, 350)

        self.show()

    def generate_key(self):
        path_to_save = self.get_directory()
        if path_to_save == "":
            return
        private_file = join(path_to_save, "private.pem")
        public_file = join(path_to_save, "public.pem")
        if isfile(private_file) or isfile(public_file):
            self.popup_message(
                "Error", "private.pem or public.pem is already in the directory")
            return
        save_keypair(generate_key(), (private_file, public_file))
        self.popup_message(
            "Success", "private.pem or public.pem saved in the directory")

    def popup_message(self, title, text):
        dialog = QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.exec_()

    def get_directory(self):
        path = str(QFileDialog.getExistingDirectory(
            self, "select directory to download files"))
        return path

    def get_open_file(self):
        path = str(QFileDialog.getOpenFileName(self, "select file"))
        return path

    def get_save_file(self):
        path = str(QFileDialog.getOpenFileName(self, "select file"))
        return path


def startgui():
    app = QApplication(sys.argv)
    window = MainWindow()

    app.exec_()


if __name__ == "__main__":
    startgui()
