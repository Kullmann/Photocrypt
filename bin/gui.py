"""
GUI Program
"""

import sys
from os.path import dirname, isfile, join, realpath

from photocrypt.crypto.RSA import generate_key, save_keypair, load_key
from photocrypt.utils import keymgr
from photocrypt import encrypt_image, decrypt_image, open_image
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QErrorMessage, QFileDialog,
                             QFormLayout, QGroupBox, QHBoxLayout, QLineEdit,
                             QLabel, QMainWindow, QMessageBox, QPushButton,
                             QScrollArea, QVBoxLayout, QWidget)
import outlook

from styles import green_button_style, blue_button_style, disabled_button_style
WORKING_DIRECTORY = dirname(realpath(__file__))
class MainWindow(QMainWindow):
    """
    Main window
    """

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setStyleSheet("background-color:#315d90; font: 12pt Helvetica; color: #d3e1ed")
        self.setWindowTitle("Photo Crypto")
        self.resize(850, 600)
        

        self.title = QLabel(
            "AES-128 Photo Encryption wrapped with RSA-2048", self)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 30pt;")
        self.title.resize(700, 200)
        self.title.move(120, 30)

        icon_image = QPixmap()
        icon_image.load(join(WORKING_DIRECTORY, 'resource', 'icon.png'))
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
        self.rbutton.resize(self.rbutton.sizeHint().width(), self.rbutton.sizeHint().height())
        self.rbutton.setStyleSheet(green_button_style())
        self.rbutton.move(self.width() // 2 - self.rbutton.sizeHint().width() // 2, 300)
        self.rbutton.clicked.connect(self.generate_key)

        self.ebutton = QPushButton("Encrypt", self)
        self.ebutton.resize(self.ebutton.sizeHint().width(), self.ebutton.sizeHint().height())
        self.ebutton.setStyleSheet(blue_button_style())
        self.ebutton.move(180, 350)
        self.ebutton.setDisabled(True)
        self.ebutton.setStyleSheet(disabled_button_style())
        self.ebutton.clicked.connect(self.encrypt)

        self.dbutton = QPushButton("Decrypt", self)
        self.dbutton.resize(self.dbutton.sizeHint().width(), self.dbutton.sizeHint().height())
        self.dbutton.setStyleSheet(blue_button_style())
        self.dbutton.move(280, 350)
        self.dbutton.setDisabled(True)
        self.dbutton.setStyleSheet(disabled_button_style())
        self.dbutton.clicked.connect(self.decrypt)

        self.cbutton = QPushButton("Contacts", self)
        self.cbutton.resize(self.cbutton.sizeHint().width(), self.cbutton.sizeHint().height())
        self.cbutton.setStyleSheet(blue_button_style())
        self.cbutton.move(380, 350)
        self.cbutton.clicked.connect(self.open_contact)

        self.pbutton = QPushButton("Update private key", self)
        self.pbutton.resize(self.pbutton.sizeHint().width(), self.pbutton.sizeHint().height())
        self.pbutton.setStyleSheet(blue_button_style())
        self.pbutton.move(480, 350)
        self.pbutton.clicked.connect(self.update_private_key)

        self.private_found_indicator = QLabel("Private key not loaded - update or generate private key", self)
        self.private_found_indicator.resize(self.private_found_indicator.sizeHint().width(), self.private_found_indicator.sizeHint().height())

        self.current_recipient = QLabel("Recipient: Not selected. Use Contacts", self)
        self.current_recipient.resize(800, self.current_recipient.sizeHint().height())
        self.current_recipient.move(10, self.height() - self.current_recipient.height() - 10)
        self.private_found_indicator.move(10, self.height() - self.current_recipient.height() - self.private_found_indicator.height() - 10)

        self.keymgr = keymgr.create()
        self.recipient = None
        self.private_key_path = None
        if not isfile(join(WORKING_DIRECTORY,'data','private_key_location.txt')):
            with open(join(WORKING_DIRECTORY,'data','private_key_location.txt'), 'w') as file:
                file.write('')
        with open(join(WORKING_DIRECTORY,'data','private_key_location.txt'), 'r') as file:
            location = file.read()
            if isfile(location):
                self.private_key_path = location
                self.set_private_key_found_indicator(True)


        self.contact = Contacts(self.keymgr, self.set_recipient_key)
        self.imview = None

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
        self.popup_message("Success", "private.pem or public.pem saved in the directory")
        self.set_private_key_path(private_file)
    
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
        path, _ = QFileDialog.getOpenFileName(self, "select file")
        return path

    def get_save_file(self):
        path, _= QFileDialog.getOpenFileName(self, "select file")
        return path

    def set_private_key_found_indicator(self, on):
        if on:
            self.private_found_indicator.setText("Private key located")
            self.dbutton.setDisabled(False)
            self.dbutton.setStyleSheet(blue_button_style())
        else:
            self.private_found_indicator.setText("Private key not located")
            self.dbutton.setDisabled(True)
            self.dbutton.setStyleSheet(disabled_button_style())

    def set_private_key_path(self, path):
        if not isfile(path):
            self.popup_message("Error", "File does not exist.")
            return False
        with open(path, 'rb') as file:
            head = file.read(40)
            if not head.startswith(b'-----BEGIN RSA PRIVATE KEY-----'):
                self.popup_message("Error", "Invalid private key.")
                return False
        self.private_key_path = path
        self.set_private_key_found_indicator(True)
        with open(join(WORKING_DIRECTORY, 'data', 'private_key_location.txt'), 'w') as file:
            file.write(self.private_key_path)
        return True

    def load_private_key(self):
        if self.private_key_path:
            return load_key(self.private_key_path)
    
    def set_recipient_key(self, key):
        self.recipient = key
        self.current_recipient.setText(f"Recipient: {key['name']}({key['email']})")
        self.ebutton.setDisabled(False)
        self.ebutton.setStyleSheet(blue_button_style())
    
    def open_contact(self):
        self.contact.show()

    def encrypt(self):
        if not self.recipient:
            self.popup_message("Error", "recipient not selected.")
            return
        path = self.get_open_file()
        if path == "":
            return
        
        try:
            image = open_image(path)
            encrypted = encrypt_image(image, self.recipient['public_key'])
            self.show_image("Encrypted Image", encrypted)
        except Exception as err:
            self.popup_message("Error", str(err))
    
    def decrypt(self):
        if not self.private_key_path:
            self.popup_message("Error", "private key not located.")
            return
        path = self.get_open_file()
        if path == "":
            return
        try:
            private_key = self.load_private_key()
            image = open_image(path)
            decrypted = decrypt_image(image, private_key)
            self.show_image("Decrypted Image", decrypted)
        except Exception as err:
            self.popup_message("Error", str(err))
    
    def update_private_key(self):
        path = self.get_open_file()
        if path == "":
            return
        if self.set_private_key_path(path):
            self.popup_message("Success", "Updated private key path.")

    def show_image(self, title, image):
        default_email = self.recipient['email'] if self.recipient else None
        self.imview = ImageViewer(title, image, default_email=default_email)
        self.imview.show()
    
    def closeEvent(self, event):
        self.contact.close()

class Contacts(QWidget):
    """
    Contacts window
    """

    def __init__(self, key_manager, setter):
        super(Contacts,self).__init__()
        self.setStyleSheet("background-color:#315d90; font: 12pt Helvetica;")
        self.setWindowTitle("Contacts - Photo Crypto")
        self.resize(500, 600)
        self.key_manager = key_manager
        self.setter = setter
        self.key_manager.connect()
        self.form =QFormLayout()
        self.keys = {}
        contact_list = QWidget()
        contact_list.setStyleSheet("color: #ffffff")
        self.list_key()
        contact_list.setLayout(self.form)
        scroll = QScrollArea()
        scroll.setWidget(contact_list)
        scroll.setWidgetResizable(True)
        add = QPushButton("Add Contact")
        add.setStyleSheet(blue_button_style(height=60))
        vbox = QVBoxLayout(self)
        vbox.addWidget(scroll)
        vbox.addWidget(add)
        #self.show()
        self.add_contact = AddContact(self.add_key)
        add.clicked.connect(self.open_add_contact)
    
    def list_key(self):
        self.keys = {}
        names = []
        emails = []
        buttons = []
        while self.form.count() >0:
            self.form.removeRow(self.form.takeAt(0))
        keys = self.key_manager.list_key()
        i = 0
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 20, 0, 20)
        hbox.addWidget(QLabel("Name"))
        hbox.addWidget(QLabel("Email"))
        hbox.addWidget(QLabel("Set Recipient"))
        self.form.addRow(hbox)
        for key in keys:
            names.append(QLabel(key['name']))
            emails.append(QLabel(key['email']))
            button = QPushButton("Set Recipient")
            button.setStyleSheet(green_button_style())
            self.keys[button] = key
            button.clicked.connect(self.set_key)
            buttons.append(button)
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 20, 0, 20)
            hbox.addWidget(names[i])
            hbox.addWidget(emails[i])
            hbox.addWidget(buttons[i])
            self.form.addRow(hbox)
            i += 1
        return self.key_manager.list_key()
    
    def set_key(self):
        for s in self.keys:
            s.setDisabled(False)
            s.setStyleSheet(green_button_style())
        self.sender().setDisabled(True)
        self.sender().setStyleSheet(disabled_button_style())
        self.setter(self.keys[self.sender()])
    
    def add_key(self, name, email, keypath):
        try:
            key = load_key(keypath)
            self.key_manager.write_key(name, email, key)
            self.add_contact.close()
            self.list_key()
            self.popup_message("Success", "Successfully added contect info.")
        except ValueError as err:
            self.popup_message("Error", str(err))
        except FileNotFoundError as err:
            self.popup_message("Error", str(err))

    def popup_message(self, title, text):
        dialog = QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.exec_()
            

    def open_add_contact(self):
        self.add_contact.show()
    
    def closeEvent(self, event):
        self.add_contact.close()

