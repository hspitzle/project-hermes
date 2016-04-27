from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *

from User import *

form_class = uic.loadUiType("assets/ui/login.ui")[0]                 # Load the UI


class LoginDialog(QDialog, form_class):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setModal(True)
        self.setFixedSize(self.width(), self.height())
        self.connectActions()

        self.gpassEdit.setEchoMode(QLineEdit.Password)
        self.s_passEdit.setEchoMode(QLineEdit.Password)

    def connectActions(self):
        self.loginButton.clicked.connect(self.profileLogin)
        self.loginEdit.returnPressed.connect(self.profileLogin)
        self.createButton.clicked.connect(self.profileCreate)

    def profileCreate(self):
        username = str(self.usernameEdit.text())
        G_username = str(self.gmailEdit.text())
        G_password = str(self.gpassEdit.text())
        S_username = str(self.s_userEdit.text())
        S_password = str(self.s_passEdit.text())
        SOUNDCLOUD_CLIENT_ID = str(self.s_clientEdit.text())
        SOUNDCLOUD_CLIENT_SECRET_ID = str(self.s_secretEdit.text())

        # wrtie info
        # f = open('user.tmp', 'w')
        # f.write(username + "\n")
        # f.write(G_username + "\n")
        # f.write(G_password + "\n")
        # f.write(S_username + "\n")
        # f.write(S_password + "\n")
        # f.write(SOUNDCLOUD_CLIENT_ID + "\n")
        # f.write(SOUNDCLOUD_CLIENT_SECRET_ID + "\n")

        # read info
        f = open('user.tmp', 'r')
        username = f.readline()[:-1]
        G_username = f.readline()[:-1]
        G_password = f.readline()[:-1]
        S_username = f.readline()[:-1]
        S_password = f.readline()[:-1]
        SOUNDCLOUD_CLIENT_ID = f.readline()[:-1]
        SOUNDCLOUD_CLIENT_SECRET_ID = f.readline()[:-1]

        # testing
        # print username
        # print G_username
        # print G_password
        # print S_username
        # print S_password
        # print SOUNDCLOUD_CLIENT_ID
        # print SOUNDCLOUD_CLIENT_SECRET_ID
        #
        # f = open('user1.tmp', 'w')
        # f.write(username + "\n")
        # f.write(G_username + "\n")
        # f.write(G_password + "\n")
        # f.write(S_username + "\n")
        # f.write(S_password + "\n")
        # f.write(SOUNDCLOUD_CLIENT_ID + "\n")
        # f.write(SOUNDCLOUD_CLIENT_SECRET_ID + "\n")

        Deviceclient = Webclient()
        Deviceclient.login(G_username, G_password)
        DList = Deviceclient.get_registered_devices()
        GOOGLE_DEVICE_ID = ''
        for device in DList:
            if device['type'] == "PHONE":
                GOOGLE_DEVICE_ID = device["id"]
                if GOOGLE_DEVICE_ID[:2] == '0x':
                    GOOGLE_DEVICE_ID = GOOGLE_DEVICE_ID[2:]
                break

        userdata_path = User.get_filename(username)
        if not path.exists(userdata_path):
            os.mkdir(userdata_path)

        File = open(path.join(userdata_path, username), 'w+')
        File.write(User.encode("private_key", G_username) + '\n')
        File.write(User.encode("private_key", G_password) + '\n')
        File.write(User.encode("private_key", S_username) + '\n')
        File.write(User.encode("private_key", S_password) + '\n')
        File.write(GOOGLE_DEVICE_ID + '\n')
        File.write(SOUNDCLOUD_CLIENT_ID + '\n')
        File.write(SOUNDCLOUD_CLIENT_SECRET_ID + '\n')
        File.close()
        self.login(username)

    def login(self, username):
        self.parent.username = username
        self.done(1)

    def profileLogin(self):
        username = str(self.loginEdit.text())
        self.login(username)
