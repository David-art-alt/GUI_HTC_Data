import sys
import os
import datenbank
import time
import PyQt6.QtGui as qtg
from PyQt6.QtCore import Qt
from PySide6 import *
from PyQt6.QtGui import QDoubleValidator
from PyQt6 import QtCore
import PyQt6.QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel, QSqlQuery, QSqlTableModel

username = ''

class DataInputWindow(qtw.QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()

        self.setFixedSize(300, 450)
        self.setWindowTitle("CHN Analysis Data")


        self.combo_prozess = qtw.QComboBox()
        self.combo_prozess.addItems(['RAW','HTC','Pyrolysis'])
        self.combo_label = qtw.QLabel("Process")
        self.combo = [self.combo_label, self.combo_prozess]

        self.sample_in = qtw.QLineEdit()
        #self.sample_in.setFixedWidth()
        self.sample_in_label = qtw.QLabel('Sample')
        self.sample =[self.sample_in_label, self.sample_in]

        self.carbon_in = qtw.QDoubleSpinBox()
        self.carbon_in_label = qtw.QLabel('Carbon    ')
        self.carbon_in_unit = qtw.QLabel('wt%')
        self.carbon = [self.carbon_in_label, self.carbon_in, self.carbon_in_unit]

        self.hydrogen_in = qtw.QDoubleSpinBox()
        self.hydrogen_in_label = qtw.QLabel('Hydrogen')
        self.hydrogen_in_unit = qtw.QLabel('wt%')
        self.hydrogen = [self.hydrogen_in_label, self.hydrogen_in, self.hydrogen_in_unit]

        self.nitrogen_in = qtw.QDoubleSpinBox()
        self.nitrogen_in_label = qtw.QLabel('Nitrogen  ')
        self.nitrogen_in_unit = qtw.QLabel('wt%')
        self.nitrogen = [self.nitrogen_in_label,self.nitrogen_in,self.nitrogen_in_unit]


        self.button_cancel = qtw.QPushButton('Cancel', clicked=self.closeEvent)
        self.button_enter = qtw.QPushButton('Enter', clicked=self.insert_database)
        self.button_add_data = qtw.QPushButton('Add Data', clicked=self.input_new_data)
        self.button_show_data = qtw.QPushButton('Show Data', clicked=self.show_data_table)
        self.buttons1 = [self.button_cancel,self.button_enter]
        self.buttons2 = [self.button_show_data, self.button_add_data]
        self.buttons = [self.button_cancel,self.button_enter,self.button_show_data, self.button_add_data]
        self.button_style(self.buttons)

        self.chn_layout = [self.combo,self.sample,self.carbon,self.hydrogen,self.nitrogen,self.buttons1,self.buttons2]
        self.layout()

        self.inputs = [self.carbon_in, self.hydrogen_in, self.nitrogen_in]
        self.define_Data_input()


        self.show()

    def define_Data_input(self):
        for i in self.inputs:
            i.setRange(0.00, 100.00)
            i.setValue(0.00)

    def layout(self):
        layout = qtw.QFormLayout()
        for elements in self.chn_layout:
            self.widget1 = qtw.QWidget()
            layout_h = qtw.QHBoxLayout(self.widget1)
            for j in elements:
                layout_h.addWidget(j)
            #layout.addRow(self.widget1)
                j.setFont(qtg.QFont('Arial', 18))
                f = j.font()
                f.setPointSize(18)
                j.setFont(f)
                self.setLayout(layout)
            layout.addRow(self.widget1)


    def insert_database(self):

        process = self.combo_prozess.currentText()
        sample = self.sample_in.text()
        carbon = self.carbon_in.text()
        hydrogen = self.hydrogen_in.text()
        nitrogen = self.nitrogen_in.text()
        print(username,process,sample,carbon,hydrogen,nitrogen)

        # Create the connection
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("analysisdata.sqlite")

        # Open the connection
        if not con.open():
            print("Database Error: %s" % con.lastError().databaseText())
            sys.exit(1)

        # Create a query and execute it right away using .exec()
        createTableQuery = QSqlQuery()
        createTableQuery.exec(
            """
            CREATE TABLE analysisdata (

                name VARCHAR(40) NOT NULL,
                sampleId VARCHAR(40) NOT NULL,
                process VARCHAR(40) NOT NULL,
                carbon FLOAT,
                hydrogen FLOAT,
                nitrogen FLOAT
                )
                """
        )

        print(con.tables())

        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """
            INSERT INTO analysisdata (
                name,
                sampleID,
                process
                carbon,
                hydrogen,
                nitrogen
            )
            VALUES (?, ?, ?,?,?,?)
            """
        )
        insertDataQuery.addBindValue('David')
        insertDataQuery.addBindValue('Char')
        insertDataQuery.addBindValue('HTC')
        insertDataQuery.addBindValue(40)
        insertDataQuery.addBindValue(10)
        insertDataQuery.addBindValue(3)
        insertDataQuery.exec()

    def input_new_data(self):
        self.sample_in.clear()
        for i in self.inputs:
            i.setValue(0.00)

    def show_data_table(self):
        #datenbank.createConnection()
        self.AnalysisdataWindow = datenbank.Analysisdata()
        self.AnalysisdataWindow.show()


    def closeEvent(self, event):

        reply = qtw.QMessageBox.question(self, 'Message',
                                         "Are you sure to quit?", qtw.QMessageBox.StandardButton.Yes |
                                         qtw.QMessageBox.StandardButton.No)

        if reply == qtw.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            pass

    def button_style(self, buttons):

        for i in buttons:
            i.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: "white";
                border-radius: 5px;
                border-style: outset;
                border-width: 1px;
                border-color: lightgrey;
                color: "black"
            }
            QPushButton:hover {
                background-color: lightgray;
                border-color: grey;
            }
            """)


class LoginWindow(qtw.QWidget):

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        # custom code goes here
        #self.setGeometry(300, 300, 400, 200)
        self.setFixedSize(400, 200)

        self.setWindowTitle('Login')
        self.label_username = qtw.QLabel('Username')
        self.label_password= qtw.QLabel('Password')
        label = [self.label_username,self.label_password]
        self.le_username = qtw.QLineEdit()
        self.le_password = qtw.QLineEdit()
        ledit = [self.le_username,self.le_password]

        for la,le  in zip(label,ledit):
            la.setFont(qtg.QFont('Arial', 20))
            f = le.font()
            f.setPointSize(20)
            le.setFont(f)


        self.le_password.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        self.button_cancel = qtw.QPushButton('Cancel',clicked=self.close_event_login)
        self.button_login = qtw.QPushButton('&Log In', clicked=self.check_credential)
        self.button_login.isDefault()
        #self.button_login.clicked.connect(self.check_credential)
        #self.button_login.setShortcut("Ctrl+Return")
        buttons = [self.button_cancel,self.button_login]
        self.button_style(buttons)


        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.button_cancel)
        hbox.addWidget(self.button_login)

        self.status = qtw.QLabel('')
        self.status
        self.status.setStyleSheet('font-size: 15px; color: red;')

        layout = qtw.QGridLayout()


        layout.addWidget(self.label_username, 0, 0)
        layout.addWidget(self.le_username, 0, 1)
        layout.addWidget(self.label_password, 1, 0)
        layout.addWidget(self.le_password, 1, 1)
        layout.addWidget(self.status, 2, 1)
        #layout.setRowStretch(2, 1)
        layout.addLayout(hbox, 3, 0, 1, 2)

        self.setLayout(layout)
        self.setLayout(layout)
        self.show()




    def check_credential(self):
        username = self.le_username.text()
        password = self.le_password.text()

        if password == 'IVET107':
            #self.create_connection
            time.sleep(1)
            self.DataInputWindow = DataInputWindow()
            self.DataInputWindow.show()
            self.close()
        else:
            self.status.setText('Password is incorrect')



    def close_event_login(self, event):

        reply = qtw.QMessageBox.question(self, 'Message',
                                         "Are you sure to quit Login?", qtw.QMessageBox.StandardButton.Yes |
                                         qtw.QMessageBox.StandardButton.No)

        if reply == qtw.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            pass


    def button_style(self,buttons):
        ''''''

        for i in buttons:
            i.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: "white";
                border-radius: 5px;
                border-style: outset;
                border-width: 1px;
                border-color: lightgrey;
                color: "black"
            }
            QPushButton:hover {
                background-color: lightgray;
                border-color: grey;
            }
            """)



def main():
    app = qtw.QApplication(sys.argv)
    login_window = LoginWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()