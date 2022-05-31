from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date
from checks import *


class AddReader(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = 'Adding a reader'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 300
        self.connection = connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.label_name = QLabel('Enter your first name:', self)
        self.label_name.move(10, 10)
        self.label_name.setFont(QFont('Arial', 14))

        # Create textbox with a name
        self.textbox_name = QLineEdit(self)
        self.textbox_name.move(10, 28)
        self.textbox_name.resize(280, 20)

        self.label_surname = QLabel('Enter your last name:', self)
        self.label_surname.move(10, 52)
        self.label_surname.setFont(QFont('Arial', 14))

        # Create textbox with a surname
        self.textbox_surname = QLineEdit(self)
        self.textbox_surname.move(10, 70)
        self.textbox_surname.resize(280, 20)

        self.label_dob = QLabel('Enter your date of birth (YYYY/MM/DD):', self)
        self.label_dob.move(10, 94)
        self.label_dob.setFont(QFont('Arial', 14))

        # Create textbox with a date of birth
        self.textbox_dob = QLineEdit(self)
        self.textbox_dob.move(10, 112)
        self.textbox_dob.resize(280, 20)

        self.label_phone = QLabel('Enter your phone number:', self)
        self.label_phone.move(10, 138)
        self.label_phone.setFont(QFont('Arial', 14))

        # Create textbox with a phone number
        self.textbox_phone = QLineEdit(self)
        self.textbox_phone.move(10, 156)
        self.textbox_phone.resize(280, 20)

        self.label_email = QLabel('Enter your E-mail address:', self)
        self.label_email.move(10, 180)
        self.label_email.setFont(QFont('Arial', 14))

        # Create textbox with an email address
        self.textbox_email = QLineEdit(self)
        self.textbox_email.move(10, 198)
        self.textbox_email.resize(280, 20)

        # button to add a reader
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a reader')
        button_add.move(97, 243)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit')
        button_exit.move(203, 243)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

    @pyqtSlot()
    def on_click_add(self):
        print('Button_addreader_clicked')
        name = self.textbox_name.text().lower()
        surname = self.textbox_surname.text().lower()
        dob = self.textbox_dob.text()
        phone = self.textbox_phone.text()
        email = self.textbox_email.text().lower()
        datestart = date.today().strftime("%Y/%m/%d")
        statusdate = date.today().strftime("%Y/%m/%d")

        # checking all the entered data
        if not is_data_filled([name, surname, dob, phone, email]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill all the fields, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            if not is_date(dob):
                QMessageBox.warning(self, 'Date should be formatted', "Wrong date format, fill again, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_dob.setText("")
            elif not is_phone(phone):
                QMessageBox.warning(self, 'Wrong phone number format', "Wrong phone number format, fill again, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_phone.setText("")
            elif not is_email(email):
                QMessageBox.warning(self, 'Wrong email format', "An actual email address needed",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_email.setText("")
            else:
                values = tuple([name, surname, dob, phone, email, datestart, statusdate, 0])
                # защита от системных ошибок по вводу данных в базу
                try:
                    self.connection.insert_into('Reader', values)
                    buttonReply = QMessageBox.question(self, 'Want to exit?',
                                                       "Reader added to database. Want to add another reader?",
                                                       QMessageBox.Yes | QMessageBox.No,
                                                       QMessageBox.Yes)
                    if buttonReply == QMessageBox.No:
                        self.close()
                except:
                    QMessageBox.warning(self, 'Check your data', "Check your data: you should be over 16 years old!",
                                        QMessageBox.Ok, QMessageBox.Ok)

                self.textbox_name.setText("")
                self.textbox_surname.setText("")
                self.textbox_dob.setText("")
                self.textbox_phone.setText("")
                self.textbox_email.setText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
