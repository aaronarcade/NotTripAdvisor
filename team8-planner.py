import pymysql
import csv
import sys
import getpass
from PyQt5 import QtWidgets

from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QVariant,
    QDate
)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QAction,
    QDialog,
    QWidget,
    QDialogButtonBox,
    QFileDialog,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QListView,
    QLabel,
    QLineEdit,
    QDateEdit,
    QPlainTextEdit,
    QComboBox,
    QMessageBox
)

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem
)

# from mainwindow import Ui_MainWindow

def all_not_active():
    conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
    curs=conn.cursor()
    curs.execute("UPDATE user SET is_current = 0")
    curs.close()
    conn.commit()
    conn.close()

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Login')
        self.userLabel = QLabel("User:", self)
        self.textName = QtWidgets.QLineEdit(self)
        self.passLabel = QLabel("Pass:", self)
        self.textPass = QtWidgets.QLineEdit(self)
        #self.LLL = QtWidgets.QPushButton('LLL', self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonRegis = QtWidgets.QPushButton('Register', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonRegis.clicked.connect(self.display_regis)
        #self.LLL.clicked.connect(self.lll)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.userLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.passLabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        layout.addWidget(self.buttonRegis)

    def handleLogin(self):

        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        curs.execute("SELECT * FROM user")
        curs.close()
        conn.close()

        global user_data
        user_data = {}
        for line in curs:
            user_data[line[2]] = line[0:2]+line[3:]

        if self.textName.text() in user_data:
            userinfo = user_data[self.textName.text()]

        check_login(self.textName.text())

        current_user_switch("on", self.textName.text())

        if self.textName.text() =='' or self.textPass.text()=='':
            QtWidgets.QMessageBox.warning(self, 'Error', 'User or Password Missing')
        elif self.textName.text() in user_data:
            if self.textPass.text() == user_data[self.textName.text()][2]:
                if user_data[self.textName.text()][4] == 1:
                    QtWidgets.QMessageBox.warning(self, 'Sorry', 'You have been suspended by an admin')
                else:
                    self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Incorrect Password')
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Incorrect User or Password')

    def __str__(self):
        return(self.textName.text())

    def display_regis(self):
        regis_val()
        self.accept()

def current_user_switch(onoff, username="nouser"):
    conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
    curs=conn.cursor()
    query = f"UPDATE user SET is_current = 1 WHERE email = '{username}'"
    curs.execute(query)
    curs.close()
    conn.commit()
    conn.close()

    conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
    curs=conn.cursor()
    query = "SELECT * from user where is_current = 1"
    curs.execute(query)
    curs.close()
    conn.commit()
    conn.close()

def regis_val():
    global val
    val = 2

def check_login(email):
    conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
    curs=conn.cursor()
    query = f"SELECT is_admin FROM user WHERE email = '{email}'"
    curs.execute(query)
    curs.close()
    conn.close()
    global val
    for line in curs:
        val = line[0]
    return("Bonus points for tears?")

class Admin(QtWidgets.QDialog):
    def open_file(self):
        file_name, filter = \
            QFileDialog.getOpenFileName(self, "Open file", ".",
                                        "All files (*);;CSV Files (*.csv)")

        with open(file_name) as fin:
            csv_data = [row for row in csv.reader(fin)]
        table_model = SimpleTableModel(csv_data[0], csv_data[1:])
        table_view = QTableView()
        table_view.setModel(table_model)
        self.setCentralWidget(table_view)

    def __init__(self, parent=None):
        super(Admin, self).__init__(parent)
        self.setWindowTitle('Admin Dashboard')
        self.resize(600,400)
        self.attrLabel = QLabel("Attractions:", self)
        self.attrbttn = QPushButton("List of Attractions",self)
        #self.attrbttn.clicked.connect(self.test)
        self.attrbttn.clicked.connect(self.display_attr_dialogue)

        self.nattrbttn = QPushButton("New Attraction",self)
        self.nattrbttn.clicked.connect(self.display_nattr)

        self.eattrbttn = QPushButton("Edit Attraction",self)
        self.eattrbttn.clicked.connect(self.display_eattr)

        self.attrrepbttn = QPushButton("Attraction Reports",self)
        self.attrrepbttn.clicked.connect(self.display_thelastpage)

        self.userLabel = QLabel("Users:", self)
        self.userbttn = QtWidgets.QPushButton('List of Users', self)
        self.userbttn.clicked.connect(self.display_user_dialogue)

        self.nuserbttn = QtWidgets.QPushButton('New User', self)
        self.nuserbttn.clicked.connect(self.display_nuser)

        self.duserbttn = QtWidgets.QPushButton('Delete User', self)
        self.duserbttn.clicked.connect(self.display_duser)

        self.suserbttn = QtWidgets.QPushButton('Suspend/Unsuspend User', self)
        self.suserbttn.clicked.connect(self.display_suser)

        self.buttonDism = QtWidgets.QPushButton('Dismiss', self)
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.attrLabel)
        layout.addWidget(self.attrbttn)
        layout.addWidget(self.nattrbttn)
        layout.addWidget(self.eattrbttn)
        layout.addWidget(self.attrrepbttn)
        layout.addWidget(self.userLabel)
        layout.addWidget(self.userbttn)
        layout.addWidget(self.nuserbttn)
        layout.addWidget(self.duserbttn)
        layout.addWidget(self.suserbttn)

        layout.addWidget(self.buttonDism)

        self.attraction_table_view =  QTableView(self)
        self.attraction_table_view.resize(900, 1200)
        self.attraction_table_view.move(0,57)
        self.attraction_table_view.setVisible(False)

        self.user_table_view =  QTableView(self)
        self.user_table_view.resize(900, 1200)
        self.user_table_view.move(0,57)
        self.user_table_view.setVisible(False)

        self.buttonDism.clicked.connect(self.callingFunction)

    def callingFunction(self):
        all_not_active()
        self.close()

    def display_attr_dialogue(self):
        connection = pymysql.connect(host = 'localhost',
                                         user='root',
                                         password='',
                                         db ='team8')

        cursor = connection.cursor()
        cursor.execute("select * from attraction")
        listoflists = []

        for row in cursor:
            listoflists.append(row)

        attraction_table_model = SimpleTableModel(['Name','Description', 'Address', 'Transit #', 'Need Reservation'], listoflists)

        cursor.close()
        connection.close()
        table_dialog = TableDialog('Attractions', attraction_table_model)
        table_dialog.exec_()

    def display_attraction_table(self):
        self.attraction_table_view.setVisible(True)
        self.user_table_view.setVisible(False)
        self.attraction_table_view.update()

    def display_user_dialogue(self):
        connection = pymysql.connect(host = 'localhost',
                                         user='root',
                                         password='',
                                         db ='team8')

        cursor = connection.cursor()
        cursor.execute("select * from user")
        listoflists2 = []

        for row in cursor:
            listoflists2.append(row)

        user_table_model = SimpleTableModel(['First Name','Last Name', 'Email', 'Password', 'Admin', 'Suspended'], listoflists2)

        cursor.close()
        connection.close()
        table_dialog = TableDialog('Users', user_table_model)
        table_dialog.exec_()

    def display_user_table(self):
        self.user_table_view.setVisible(True)
        self.attraction_table_view.setVisible(False)
        self.attraction_table_view.update()

    def display_nattr(self):
        newA = NewA()
        #need var to pass to tell to prefill
        newA.show()
        newA.exec_()

    def display_eattr(self):
        editA = EditA()
        editA.show()
        editA.exec_()

    def display_nuser(self):
        registration = Registration()
        registration.show()
        registration.exec_()

    def display_duser(self):
        delt = Delt()
        delt.show()
        delt.exec_()

    def display_suser(self):
        susp = Susp()
        susp.show()
        susp.exec_()

    def display_thelastpage(self):
        attrReports = AttrReports()
        attrReports.show()
        attrReports.exec_()


