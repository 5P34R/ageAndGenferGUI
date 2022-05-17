
import sys, os
from PIL import Image
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from cv2 import solveCubic

from utils.dbconnect import createUser, Login
from utils.uuidGen import randomUUID
from utils.img_detect import solution
# from utils.video.agender.main import solve

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('screens/welcome.ui', self)

        self.createaccount_button.clicked.connect(self.goToCreateScreen)
        self.login_button.clicked.connect(self.goToLogin)
        self.contact_button.clicked.connect(self.goToContact)


    def goToCreateScreen(self):
        print("pressed")
        createAccount = CreateAccountScreen()
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex() +1)

    def goToLogin(self):
        loginscreen = LoginScreen()
        widget.addWidget(loginscreen)
        widget.setCurrentIndex(widget.currentIndex() +1)

    def goToContact(self):
        contact = ContactUs()
        widget.addWidget(contact)
        widget.setCurrentIndex(widget.currentIndex() +1)


class CreateAccountScreen(QDialog):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi('screens/createaccount.ui', self)
        self.fname_input.setAlignment(Qt.AlignCenter)
        self.lname_input.setAlignment(Qt.AlignCenter)
        self.email_input.setAlignment(Qt.AlignCenter)
        self.phone_input.setAlignment(Qt.AlignCenter)
        self.username_input.setAlignment(Qt.AlignCenter)
        self.password_input.setAlignment(Qt.AlignCenter)

        self.login_button.clicked.connect(self.goToLogin)
        self.createaccount_button.clicked.connect(self.signup)

    def goToLogin(self):
        loginscreen = LoginScreen()
        widget.addWidget(loginscreen)
        widget.setCurrentIndex(widget.currentIndex() +1)

    def signup(self):
        fname = self.fname_input.text()
        lname = self.lname_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        # print(fname, lname, email, phone, username, password)
        uuid = randomUUID()
        res = createUser(uuid=uuid, username=username, password=password, f_name=fname, l_name=lname, email=email, phone=phone)

        if res == "success":
            opt = OptionScreen()
            widget.addWidget(opt)
            widget.setCurrentIndex(widget.currentIndex() +1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('screens/loginscreen.ui', self)
        self.username_input.setAlignment(Qt.AlignCenter)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.invalid_label.setAlignment(Qt.AlignCenter)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.createaccount_button.clicked.connect(self.goToSignup)
        self.loginsubmit_button.clicked.connect(self.submitLogin)
        

    def goToSignup(self):
        signup = CreateAccountScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() +1)

    def submitLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        res = Login(username=username, password=password)
        if res == "invalid":
            self.invalid_label.setText("Incorrect username/passwd")
        else:
            opt = OptionScreen()
            widget.addWidget(opt)
            widget.setCurrentIndex(widget.currentIndex() +1)


class OptionScreen(QDialog):
    def __init__(self):
        super(OptionScreen, self).__init__()
        loadUi("screens/optionscreen.ui", self)
        self.go_back.setIcon(QIcon('assets/back-button.png'))
        self.go_back.setIconSize(QSize(40, 40))
        self.upload_img_button.clicked.connect(self.goToUpload)
        self.video_button.clicked.connect(self.VideoCaps)

    def VideoCaps(self):
        os.system("python ./utils/video/agender/main.py")
        # print(os.getcwd())
    def goToUpload(self):
        imgRec = ImageRecog()
        widget.addWidget(imgRec)
        widget.setCurrentIndex(widget.currentIndex() +1)

    def goBack(self):
        welcm = WelcomeScreen()
        widget.addWidget(welcm)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ImageRecog(QDialog):
    def __init__(self):
        super(ImageRecog, self).__init__()
        loadUi('screens/imagerecg.ui', self)

        self.go_back.setIcon(QIcon('assets/back-button.png'))
        self.go_back.setIconSize(QSize(40, 40))
        self.go_back.clicked.connect(self.goBack)

        self.upload_button.clicked.connect(self.getImageFile)
        # self.train_button.clicked.connect(self.OpenWindow)
    
    def goBack(self):
        opt = OptionScreen()
        widget.addWidget(opt)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def getImageFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", os.path.expanduser('~'), "Image files (*.jpg *.png *.jpeg *.gif)")
        print(filename)
        self.image_label.setPixmap(QPixmap(filename))
        solution(filename)

    # def OpenWindow(self):
    #     self.w = Result()
    #     self.w.initUI()


class Result(QDialog):
    def __init__(self):
        super(Result, self).__init__()
        loadUi('screens/result.ui', self)
    
    def initUI(self): 
        image = Image.open(f"{os.getcwd()}\output\output.jpg")
        image = image.resize((600, 400))
        width, height = image. size
        print(width, height)
        # pixmap = QPixmap(f"{os.getcwd()}\output\output.jpg")
        self.image_output.setPixmap(QPixmap(f"{os.getcwd()}\output\output.jpg"))
        self.resize(width,height)
        self.show()


class ContactUs(QDialog):
    def __init__(self):
        super(ContactUs, self).__init__()
        loadUi('screens/contactui.ui', self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)

    widget.setFixedHeight(650)
    widget.setFixedWidth(1050)

    widget.show()

    sys.exit(app.exec_())