class AddContact(QWidget):
    """
    Add Contact Window
    """

    def __init__(self, callback):
        super(AddContact,self).__init__()
        self.setStyleSheet("background-color:#315d90; font: 12pt Helvetica; color: white")
        self.setWindowTitle("Add Contact - Photo Crypto")
        self.resize(500, 310)
        self.callback = callback
        self.path = ""
        form = QFormLayout(self)

        namebox = QHBoxLayout()
        name_label, self.name_input = QLabel("name"), QLineEdit()
        namebox.addWidget(name_label)
        namebox.addWidget(self.name_input)
        namebox.setContentsMargins(0, 20, 0, 20)

        emailbox = QHBoxLayout()
        email_label, self.email_input = QLabel("email"), QLineEdit()
        emailbox.addWidget(email_label)
        emailbox.addWidget(self.email_input)
        emailbox.setContentsMargins(0, 20, 0, 20)

        keybox = QHBoxLayout()
        key_label, self.path_label, key_button = QLabel("public key"), QLabel(self.path), QPushButton("browse")
        key_button.setStyleSheet(green_button_style())
        key_button.clicked.connect(self.select_file)
        keybox.addWidget(key_label)
        keybox.addWidget(self.path_label)
        keybox.addWidget(key_button)
        keybox.setContentsMargins(0, 20, 0, 20)

        form.addRow(namebox)
        form.addRow(emailbox)
        form.addRow(keybox)
        add_button = QPushButton("Add")
        add_button.setStyleSheet(blue_button_style(height=40))
        form.addRow(add_button)

        add_button.clicked.connect(self.add)
    
    def add(self):
        self.callback(
            self.name_input.text(),
            self.email_input.text(),
            self.path
            )
    
    def select_file(self):
        path = QFileDialog.getOpenFileName(self, "select file")
        self.path, _ = path
        label = "..." + self.path[-20:] if len(self.path) > 20 else self.path
        self.path_label.setText(label)

    def closeEvent(self, event):
        pass