class Delt(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Delt, self).__init__(parent)
        #if dors == "d":
        self.setWindowTitle('Delete User')
        #if dors == "s":
        #    self.setWindowTitle('Suspend User')
        self.resize(600,200)


        self.userLabel = QLabel("User Email:", self)
        self.textUser = QtWidgets.QLineEdit(self)

        self.buttonDel = QtWidgets.QPushButton('Delete', self)
        self.buttonDel.clicked.connect(self.delUser)
        self.buttonDis = QtWidgets.QPushButton('Dismiss', self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.userLabel)
        layout.addWidget(self.textUser)

        layout.addWidget(self.buttonDel)
        layout.addWidget(self.buttonDis)

        self.buttonDis.clicked.connect(self.close)

    def delUser(self):
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        curs1=conn.cursor()

        delQ = f"DELETE FROM user WHERE email='{self.textUser.text()}';"
        genQ = f"SELECT * FROM user WHERE email = '{self.textUser.text()}'"
        curs.execute(genQ)

        user_data = {}
        for line in curs:
            user_data[line[2]] = line[0:2]+line[3:]

        if self.textUser.text() in user_data:
            userinfo = user_data[self.textUser.text()]
            if user_data[self.textUser.text()][3] ==1:
                QtWidgets.QMessageBox.warning(self, 'Error', f"Cannot delete Admin: '{self.textUser.text()}'")
            else:
                curs1.execute(delQ)
                if user_data[self.textUser.text()][4] == 1:
                    QtWidgets.QMessageBox.warning(self, 'Success', f"Suspended user '{self.textUser.text()}' is now deleted")
                else:
                    QtWidgets.QMessageBox.warning(self, 'Success', f"User '{self.textUser.text()}' is now deleted")
                curs.close()
                curs1.close()
                conn.commit()
                conn.close()
                self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', f"User '{self.textUser.text()} is not in the database'")

class Susp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Susp, self).__init__(parent)
        #if dors == "d":
        self.setWindowTitle('Suspend User')
        #if dors == "s":
        #    self.setWindowTitle('Suspend User')
        self.resize(600,200)


        self.userLabel = QLabel("User Email:", self)
        self.textUser = QtWidgets.QLineEdit(self)

        self.buttonSus = QtWidgets.QPushButton('Suspend', self)
        self.buttonSus.clicked.connect(self.susUser)

        self.buttonUnsus = QtWidgets.QPushButton('Unsuspend', self)
        self.buttonUnsus.clicked.connect(self.unsusUser)
        self.buttonDis = QtWidgets.QPushButton('Dismiss', self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.userLabel)
        layout.addWidget(self.textUser)

        layout.addWidget(self.buttonSus)
        layout.addWidget(self.buttonUnsus)
        layout.addWidget(self.buttonDis)

        self.buttonDis.clicked.connect(self.close)

    def susUser(self):
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        curs1=conn.cursor()

        susQ = f"UPDATE user SET is_suspend = 1 WHERE email = '{self.textUser.text()}'"
        genQ = f"SELECT * FROM user WHERE email = '{self.textUser.text()}'"
        curs.execute(genQ)

        user_data = {}
        for line in curs:
            user_data[line[2]] = line[0:2]+line[3:]

        if self.textUser.text() in user_data:
            userinfo = user_data[self.textUser.text()]
            if user_data[self.textUser.text()][4] == 1:
                QtWidgets.QMessageBox.warning(self, 'Error', f"User '{self.textUser.text()}' has already been suspended")
            elif user_data[self.textUser.text()][3] ==1:
                 QtWidgets.QMessageBox.warning(self, 'Error', f"Cannot suspend Admin: '{self.textUser.text()}'")
            else:
                curs1.execute(susQ)
                QtWidgets.QMessageBox.warning(self, 'Success', f"User '{self.textUser.text()}' is now suspended")
                curs.close()
                curs1.close()
                conn.commit()
                conn.close()
                self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', f"User '{self.textUser.text()} is not in the database'")


        # curs.execute(f"UPDATE user SET is_suspend = 1 WHERE email = '{self.textUser.text()}'")

    def unsusUser(self):
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        curs1=conn.cursor()

        unSusQ = f"UPDATE user SET is_suspend = FALSE WHERE email = '{self.textUser.text()}';"
        genQ = f"SELECT * FROM user WHERE email = '{self.textUser.text()}'"
        curs.execute(genQ)

        user_data = {}
        for line in curs:
            user_data[line[2]] = line[0:2]+line[3:]

        if self.textUser.text() in user_data:
            userinfo = user_data[self.textUser.text()]
            if user_data[self.textUser.text()][4] == 0:
                QtWidgets.QMessageBox.warning(self, 'Error', f"User '{self.textUser.text()}' is not currently suspended")
            else:
                curs1.execute(unSusQ)
                QtWidgets.QMessageBox.warning(self, 'Success', f"User '{self.textUser.text()}' is now unsuspended")
                curs.close()
                conn.commit()
                conn.close()
                self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', f"User '{self.textUser.text()} is not in the database'")

class Customer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Customer, self).__init__(parent)
        self.setWindowTitle('Customer Dashboard')
        self.resize(600,400)

        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs1=conn.cursor()
        curs1.execute("SELECT * FROM user WHERE is_current = 1")
        for user in curs1:
            userinfo = user
        curs1.close()
        curs2=conn.cursor()
        email = userinfo[2]
        query = f"SELECT * FROM address WHERE email = '{email}'"
        curs2.execute(query)
        for line in curs2:
            useraddress = line
        curs2.close()
        curs3=conn.cursor()
        query = f"SELECT * FROM credit_card WHERE email = '{email}'"
        curs3.execute(query)
        for line in curs3:
            usercredit = line
        curs3.close()
        conn.close()

        self.profileLabel = QLabel("Profile", self)
        self.userLabel = QLabel(f"     Email:\t{email}", self)
        self.l_nameLabel = QLabel(f"     Last Name:\t{userinfo[1]}", self)
        self.f_nameLabel = QLabel(f"     First Name:\t{userinfo[0]}", self)
        #self.b_dayLabel = QLabel(f"     Birthday:\t{useraddress[3]}", self)
        self.ccLabel = QLabel(f"     Credit Card:\t{usercredit[0]}", self)
        self.expLabel = QLabel(f"     Expiry:\t{usercredit[1]}", self)
        self.addr1Label = QLabel(f"     Address 1:\t{useraddress[0]}, {useraddress[1]}", self)
        self.addr2Label = QLabel(f"     Address 2:\t", self)
        self.cityLabel = QLabel(f"     City:\t\t{useraddress[2]}", self)
        self.stateLabel = QLabel(f"     State:\t{useraddress[3]}", self)
        self.postLabel = QLabel(f"     Postal Code:\t{useraddress[4]}", self)
        self.countLabel = QLabel(f"     Country:\t{useraddress[5]}", self)
        self.tripLabel = QLabel("Trips:", self)

        self.buttonEditP = QtWidgets.QPushButton('Edit Profile', self)
        self.buttonEditP.clicked.connect(self.open_edit_customer)
        self.buttonDet = QtWidgets.QPushButton('Trip Details', self)
        self.buttonDet.clicked.connect(self.openDeets)
        self.buttonNewT = QtWidgets.QPushButton('New Trip', self)
        self.buttonNewT.clicked.connect(self.open_Reports)
        self.buttonDis = QtWidgets.QPushButton('Dismiss', self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.profileLabel)
        layout.addWidget(self.buttonEditP)
        layout.addWidget(self.userLabel)
        layout.addWidget(self.l_nameLabel)
        layout.addWidget(self.f_nameLabel)
        #layout.addWidget(self.b_dayLabel)
        layout.addWidget(self.ccLabel)
        layout.addWidget(self.expLabel)
        layout.addWidget(self.addr1Label)
        layout.addWidget(self.addr2Label)
        layout.addWidget(self.cityLabel)
        layout.addWidget(self.stateLabel)
        layout.addWidget(self.postLabel)
        layout.addWidget(self.countLabel)
        layout.addWidget(self.tripLabel)
        layout.addWidget(self.buttonDet)
        layout.addWidget(self.buttonNewT)
        layout.addWidget(self.buttonDis)

        self.buttonDis.clicked.connect(self.callingFunction)

    def callingFunction(self):
        all_not_active()
        self.close()

    def c_u_s(self, onoff, username):
        current_user_switch(onoff, username)

    def open_Reports(self):
        reports = Reports()
        reports.show()
        reports.exec_()

    def open_edit_customer(self):
        eregistration = ERegistration()
        eregistration.show()
        eregistration.exec_()

        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs0=conn.cursor()
        curs1=conn.cursor()
        curs2=conn.cursor()
        curs3=conn.cursor()
        curs0.execute("SELECT email FROM user WHERE is_current=1")
        for usr in curs0:
            email = usr[0]
        curs1.execute("SELECT * FROM user WHERE is_current=1")

        for line in curs1:
            firstname, lastname, email = line[0], line[1], line[2]

        curs2.execute(f"SELECT * FROM address where email='{email}'")
        curs3.execute(f"SELECT * FROM credit_card where email='{email}'")
        curs1.close()
        curs2.close()
        curs3.close()
        conn.close()


        for line in curs2:
            street, city, state, zipcode, country = f"{line[0]} {line[1]}", line[2], line[3], line[4], line[5]
        for line in curs3:
            no, date = line[0], str(line[1])

        self.userLabel.setText(f"     Email:\t{email}")
        self.l_nameLabel.setText(f"     Last Name:\t{lastname}")
        self.f_nameLabel.setText(f"     First Name:\t{firstname}")
        self.ccLabel.setText(f"     Credit Card:\t{no}")
        self.expLabel.setText(f"     Expiry:\t{date}")
        self.addr1Label.setText(f"     Address 1:\t{street}")
        self.addr2Label.setText(f"     Address 2:\t")
        self.cityLabel.setText(f"     City:\t\t{city}")
        self.stateLabel.setText(f"     State:\t{state}")
        self.postLabel.setText(f"     Postal Code:\t{zipcode}")
        self.countLabel.setText(f"     Country:\t{country}")

    def openDeets(self):
        showDeets = ShowDeets()
        showDeets.show()
        showDeets.exec_()

