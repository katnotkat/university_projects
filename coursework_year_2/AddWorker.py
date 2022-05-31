from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date
from checks import *


class AddWorker(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = 'Adding a worker'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 515
        self.connection = connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # first name
        self.label_name = QLabel('Enter your first name:', self)
        self.label_name.move(10, 10)
        self.label_name.setFont(QFont('Arial', 14))

        self.textbox_name = QLineEdit(self)
        self.textbox_name.move(10, 28)
        self.textbox_name.resize(280, 20)

        # last name
        self.label_surname = QLabel('Enter your last name:', self)
        self.label_surname.move(10, 52)
        self.label_surname.setFont(QFont('Arial', 14))

        self.textbox_surname = QLineEdit(self)
        self.textbox_surname.move(10, 70)
        self.textbox_surname.resize(280, 20)

        # date of birth
        self.label_dob = QLabel('Enter your date of birth (YYYY/MM/DD):', self)
        self.label_dob.move(10, 94)
        self.label_dob.setFont(QFont('Arial', 14))

        self.textbox_dob = QLineEdit(self)
        self.textbox_dob.move(10, 112)
        self.textbox_dob.resize(280, 20)

        # phone
        self.label_phone = QLabel('Enter your phone number:', self)
        self.label_phone.move(10, 138)
        self.label_phone.setFont(QFont('Arial', 14))

        self.textbox_phone = QLineEdit(self)
        self.textbox_phone.move(10, 156)
        self.textbox_phone.resize(280, 20)

        # email
        self.label_email = QLabel('Enter your E-mail address:', self)
        self.label_email.move(10, 180)
        self.label_email.setFont(QFont('Arial', 14))

        self.textbox_email = QLineEdit(self)
        self.textbox_email.move(10, 198)
        self.textbox_email.resize(280, 20)

        # ssn
        self.label_ssn = QLabel('Enter your SSN number (only digits):', self)
        self.label_ssn.move(10, 222)
        self.label_ssn.setFont(QFont('Arial', 14))

        self.textbox_ssn = QLineEdit(self)
        self.textbox_ssn.move(10, 240)
        self.textbox_ssn.resize(280, 20)

        # inn
        self.label_inn = QLabel('Enter your INN number (only digits):', self)
        self.label_inn.move(10, 264)
        self.label_inn.setFont(QFont('Arial', 14))

        self.textbox_inn = QLineEdit(self)
        self.textbox_inn.move(10, 282)
        self.textbox_inn.resize(280, 20)

        # passport data
        self.label_passport = QLabel('Enter your passport series and number (digits, no spaces):', self)
        self.label_passport.move(10, 306)
        self.label_passport.setFont(QFont('Arial', 14))

        self.textbox_passport = QLineEdit(self)
        self.textbox_passport.move(10, 324)
        self.textbox_passport.resize(280, 20)

        # Library
        self.label_library = QLabel('Choose your library:', self)
        self.label_library.move(10, 348)
        self.label_library.setFont(QFont('Arial', 14))

        self.combo_library = QComboBox(self)
        self.combo_library.move(10, 366)
        self.combo_library.resize(280, 20)
        libraries = self.connection.choose_table_columns('Library', ['Name'])
        self.combo_library.addItem('')
        for el in libraries:
            self.combo_library.addItem(el[0])

        # Post
        self.label_post = QLabel('Choose your post:', self)
        self.label_post.move(10, 390)
        self.label_post.setFont(QFont('Arial', 14))

        self.combo_post = QComboBox(self)
        self.combo_post.move(10, 408)
        self.combo_post.resize(280, 20)
        posts = self.connection.choose_table_columns('Post', ['PostName'])
        self.combo_post.addItem('')
        for el in posts:
            self.combo_post.addItem(el[0])

        # salary
        self.label_salary = QLabel('Enter the salary (in roubles):', self)
        self.label_salary.move(10, 432)
        self.label_salary.setFont(QFont('Arial', 14))

        self.textbox_salary = QLineEdit(self)
        self.textbox_salary.move(10, 450)
        self.textbox_salary.resize(280, 20)

        # button to add a worker
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a worker')
        button_add.move(97, 474)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit')
        button_exit.move(203, 474)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

    @pyqtSlot()
    def on_click_add(self):
        print('Button_addworker_clicked')
        name = self.textbox_name.text().lower()
        surname = self.textbox_surname.text().lower()
        dob = self.textbox_dob.text()
        phone = self.textbox_phone.text()
        email = self.textbox_email.text().lower()
        inn = self.textbox_inn.text()
        ssn = self.textbox_ssn.text()
        passport = self.textbox_passport.text()
        salary = self.textbox_salary.text()
        library = self.combo_library.currentText()
        post = self.combo_post.currentText()
        datestarted = date.today().strftime("%Y/%m/%d")

        # checking all the entered data
        if not is_data_filled([name, surname, dob, phone, email, inn, ssn, passport, salary, library, post]):
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
            elif not is_ssn_inn_passp(ssn, 'ssn'):
                QMessageBox.warning(self, 'Wrong SSN format', "Enter your SSN in right format, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_ssn.setText("")
            elif not is_ssn_inn_passp(inn, 'inn'):
                QMessageBox.warning(self, 'Wrong INN format', "Enter your INN in right format, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_inn.setText("")
            elif not is_ssn_inn_passp(passport, 'passport'):
                QMessageBox.warning(self, 'Wrong passport format', "Enter your passport data in right format, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_passport.setText("")
            elif not is_int(salary):
                QMessageBox.warning(self, 'Wrong salary format', "Salary should be an integer number",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_salary.setText("")
            elif self.connection.execute_statement(f"select dbo.check_worker('{ssn}', '{inn}', '{passport}')",
                                                   True)[0][0]:
                QMessageBox.warning(self, 'Worker already exists!', "Worker personal data already exists!",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_ssn.setText("")
                self.textbox_inn.setText("")
                self.textbox_passport.setText("")
            else:
                libid = self.connection.find_column_by_conditions('Library', 'LibraryID',
                                                                  ['Name'], [library], ['varchar'])
                postid = self.connection.find_column_by_conditions('Post', 'PostID', ['PostName'], [post], ['varchar'])
                values = tuple([ssn, inn, passport, name, surname, phone, email, dob,
                                datestarted, int(salary), int(libid), int(postid)])
                # защита от системных ошибок по вводу данных в базу
                try:
                    self.connection.insert_into('Worker', values)
                    buttonReply = QMessageBox.question(self, 'Want to exit?',
                                                       "Worker added to database. Want to add another worker?",
                                                       QMessageBox.Yes | QMessageBox.No,
                                                       QMessageBox.Yes)
                    if buttonReply == QMessageBox.No:
                        self.close()
                except:
                    QMessageBox.warning(self, 'Check your data', "Check your data: you should be over 18 years old!",
                                        QMessageBox.Ok, QMessageBox.Ok)

                self.textbox_name.setText("")
                self.textbox_surname.setText("")
                self.textbox_dob.setText("")
                self.textbox_phone.setText("")
                self.textbox_email.setText("")
                self.textbox_inn.setText("")
                self.textbox_ssn.setText("")
                self.textbox_passport.setText("")
                self.textbox_salary.setText("")
                self.combo_library.setCurrentText("")
                self.combo_post.setCurrentText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