class ImageViewer(QWidget):
    """
    Contact window
    """

    def __init__(self, title, image, default_email=None):
        super(ImageViewer,self).__init__()
        self.setStyleSheet("background-color:#315d90; font: 12pt Helvetica; color: white")
        self.setWindowTitle("Image Viewer - Photo Crypto")
        self.src_image = image
        self.default_email = default_email
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.src_image.to_bytes())
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)
        self.resize(self.pixmap.width()+50,self.pixmap.height()+120)
        self.image.move(25, 50)
        self.label = QLabel(title, self)
        self.label.resize(self.label.sizeHint().width(), self.label.sizeHint().height())
        self.label.move(self.width() / 2 - self.label.width() / 2,10)
        self.save_button = QPushButton("save", self)
        self.share_button = QPushButton("share", self)
        self.save_button.resize(self.share_button.sizeHint().width(), self.share_button.sizeHint().height())
        self.save_button.move(self.width() / 2 - self.share_button.sizeHint().width() - 20, self.height() - self.share_button.sizeHint().height() - 20)
        self.save_button.setStyleSheet(blue_button_style(height=30))
        self.save_button.clicked.connect(self.save_image)
        self.share_button.resize(self.share_button.sizeHint().width(), self.share_button.sizeHint().height())
        self.share_button.move(self.width() / 2 + 20, self.height() - self.share_button.sizeHint().height() - 20)
        self.share_button.setStyleSheet(blue_button_style(height=30))
        self.share_button.clicked.connect(self.share_image)

    def save_image(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["Image files (*bmp *.jpg *.jpeg *.jpe *.jfif *.png) | *.bmp; *.jpg; *.jpeg; *.jpe; *.jfif; *.png"])
        if dialog.exec_() == QFileDialog.Accepted:
            path = dialog.selectedFiles()
            self.src_image.save(*path)
        else:
            return
        # print(path)

    def share_image(self):
        save_path = join(WORKING_DIRECTORY, "data", "shared.bmp")
        self.src_image.save(save_path)
        email = self.default_email if self.default_email else ""
        subject = "Encrypted Image"
        outlook.open_outlook_client(save_path, email, subject)

def startgui():
    app = QApplication(sys.argv)
    window = MainWindow()
    #window = ImageViewer("test", open_image("test.png"))
    window.show()

    app.exec_()


if __name__ == "__main__":
    startgui()