class SimpleTableModel(QAbstractTableModel):

    def __init__(self, headers, rows):
        QAbstractTableModel.__init__(self, None)
        self.headers = headers
        self.rows = rows

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if (not index.isValid()) or (role != Qt.DisplayRole):
            return QVariant()
        else:
            return QVariant(self.rows[index.row()][index.column()])

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        elif orientation == Qt.Vertical:
            return section + 1
        else:
            return self.headers[section]

class TableDialog(QDialog):
    def __init__ (self, title,table_model):
        super(TableDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle(title)
        self.table_view = QTableView(self)
        self.table_view.setModel(table_model)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.close)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.table_view)
        self.vbox.addWidget(buttons)
        self.setLayout(self.vbox)
        self.resize(600,400)

class Registration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Registration, self).__init__(parent)

        self.setWindowTitle("New User")

        self.emailLabel = QLabel("*Email:", self)
        self.textEmail = QtWidgets.QLineEdit(self)

        self.confirmEmailLabel = QLabel("*Confirm Email:", self)
        self.textConfirmEmail = QtWidgets.QLineEdit(self)

        self.passLabel = QLabel("*Password:", self)
        self.textPass = QtWidgets.QLineEdit(self)

        self.confirmPassLabel = QLabel("*Confirm Password:", self)
        self.textConfirmPass = QtWidgets.QLineEdit(self)

        self.firstLabel = QLabel("*First Name:", self)
        self.textFirst = QtWidgets.QLineEdit(self)

        self.lastLabel = QLabel("*Last Name:", self)
        self.textLast = QtWidgets.QLineEdit(self)

        self.addLabel = QLabel("*Address 1:", self)
        self.textAdd = QtWidgets.QLineEdit(self)

        self.add2Label = QLabel("Address 2:", self)
        self.textAdd2 = QtWidgets.QLineEdit(self)

        self.cityLabel = QLabel("*City:", self)
        self.textCity = QtWidgets.QLineEdit(self)

        self.stateLabel = QLabel("*State:", self)
        self.textState = QtWidgets.QLineEdit(self)

        self.pcLabel = QLabel("*Postal Code:", self)
        self.textPc = QtWidgets.QLineEdit(self)

        self.countryLabel = QLabel("*Country:", self)
        self.textCountry = QtWidgets.QLineEdit(self)

        self.ccnLabel = QLabel("*Credit Card Number:", self)
        self.textCcn = QtWidgets.QLineEdit(self)

        self.cvvLabel = QLabel("*CVV Number:", self)
        self.textCvv = QtWidgets.QLineEdit(self)

        self.ccexpLabel = QLabel("*Credit Card Expiry Date:\n(YYYY-MM-DD)", self)
        self.textCcexp = QtWidgets.QLineEdit(self)

        self.buttonRegister = QtWidgets.QPushButton('Register', self)
        self.buttonRegister.clicked.connect(self.handleRegistration)

        self.buttonDismiss = QtWidgets.QPushButton('Dismiss', self)
        self.buttonDismiss.clicked.connect(self.close)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.emailLabel)
        layout.addWidget(self.textEmail)

        layout.addWidget(self.confirmEmailLabel)
        layout.addWidget(self.textConfirmEmail)

        layout.addWidget(self.passLabel)
        layout.addWidget(self.textPass)

        layout.addWidget(self.confirmPassLabel)
        layout.addWidget(self.textConfirmPass)

        layout.addWidget(self.firstLabel)
        layout.addWidget(self.textFirst)

        layout.addWidget(self.lastLabel)
        layout.addWidget(self.textLast)

        layout.addWidget(self.addLabel)
        layout.addWidget(self.textAdd)

        layout.addWidget(self.add2Label)
        layout.addWidget(self.textAdd2)

        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)

        layout.addWidget(self.stateLabel)
        layout.addWidget(self.textState)

        layout.addWidget(self.pcLabel)
        layout.addWidget(self.textPc)

        layout.addWidget(self.countryLabel)
        layout.addWidget(self.textCountry)

        layout.addWidget(self.ccnLabel)
        layout.addWidget(self.textCcn)

        layout.addWidget(self.cvvLabel)
        layout.addWidget(self.textCvv)

        layout.addWidget(self.ccexpLabel)
        layout.addWidget(self.textCcexp)

        layout.addWidget(self.buttonRegister)

        layout.addWidget(self.buttonDismiss)

    def handleRegistration(self):
        alist=[self.textEmail.text(),self.textConfirmEmail.text(),self.textPass.text(),self.textConfirmPass.text(),self.textFirst.text(),
        self.textLast.text(),self.textAdd.text(),self.textCity.text(),self.textState.text(),self.textPc.text(),self.textCountry.text(),
        self.textCcn.text(), self.textCcexp.text()]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count >0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')

        elif self.textPass.text() != self.textConfirmPass.text():
            QtWidgets.QMessageBox.warning(self, 'Error', "Passwords Don't Match")

        elif self.textEmail.text() != self.textConfirmEmail.text():
            QtWidgets.QMessageBox.warning(self, 'Error', "Emails Don't Match")
        else:
            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs1=conn.cursor()
            query1 = (f"SELECT email from user")
            curs1.execute(query1)
            emails = []
            for email in curs1:
                emails.append(email[0])
            curs1.close()

            if self.textEmail.text() in emails:
                    QtWidgets.QMessageBox.warning(self, 'Error', "Emails Already Exits")
            else:
                curs2=conn.cursor()
                curs3=conn.cursor()
                curs4=conn.cursor()
                add = self.textAdd.text().split()
                add1 = self.textAdd.text().split(",")[0]
                if len(add) == 1:
                    add2 = self.textAdd.text().split(",")[0]
                else:
                    add2 = self.textAdd.text().split(",")[1]
                query2 = (f"INSERT into user values('{self.textFirst.text()}','{self.textLast.text()}','{self.textEmail.text()}','{self.textConfirmPass.text()}',FALSE,FALSE,TRUE)")
                query3 = (f"INSERT into address values('{add1}','{add2}','{self.textCity.text()}','{self.textState.text()}', '{self.textPc.text()}', '{self.textCountry.text()}', '{self.textEmail.text()}')")
                query4 = (f"INSERT into credit_card values('{self.textCcn.text()}','{self.textCcexp.text()}','{self.textCvv.text()}','{self.textEmail.text()}')")
                curs2.execute(query2)
                curs3.execute(query3)
                curs4.execute(query4)
                curs2.close()
                curs3.close()
                curs4.close()
                self.close()
                self.accept()

            conn.commit()
            conn.close()


