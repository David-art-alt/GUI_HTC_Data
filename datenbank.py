import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

class Analysisdata(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(450, 250)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(6)
        self.view.setHorizontalHeaderLabels([ "Name","SampleID","Process", "Carbon [wt%]", "Hydrogen [wt%]","Nitrogen [wt%]"])
        query = QSqlQuery("SELECT name,sampleId,prozess,carbon,hydrogen,nitrogen FROM analysisdata")
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            self.view.setItem(rows, 2, QTableWidgetItem(query.value(2)))
            self.view.setItem(rows, 3, QTableWidgetItem(query.value(3)))
            self.view.setItem(rows, 4, QTableWidgetItem(query.value(4)))
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("analysisdata.sqlite")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True

def show_data_table():
    app = QApplication(sys.argv)
    if not createConnection():
        sys.exit(1)
    AnalysisdataWindow = Analysisdata()
    AnalysisdataWindow.show()
    sys.exit(app.exec())