class ERegistration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ERegistration, self).__init__(parent)
        self.resize(500,800)
        self.setWindowTitle("Edit Login")

        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs1=conn.cursor()
        curs2=conn.cursor()
        curs3=conn.cursor()
        curs1.execute("SELECT * FROM user where is_current='1'")

        for line in curs1:
            firstname, lastname, email = line[0], line[1], line[2]

        curs2.execute(f"SELECT * FROM address where email='{email}'")
        curs3.execute(f"SELECT * FROM credit_card where email='{email}'")
        curs1.close()
        curs2.close()
        curs3.close()
        conn.close()


        for line in curs2:
            street, city, state, zipcode, country = f"{line[0]}, {line[1]}", line[2], line[3], line[4], line[5]
        for line in curs3:
            no, date = line[0], str(line[1])


        #address = line[2].split(",")
        #email, password, firstname, lastname, address, city, state, post, country,
        #name, description, trans = line[0], line[1], line[3]

        self.emailLabel = QLabel("*Email:", self)
        self.textEmail = QLabel(f"{email}\t This is permanent", self)

        self.firstLabel = QLabel("*First Name:", self)
        self.textFirst = QtWidgets.QLineEdit(firstname, self)

        self.lastLabel = QLabel("*Last Name:", self)
        self.textLast = QtWidgets.QLineEdit(lastname, self)

        self.addLabel = QLabel("*Address 1:", self)
        self.textAdd = QtWidgets.QLineEdit(street, self)

        self.add2Label = QLabel("Address 2:", self)
        self.textAdd2 = QtWidgets.QLineEdit(self)

        self.cityLabel = QLabel("*City:", self)
        self.textCity = QtWidgets.QLineEdit(city, self)

        self.stateLabel = QLabel("*State:", self)
        self.textState = QtWidgets.QLineEdit(state, self)

        self.pcLabel = QLabel("*Postal Code:", self)
        self.textPc = QtWidgets.QLineEdit(str(zipcode), self)

        self.countryLabel = QLabel("*Country:", self)
        self.textCountry = QtWidgets.QLineEdit(country, self)

        self.ccnLabel = QLabel("*Credit Card Number:", self)
        self.textCcn = QtWidgets.QLineEdit(str(no), self)

        self.ccexpLabel = QLabel("*Credit Card Expiry Date:\n(YYYY-MM-DD)", self)
        self.textCcexp = QtWidgets.QLineEdit(date, self)

        self.buttonRegister = QtWidgets.QPushButton('Submit Changes', self)
        self.buttonRegister.clicked.connect(self.handleERegistration)

        self.buttonDismiss = QtWidgets.QPushButton('Dismiss', self)
        self.buttonDismiss.clicked.connect(self.close)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.emailLabel)
        layout.addWidget(self.textEmail)

        layout.addWidget(self.firstLabel)
        layout.addWidget(self.textFirst)

        layout.addWidget(self.lastLabel)
        layout.addWidget(self.textLast)

        layout.addWidget(self.addLabel)
        layout.addWidget(self.textAdd)

        layout.addWidget(self.add2Label)
        layout.addWidget(self.textAdd2)

        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)

        layout.addWidget(self.stateLabel)
        layout.addWidget(self.textState)

        layout.addWidget(self.pcLabel)
        layout.addWidget(self.textPc)

        layout.addWidget(self.countryLabel)
        layout.addWidget(self.textCountry)

        layout.addWidget(self.ccnLabel)
        layout.addWidget(self.textCcn)

        layout.addWidget(self.ccexpLabel)
        layout.addWidget(self.textCcexp)

        layout.addWidget(self.buttonRegister)

        layout.addWidget(self.buttonDismiss)

    def handleERegistration(self):
        alist=[self.textEmail.text(),self.textFirst.text(),
        self.textLast.text(),self.textAdd.text(),self.textCity.text(),self.textState.text(),self.textPc.text(),self.textCountry.text(),
        self.textCcn.text(), self.textCcexp.text()]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count >0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')
        else:
            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs1=conn.cursor()
            curs2=conn.cursor()
            curs3=conn.cursor()
            ta = self.textAdd.text().split(" ")[0]
            s = self.textAdd.text().split(" ")[1]
            email = self.textEmail.text().split(" ")[0].strip("\t")
            query1 = f"INSERT into user (f_name, l_name, email, password, is_admin, is_suspend, is_current) values ('{self.textFirst.text()}', '{self.textLast.text()}', '{email}', 'password', 0, 0, 0) ON DUPLICATE KEY UPDATE f_name='{self.textFirst.text()}', l_name='{self.textLast.text()}'"
            #query2 = f"INSERT into address (address_num, street, city, state, zip, country, email) values('{ta}', '{s}', '{self.textCity.text()}', '{self.textState.text()}', '{self.textPc.text()}', '{self.textCountry.text()}', '{email}') ON DUPLICATE KEY UPDATE address_num='{ta}', street='{s}', city='{self.textCity.text()}', state='{self.textState.text()}', zip='{self.textPc.text()}', country='{self.textCountry.text()}'"
            #query3 = f"INSERT into credit_card (ccnumber, expiry, cvv, email) values('{self.textCcn.text()}', '{self.textCcexp.text()}', '123', '{email}') ON DUPLICATE KEY UPDATE ccnumber='{self.textCcn.text()}', expiry='{self.textCcexp.text()}', cvv=123"

            #does not work property, closer, no errors
            #query1 = f"UPDATE user SET f_name='{self.textFirst.text()}', l_name='{self.textLast.text()}' WHERE user.email = '{email}'"
            #query2 = f"UPDATE address SET address_num='{ta}', street='{s}', city='{self.textCity.text()}', state='{self.textState.text()}', zip='{self.textPc.text()}', country='{self.textCountry.text()}' WHERE address.email = '{email}'"
            #query3 = f"UPDATE credit_card SET ccnumber='{self.textCcn.text()}', expiry='{self.textCcexp.text()}', cvv=123 WHERE credit_card.email = '{email}'"

            #OLD, DOES NOT WORK AT ALL
            #query1 = f"INSERT into user (f_name, l_name, email, password, is_admin, is_suspend, is_current) values('{self.textFirst.text()}', '{self.textLast.text()}', '{email}', 'password', 0, 0, 0) ON DUPLICATE KEY UPDATE f_name='{self.textFirst.text()}', l_name='{self.textLast.text()}'"
            #query2 = f"INSERT into address (address_num, street, city, state, zip, country, email) values('{ta}', '{s}', '{self.textCity.text()}', '{self.textState.text()}', '{self.textPc.text()}', '{self.textCountry.text()}', '{email}') ON DUPLICATE KEY UPDATE address_num='{ta}', street='{s}', city='{self.textCity.text()}', state='{self.textState.text()}', zip='{self.textPc.text()}', country='{self.textCountry.text()}'"
            #query3 = f"INSERT into credit_card (ccnumber, expiry, cvv, email) values('{self.textCcn.text()}', '{self.textCcexp.text()}', '123', '{email}') ON DUPLICATE KEY UPDATE ccnumber='{self.textCcn.text()}', expiry='{self.textCcexp.text()}', cvv=123"

            #DOES NOT WORK IN DB, NO ERRORS
            #query1 = f"UPDATE user SET f_name='{self.textFirst.text()}', l_name='{self.textLast.text()}' WHERE email = '{email}'"
            #query2 = f"UPDATE address SET address_num='{ta}', street='{s}', city='{self.textCity.text()}', state='{self.textState.text()}', zip='{self.textPc.text()}', country='{self.textCountry.text()}' WHERE email = '{email}'"
            #query3 = f"UPDATE credit_card SET ccnumber='{self.textCcn.text()}', expiry='{self.textCcexp.text()}', cvv=123 WHERE email = '{email}'"

            curs1.execute(query1)
            #curs2.execute(query2)
            #curs3.execute(query3)
            curs1.close()
            curs2.close()
            curs3.close()
            conn.commit()
            conn.close()

            self.close()

#Edit Attraction
class EditA(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EditA, self).__init__(parent)
        self.setWindowTitle("Edit Attraction")
        self.resize(500,800)

        attrList2 = self.editADropDown()

        self.nameLabel = QLabel("*Name:", self)

        self.buttonUpdateA = QtWidgets.QPushButton('Select', self)
        self.buttonUpdateA.clicked.connect(self.handleAttrUp)
        self.attrLabel = QLabel("Attraction#:", self)
        self.textAttr = QtWidgets.QLineEdit(self)
        self.descLabel = QLabel("*Description:", self)
        self.textDesc = QtWidgets.QPlainTextEdit(self)

        self.add1Label = QLabel("*Address 1:", self)
        self.textAdd1 = QtWidgets.QLineEdit(self)
        self.add2Label = QLabel("Address 2:", self)
        self.textAdd2 = QtWidgets.QLineEdit(self)
        self.cityLabel = QLabel("*City:", self)
        self.textCity = QtWidgets.QLineEdit(self)
        self.countLabel = QLabel("*Country:", self)
        self.textCount = QtWidgets.QLineEdit(self)
        self.postLabel = QLabel("*Postal Code:", self)
        self.textPost = QtWidgets.QLineEdit(self)
        self.hourLabel = QLabel("Hours:", self)
        self.textHour = QtWidgets.QLineEdit(self)
        self.nearLabel = QLabel("*Nearest Public Trans # (1-8):", self)
        self.textNear = QtWidgets.QLineEdit(self)
        self.priceLabel = QLabel("Price:", self)
        self.textPrice = QtWidgets.QLineEdit(self)

        self.timeLabel = QLabel("Time Slots:", self)
        self.textTime = QtWidgets.QLineEdit(self)

        self.buttonDismiss = QtWidgets.QPushButton('Dismiss', self)

        self.buttonReport = QtWidgets.QPushButton('Submit Change', self)
        self.buttonReport.clicked.connect(self.handleEditA)

        self.dropAttr = QComboBox()
        self.dropAttr.insertItems(0, attrList2)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.dropAttr)
        layout.addWidget(self.buttonUpdateA)
        layout.addWidget(self.attrLabel)
        layout.addWidget(self.textAttr)
        layout.addWidget(self.descLabel)
        layout.addWidget(self.textDesc)

        layout.addWidget(self.add1Label)
        layout.addWidget(self.textAdd1)
        layout.addWidget(self.add2Label)
        layout.addWidget(self.textAdd2)
        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)
        layout.addWidget(self.countLabel)
        layout.addWidget(self.textCount)
        layout.addWidget(self.postLabel)
        layout.addWidget(self.textPost)
        layout.addWidget(self.hourLabel)
        layout.addWidget(self.textHour)
        layout.addWidget(self.nearLabel)
        layout.addWidget(self.textNear)
        layout.addWidget(self.priceLabel)
        layout.addWidget(self.textPrice)

        layout.addWidget(self.timeLabel)
        layout.addWidget(self.textTime)

        layout.addWidget(self.buttonReport)

        layout.addWidget(self.buttonDismiss)
        self.buttonDismiss.clicked.connect(self.close)




    def handleEditA(self):
        alist=[{self.dropAttr.currentText()}, self.textDesc.toPlainText(), self.textAdd1.text(), self.textPost.text(), self.textCity.text(), self.textCount.text(), self.textNear.text()]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')

        else:
            address1 = f"{self.textAdd1.text()} {self.textAdd2.text()} "
            address_to_query =f"{address1}, {self.textPost.text()}, {self.textCity.text()}, {self.textCount.text()}"

            query = f"INSERT into attraction (attraction_name, description, address, trans_no, res_needed) values('{self.dropAttr.currentText()}', '{self.textDesc.toPlainText()}', '{address_to_query}', {int(self.textNear.text())}, 0) ON DUPLICATE KEY UPDATE attraction_name='{self.dropAttr.currentText()}', description = '{self.textDesc.toPlainText()}', address='{address_to_query}', trans_no={int(self.textNear.text())}, res_needed=0"

            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs=conn.cursor()
            curs.execute(query)
            curs.close()
            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.warning(self, 'Success', f"Attraction has been edited")

            self.close()

    def handleAttrUp(self):

        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        curs.execute(f"SELECT * FROM attraction where attraction_name='{self.dropAttr.currentText()}'")
        curs.close()
        conn.close()

        for line in curs:

            address = line[2].split(",")
            street1, city, country, post = address[0].strip(), address[2].strip(), address[3].strip(), address[1].strip().split(" ")[0]
            desc, trans =  line[1], line[3]

        if line[0] != 'None':
            self.textDesc.setPlainText(f"{desc}")

        self.textAdd1.setText(f"{street1}")
        self.textCity.setText(f"{city}")
        self.textCount.setText(f"{country}")
        self.textPost.setText(f"{post}")
        self.textNear.setText(f"{trans}")

    def editADropDown(self):
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        attrList1 = []
        curs.execute(f"SELECT attraction_name FROM attraction")
        curs.close()
        conn.close()

        curs = [rows[0] for rows in curs]
        for rows in curs:
            attrList1.append(rows)

        return (attrList1)


class NewA(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewA, self).__init__(parent)
        self.setWindowTitle("New Attraction")
        self.resize(500,800)
        self.nameLabel = QLabel("*Name:", self)
        self.textName = QtWidgets.QLineEdit(self)
        self.attrLabel = QLabel("Attraction#:", self)
        self.textAttr = QtWidgets.QLineEdit(self)
        self.descLabel = QLabel("*Description:", self)
        self.textDesc = QtWidgets.QPlainTextEdit(self)
        self.add1Label = QLabel("*Address 1:", self)
        self.textAdd1 = QtWidgets.QLineEdit(self)
        self.add2Label = QLabel("Address 2:", self)
        self.textAdd2 = QtWidgets.QLineEdit(self)
        self.cityLabel = QLabel("*City:", self)
        self.textCity = QtWidgets.QLineEdit(self)
        self.countLabel = QLabel("*Country:", self)
        self.textCount = QtWidgets.QLineEdit(self)
        self.postLabel = QLabel("*Postal Code:", self)
        self.textPost = QtWidgets.QLineEdit(self)
        self.hourLabel = QLabel("Hours:", self)
        self.textHour = QtWidgets.QLineEdit(self)
        self.nearLabel = QLabel("*Nearest Public Trans # (1-8):", self)
        self.textNear = QtWidgets.QLineEdit(self)
        self.priceLabel = QLabel("Price:", self)
        self.textPrice = QtWidgets.QLineEdit(self)

        self.timeLabel = QLabel("Time Slots:", self)
        self.textTime = QtWidgets.QLineEdit(self)

        self.buttonDismiss = QtWidgets.QPushButton('Dismiss', self)

        self.buttonReport = QtWidgets.QPushButton('Add Attraction', self)
        self.buttonReport.clicked.connect(self.handleNewA)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.attrLabel)
        layout.addWidget(self.textAttr)
        layout.addWidget(self.descLabel)
        layout.addWidget(self.textDesc)

        layout.addWidget(self.add1Label)
        layout.addWidget(self.textAdd1)
        layout.addWidget(self.add2Label)
        layout.addWidget(self.textAdd2)
        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)
        layout.addWidget(self.countLabel)
        layout.addWidget(self.textCount)
        layout.addWidget(self.postLabel)
        layout.addWidget(self.textPost)
        layout.addWidget(self.hourLabel)
        layout.addWidget(self.textHour)
        layout.addWidget(self.nearLabel)
        layout.addWidget(self.textNear)
        layout.addWidget(self.priceLabel)
        layout.addWidget(self.textPrice)

        layout.addWidget(self.timeLabel)
        layout.addWidget(self.textTime)

        layout.addWidget(self.buttonReport)

        layout.addWidget(self.buttonDismiss)
        self.buttonDismiss.clicked.connect(self.close)


    def handleNewA(self):
        alist=[self.textName.text(),self.textDesc.toPlainText(),self.textAdd1.text(),self.textCity.text(),self.textCount.text(),self.textPost.text(),self.nearLabel.text()]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')
        else:

            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs=conn.cursor()
            curs.execute("SELECT * FROM attraction")
            curs.close()
            conn.close()

            attraction_list = {}
            for line in curs:
                attraction_list[line[2]] = line[0:2]+line[3:]

            address_to_query =f"{self.textAdd1.text()},  {self.textPost.text()}, {self.textCity.text()},{self.textCount.text()}"

            query = f"INSERT into attraction (attraction_name, description, address, trans_no, res_needed) values('{self.textName.text()}', '{self.textDesc.toPlainText()}', '{address_to_query}', {int(self.textNear.text())}, 0) ON DUPLICATE KEY UPDATE attraction_name='{self.textName.text()}', description='{self.textDesc.toPlainText()}', address='{address_to_query}', trans_no={int(self.textNear.text())}, res_needed=0"

            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs=conn.cursor()

            curs.execute(query)
            for item in curs:
                if item[0] == 1:
                    QtWidgets.QMessageBox.warning(self, 'Error', "Emails Already Exits")
            else:
                curs.execute(query)
                QtWidgets.QMessageBox.warning(self, 'Success', f"Attraction has been added")
            curs.close()
            conn.commit()
            conn.close()
            self.close()


#Attraction Reports
class Reports(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Reports, self).__init__(parent)
        self.setWindowTitle("Attraction Reports")

        self.attLabel = QLabel("Attraction:", self)
        self.textAtt = QtWidgets.QLineEdit(self)

        self.dateLabel = QLabel("Date:", self)
        self.textDate = QtWidgets.QLineEdit(self)

        self.reportLabel = QLabel("Report:", self)
        a="This is a variable"
        self.textReport = QtWidgets.QPlainTextEdit(a,self)

        self.rosterLabel = QLabel("Roster:", self)
        a="This is another variable"
        self.textRoster = QtWidgets.QPlainTextEdit(a,self)

        self.buttonReport = QtWidgets.QPushButton('Report', self)
        self.buttonReport.clicked.connect(self.handleReport)

        self.buttonDism2 = QtWidgets.QPushButton('Dismiss', self)
        self.buttonDism2.clicked.connect(self.close)


        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.attLabel)
        layout.addWidget(self.textAtt)

        layout.addWidget(self.dateLabel)
        layout.addWidget(self.textDate)

        layout.addWidget(self.reportLabel)
        layout.addWidget(self.textReport)

        layout.addWidget(self.rosterLabel)
        layout.addWidget(self.textRoster)

        layout.addWidget(self.buttonReport)
        layout.addWidget(self.buttonDism2)


    def handleReport(self):
        alist=[self.textDate.text(),self.textAtt.text(),
        self.textReport.toPlainText(),self.textRoster.toPlainText()]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')

        else:

            self.close()

#Edit Trips
# from mainwindow import Ui_MainWindow

class TripDetails(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TripDetails, self).__init__(parent)
        self.setWindowTitle("Edit Trip")

        self.cityLabel = QLabel("City:", self)
        self.textCity= QtWidgets.QLineEdit(self)

        self.dateLabel = QLabel("Date:", self)
        self.textDate = QtWidgets.QLineEdit(self)

        self.buttonInfo = QtWidgets.QPushButton('View Info', self)
        self.buttonInfo.clicked.connect(self.handleReport)

        self.reportLabel = QLabel("Time Slots:", self)

        self.textReport = QtWidgets.QLineEdit(a,self)

        self.rosterLabel = QLabel("Trip:", self)

        self.buttonReport = QtWidgets.QPushButton('Report', self)
        self.buttonReport.clicked.connect(self.handlTripDetailsDetails)

        self.buttonAddTrip = QtWidgets.QPushButton('Add Trip', self)
        self.buttonAddTrip.clicked.connect(self.add)
        #self.buttonAddTrip.clicked.connect(self.close)

        self.buttonDism3 = QtWidgets.QPushButton('Dismiss', self)
        self.buttonDism3.clicked.connect(self.close)

        self.textRoster = QtWidgets.QPlainTextEdit(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)

        layout.addWidget(self.dateLabel)
        layout.addWidget(self.textDate)

        layout.addWidget(self.buttonInfo)

        layout.addWidget(self.reportLabel)
        layout.addWidget(self.textReport)

        layout.addWidget(self.buttonAddTrip)

        layout.addWidget(self.rosterLabel)
        layout.addWidget(self.textRoster)

        layout.addWidget(self.buttonReport)
        layout.addWidget(self.buttonDism3)

    # def add(self):
    #     conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
    #     curs=conn.cursor()

    #     query = f"INSERT into activity {} {} {} {}"
    #     curs.execute(query)

    #     curs.close()
    #     conn.close()

    def handleTripDetails(self):
        alist=[self.textDate.text(),self.textCity.text(),
        self.textReport.text(),self.textRoster.setPlainText("info")]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')

        else:
            self.accept()

#Review Attraction
# from mainwindow import Ui_MainWindow

class Review(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Review, self).__init__(parent)
        self.setWindowTitle("Review")

        self.cityLabel = QLabel("City:", self)
        self.textCity = QtWidgets.QLineEdit(self)

        self.starLabel = QLabel("Enter a star Rating between 0 and 5:", self)
        self.textStar = QtWidgets.QLineEdit(self)

        self.reviewLabel = QLabel("Review:", self)

        self.textReview = QtWidgets.QPlainTextEdit(self)

        self.buttonReview = QtWidgets.QPushButton('Review', self)
        self.buttonReview.clicked.connect(self.handleReview)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)

        layout.addWidget(self.starLabel)
        layout.addWidget(self.textStar)

        layout.addWidget(self.reviewLabel)
        layout.addWidget(self.textReview)

        layout.addWidget(self.buttonReview)
    # def method(self):
    #     if self.frame.isVisible():
    #         # uncomment below, if you like symmetry :)
    #         # self.setMinimumSize(630, 150)
    #         self.resize(630, 150)
    #     else:
    #         self.setMinimumSize(630, 50)
    #         self.resize(630, 50)


    def handleReview(self):
        alist=[self.textStar.text(),self.textCity.text(), self.textReview.text()]
        count=0
        for x in alist:
            if x=="":
                count+=1
        if count>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')

        numlist=["1","2","3","4","5"]
        if self.textStar.text() not in numlist:
            QtWidgets.QMessageBox.warning(self, 'Error', "Write an integer between 0 and 5.")
        else:
            self.accept()

class Reports(QtWidgets.QDialog):
    def __init__(self):
        super(Reports, self).__init__()
        self.setWindowTitle("Edit Trip")
        self.theString = []

        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()

        query = f"SELECT max(acts_id) FROM activities"
        curs.execute(query)

        tripID = {}
        for line in curs:
            tripID = line
        self.newID = tripID[0]+1


        # self.TripIdLabel = QLabel(tripID, self)

        self.cityLabel = QLabel("City (Paris, Metz, Marseille)", self)
        self.textCity= QtWidgets.QLineEdit(self)

        self.dateLabel = QLabel("Date:\n(YYYY-MM-DD)", self)
        self.textDate = QtWidgets.QLineEdit(self)

        self.timeLabel = QLabel("Start Time:\n(HH:MM) Military Time", self)
        self.textTime = QtWidgets.QLineEdit(self)


        self.infoTitle = QLabel("View Info:\n  Select Option Below", self)
        self.infoLabel = QtWidgets.QPlainTextEdit(self)

        self.buttonInfo = QtWidgets.QPushButton('Find Attractions', self)
        self.buttonInfo.clicked.connect(self.checkEntries)

        self.TripIdTitle = QLabel(f"Trip Id: {self.newID}", self)
        #self.TripIdLabel = QLabel(self)

        self.buttonReview = QtWidgets.QPushButton('Add Activity', self)
        self.buttonReview.clicked.connect(self.addToList)
        #self.buttonReview.clicked.connect(self.checkEntries)


        self.reviewLabel = QLabel("..no activities selected..", self)

        self.costTitle = QLabel("Cost:", self)
        self.costLabel = QLabel(self)

        self.endTitle = QLabel("End Time:", self)
        self.endInfo = QLabel("..No Attraction Selected..", self)
        self.endInfo2 = QLabel(self)

        self.buttonAddTrip = QtWidgets.QPushButton('Add Trip', self)
        self.buttonAddTrip.clicked.connect(self.AtoDB)
        self.buttonAddTrip.hide()

        self.buttonDism3 = QtWidgets.QPushButton('Dismiss', self)
        self.buttonDism3.clicked.connect(self.close)



        curs.close()
        conn.close()


############################################3333
        self.cb = QComboBox()
        # a=[]
        # conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="attraction")
        # curs=conn.cursor()

        # query = ("SELECT name FROM attraction")

        # curs.execute(query)
        # curs=[rows[0] for rows in curs]
        # for rows in curs:
        #     print(rows)
        #     self.cb.addItem(rows)

        # self.cb.currentIndexChanged.connect(self.aprint)


###################################################

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.TripIdTitle)
        #layout.addWidget(self.TripIdLabel)


        layout.addWidget(self.cityLabel)
        layout.addWidget(self.textCity)

        layout.addWidget(self.dateLabel)
        layout.addWidget(self.textDate)

        layout.addWidget(self.timeLabel)
        layout.addWidget(self.textTime)


        layout.addWidget(self.endTitle)
        layout.addWidget(self.endInfo)
        layout.addWidget(self.endInfo2)
        self.endInfo2.hide()

        layout.addWidget(self.buttonInfo)

        layout.addWidget(self.infoTitle)
        layout.addWidget(self.cb)
        layout.addWidget(self.infoLabel)


        layout.addWidget(self.costTitle)
        layout.addWidget(self.costLabel)


        layout.addWidget(self.buttonReview)
        layout.addWidget(self.reviewLabel)
        self.buttonReview.hide()
        #self.buttonReview.clicked.connect(self.handleReport)

        layout.addWidget(self.buttonAddTrip)

        layout.addWidget(self.buttonDism3)


    def AtoDB(self):
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        query = (f"SELECT email from user WHERE is_current=1")
        curs.execute(query)
        for e in curs:
            email= e[0]
        # print(email)

        curs1=conn.cursor()
        now = f"{self.textDate.text()} {self.textTime.text()}:00"
        later = f"{self.textDate.text()} {self.endInfo2.text()}:00"

        toAdd = (f"{self.cb.currentText()} in {self.textCity.text()} on {self.textDate.text()} at {self.textTime.text()}")
        self.theString.append(toAdd)
        returnString = ""
        count = len(self.theString)
        while count >1:
            returnString+= self.theString[len(self.theString)-count]+'\n'
            count-=1
            # print(returnString)
        # print(returnString)
        # print(self.newID)
        # print(email)

        query1 = (f"INSERT into activities values('{returnString}',{self.newID},'{email}')")

        curs1.execute(query1)
        curs.close()
        curs1.close()
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.warning(self, 'Success', f"You have successfully added a trip!\nBon Voyage!")
        self.close()



    def add(self):
        #add attraction
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")

        for element in self.theList:
            curs=conn.cursor()
            now = f"{self.textDate.text()} {self.textTime.text()}:00"
            later = f"{self.textDate.text()} {self.endInfo2.text()}:00"
            query = f"INSERT into time_slot values('{self.cb.currentText()}', '{now}', '{later}', '{self.textCity.text()}', {self.costLabel.text()}, {self.newID})"
            # print(query)
            curs.execute(query)
            curs.close()
            conn.close()



    def numbers(self):
        #self.cost=
        time=self.textTime.text()
        start=time[0:2]
        start=int(start)
        end=start +1
        end=str(end)
        self.endTime=end+time[2:]

        self.endInfo2.setText(self.endTime)

    def updateinfo(self):
        self.cb.clear()
        self.attractionDB()
        self.endInfo.hide()
        self.endInfo2.show()

        time=self.textTime.text()
        start=time[0:2]
        start=int(start)
        end=start +1
        end=str(end)
        self.endTime=end+time[2:]

        self.endInfo2.setText(self.endTime)

    def attractionDB(self):
        numlist=["0","1","2","3","4","5","6","7","8","9"]
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        emptylist=[]
        attlist=[]
        query = (f"SELECT attraction_name FROM attraction where address like '%{self.textCity.text()}%' ")
        curs.execute(query)
        curs=[rows[0] for rows in curs]
        for rows in curs:
            attlist.append(rows)
        self.cb.clear()
        self.cb.insertItems(0,attlist)


    def checkEntries(self):
###########################
#Checking Time
        numlist=["0","1","2","3","4","5","6","7","8","9"]
        time=self.textTime.text()
        count=0

        if len(time)!=5:
            count+=1
        else:
            if time[0] not in numlist:
                count+=1
            elif time[1] not in numlist:
                count+=1
            elif int(time[0:2])>24:
                count+=1

            if time[3] not in numlist:
                count+=1
            elif time[4] not in numlist:
                count+=1
            elif int(time[3:5])>60:
                count+=1
            if time[2]!=":":
                count+=1


#Checking Date
        date=self.textDate.text()
        dcount=0


        if len(date)!=10:
            dcount+=1
        else:

            if date[0] not in numlist:
                dcount+=1
            elif date[1] not in numlist:
                dcount+=1
            elif date[2] not in numlist:
                dcount+=1
            elif date[3] not in numlist:
                dcount+=1
            elif date[5] not in numlist:
                dcount+=1
            elif date[6] not in numlist:
                dcount+=1
            elif date[8] not in numlist:
                dcount+=1
            elif date[9] not in numlist:
                dcount+=1
            elif int(date[:3])>2017:
                dcount+=1
            elif int(date[5:7])>12:
                dcount+=1

            elif int(date[8:])>31:
                dcount+=1

            if date[4]!="-" or date[7]!="-":
                dcount+=1

        if count>0 or dcount>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')
            self.cb.clear()
            self.infoLabel.clear()
            self.costLabel.clear()
            self.buttonReview.hide()
        elif self.textCity.text() not in "ParisMetzMarseille":
            self.buttonReview.hide()
            self.buttonAddTrip.hide()
            self.cb.clear()
            self.infoLabel.clear()
            self.costLabel.clear()
        else:
            self.buttonReview.show()
            self.cb.currentIndexChanged.connect(self.attInfo)
            self.cb.currentIndexChanged.connect(self.cost)
            self.cb.currentIndexChanged.connect(self.numbers)
            self.updateinfo()

    def cost(self):
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        attlist=[]
        query = (f"SELECT cost FROM activity WHERE attraction_name like '%{self.cb.currentText()}%' ")
        curs.execute(query)
        for rows in curs:
            attlist.append(str(rows[0]))
        self.costLabel.setText(attlist[0])
        curs.close()
        conn.close()

    def attInfo(self):
        attlist=[]
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()

        query = (f"SELECT description FROM attraction where attraction_name like '%{self.cb.currentText()}%' ")

        curs.execute(query)
        for rows in curs:
            cursdat = rows[0]

        if cursdat =='None':

            self.infoLabel.setPlainText("No Information on This Attraction.")

        else:
            self.infoLabel.setPlainText(f"{rows[0]}")

        curs.close()
        conn.close()


    def addToList(self):
        #remember to add :00 to time
        #Maybe get rid of
        # conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        # for element in self.theList:
        #     curs=conn.cursor()
        now = f"{self.textDate.text()} {self.textTime.text()}:00"
        later = f"{self.textDate.text()} {self.endInfo2.text()}:00"
        # #Maybe get rid of

        #self.theList.append(f"('{self.cb.currentText()}', '{now}', '{later}', 100, {self.costLabel.text()}, {self.newID})")

        toAdd = (f"{self.cb.currentText()} in {self.textCity.text()} on {self.textDate.text()} at {self.textTime.text()}")
        self.theString.append(toAdd)
        # print(self.theString)
        returnString = ""
        for l in self.theString:
            returnString+= l+"\n"

        # print(returnString)
        self.reviewLabel.setText(returnString)


        self.buttonAddTrip.show()


    def handleReport(self):
        date, startTime, endTime, attraction, city, cost, tripId = self.textDate.text(),self.textTime.text(), self.endTime, self.cb.currentText(), self.textCity.text(), self.costLabel.text(), self.TripIdLabel.text()
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        query = (f"INSERT into activity values({self.textDate.text()},{self.textTime.text()}, {self.endTime}, '{self.cb.currentText()}', '{self.textCity.text()}', {self.costLabel.text()}, {self.TripIdLabel.text()})")
        curs.execute(query)



class ShowDeets(QtWidgets.QDialog):
    def __init__(self):
        super(ShowDeets, self).__init__()
        self.setWindowTitle("Trip Details")
        layout = QtWidgets.QVBoxLayout(self)
        stringtoprint = ""


        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()
        query = (f"SELECT list_name FROM (activities join user using(email)) WHERE is_current=1")
        curs.execute(query)
        count = 1
        for a in curs:
            stringtoprint += f"Trip no: {count}\n"
            stringtoprint += a[0]+"\n\n"
            count+=1
        curs.close()
        conn.close()


        self.header = QLabel("Trips booked:\n", self)
        self.attrs = QLabel(stringtoprint, self)
        self.buttonDis = QtWidgets.QPushButton('Dismiss', self)


        layout.addWidget(self.header)
        layout.addWidget(self.attrs)
        layout.addWidget(self.buttonDis)

        self.buttonDis.clicked.connect(self.close)

# list_name varchar(2000),
#     acts_id int primary key auto_increment,
#     email varchar(254) not null,


class AttrReports(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AttrReports, self).__init__(parent)
        self.setWindowTitle("Attraction Reports")

        self.attLabel = QLabel("Attraction:", self)
        self.textAtt = QtWidgets.QLineEdit(self)
        self.textAtt.setText("Metz Cathedral")

        self.dateLabel = QLabel("Future Date (YYYY-MM-DD):", self)
        self.textDate = QtWidgets.QLineEdit(self)

        self.reportLabel = QLabel("Report:", self)



        self.rosterLabel = QLabel("Roster:", self)

        self.buttonTS = QtWidgets.QPushButton('Time Slots', self)
        self.buttonTS.clicked.connect(self.booked)

        self.buttonBookings = QtWidgets.QPushButton('Bookings', self)
        self.buttonBookings.clicked.connect(self.tripsStuff)

        self.dism = QtWidgets.QPushButton('Dismiss', self)
        self.dism.clicked.connect(self.close)

        self.list=QtWidgets.QListWidget(self)
        self.stufflist=QtWidgets.QListWidget(self)





        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.attLabel)
        layout.addWidget(self.textAtt)

        layout.addWidget(self.dateLabel)
        layout.addWidget(self.textDate)
        layout.addWidget(self.buttonTS)





        layout.addWidget(self.reportLabel)
        layout.addWidget(self.list)

        layout.addWidget(self.rosterLabel)


        layout.addWidget(self.buttonBookings)
        layout.addWidget(self.stufflist)
        layout.addWidget(self.dism)


    # def handleRep(self):
    #     alist=[self.textDate.text(),self.textAtt.text(),
    #     self.textReport.toPlainText()]
    #     count=0
    #     for x in alist:
    #         if x=="":
    #             count+=1
    #     if count>0:
    #         QtWidgets.QMessageBox.warning(self, 'Error', 'One or more spaces are not filled out correctly.')

    #     else:
    #         self.accept()
    def booked(self):
        dcount=0
        conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
        curs=conn.cursor()

        query = ("SELECT attraction_name FROM attraction")

        curs.execute(query)
        attlist=[]
        for rows in curs:
            for atts in rows:
                attlist.append(atts)
        if self.textAtt.text() not in attlist:
            dcount+=1


###########################
#Checking Date
        numlist=["0","1","2","3","4","5","6","7","8","9"]

        date=self.textDate.text()



        if len(date)!=10:
            dcount+=1
        else:

            if date[0] not in numlist:
                dcount+=1
            elif date[1] not in numlist:
                dcount+=1
            elif date[2] not in numlist:
                dcount+=1
            elif date[3] not in numlist:
                dcount+=1
            elif date[5] not in numlist:
                dcount+=1
            elif date[6] not in numlist:
                dcount+=1
            elif date[8] not in numlist:
                dcount+=1
            elif date[9] not in numlist:
                dcount+=1
            elif int(date[:3])>2017:
                dcount+=1
            elif int(date[5:7])>12:
                dcount+=1

            elif int(date[8:])>31:
                dcount+=1

            if date[4]!="-" or date[7]!="-":
                dcount+=1


        if dcount>0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please check Date or spelling of Attraction')
            self.buttonBookings.hide()
            self.list.clear()

            self.stufflist.clear()

        else:
            attlist=["8:00","12:00","16:00"]
            self.buttonBookings.show()
            for x in attlist:


                self.list.addItem(f"{x}")
    def tripsStuff(self):
        self.stufflist.clear()




        if self.list.currentItem().text()=="8:00":
            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs=conn.cursor()

            query = ("SELECT f_name FROM user LIMIT 3")

            curs.execute(query)
            attlist=[]
            for rows in curs:
                attlist.append(rows)
            if len(attlist)==3:

                self.stufflist.addItem("FULLY BOOKED\n--------------------")
            for x in attlist:
                self.stufflist.addItem(f"Customer: {x[0]}\nBooking: {self.list.currentItem().text()}\nDate: {self.textDate.text()}\n--------------------")

        elif self.list.currentItem().text()=="12:00":
            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs=conn.cursor()

            query = ("SELECT f_name FROM user where l_name like '%t%'LIMIT 3")

            curs.execute(query)
            attlist=[]
            for rows in curs:
                attlist.append(rows)
            if len(attlist)==3:
                self.stufflist.addItem("FULLY BOOKED\n--------------------")
            for x in attlist:
                self.stufflist.addItem(f"Customer: {x[0]}\nBooking: {self.list.currentItem().text()}\nDate: {self.textDate.text()}\n--------------------")
        elif self.list.currentItem().text()=="16:00":
            conn=pymysql.connect(host = 'localhost', user = 'root', password = '', db="team8")
            curs=conn.cursor()


            query = ("SELECT f_name FROM user where l_name like '%z%'LIMIT 3")

            curs.execute(query)
            attlist=[]
            for rows in curs:
                attlist.append(rows)
            if len(attlist)==3:
                self.stufflist.addItem("FULLY BOOKED\n--------------------")
            for x in attlist:
                self.stufflist.addItem(f"Customer: {x[0]}\nBooking: {self.list.currentItem().text()}\nDate: {self.textDate.text()}\n--------------------")

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        if val==1:
            admin = Admin()
            admin.show()
        if val==0:
            customer = Customer()
            customer.show()
        if val==2:
            registration = Registration()
            registration.show()
            if registration.exec_() == QtWidgets.QDialog.Accepted:
                customer = Customer()
                customer.show()

        sys.exit(app.exec_())

