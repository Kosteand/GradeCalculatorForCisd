from RetrieveGrades import *
import DriverSetup
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, \
    QVBoxLayout, QListWidget, QAbstractItemView
from DriverSetup import *
import shelve
from datetime import date
from pathlib import Path
class RetrieveGradesWindow(QWidget):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.resize(600,600)
        self.setWindowTitle("EntryBox")
        msg = QLabel(self)
        msg.setText("Username:")
        msg.move(0,100)
        msg2 = QLabel(self)
        msg2.setText("Password")
        msg2.move(0,150)
        self.wrongPassLabel = QLabel(self)
        self.wrongPassLabel.hide()
        self.wrongPassLabel.setMinimumSize(150, 10)
        self.wrongPassLabel.move(100, 300)
        self.passwordLine = QLineEdit(self)
        self.passwordLine.move(51, 150)
        self.usernameLine = QLineEdit(self)
        self.usernameLine.move(51, 100)
        self.button = QPushButton("Enter", self)
        self.button.clicked.connect(self.login)
        self.button.move(51,200)
    def login(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        if (self.driver.SSOLogin(username, password)) == False:
            self.wrongPassLabel.show()
            self.wrongPassLabel.setStyleSheet("background-color: red")
            self.wrongPassLabel.setText("Wrong password or username!")
        else:
            self.wrongPassLabel.setMinimumSize(200, 10)
            self.wrongPassLabel.setStyleSheet("background-color: green")
            self.wrongPassLabel.setText("Correct username and Pass. Wait.")
            self.wrongPassLabel.show()
            self.button.hide()
            self.driver.openStudentAccess()
            allGrades = (self.driver.getGrades())
            print(1)
            s = shelve.open('Grades/grades'+str(date.today())+'.db')['key'] = [allGrades]
            #r = shelve.open('grades/grades'+str(date.today())+'.db')
            #print(r['key'])
            w.button2.show()
            self.close()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("main Window")
        self.resize(600,600)
        self.button = QPushButton("Retrieve Grades", self)
        self.button2 = QPushButton("Plug in grades", self)
        self.button2.move(0,30)
        self.button2.hide()
        self.button.clicked.connect(self.launchGradeRetrieve)
        self.button2.clicked.connect(self.launchGradePredict)
        path = Path('Grades/grades' + str(date.today()) + '.db.dat')
        if path.is_file():
            self.button2.show()
        else:
            print("No such file")
    def launchGradeRetrieve(self):
        driver = Driver()
        self.w = RetrieveGradesWindow(driver)
        self.w.show()
    def launchGradePredict(self):
        self.p = GradePredict()
        self.p.show()
class GradePredict(QWidget):
    def __init__(self):
        super().__init__()
        r = shelve.open('Grades/grades' + str(date.today()) + '.db')
        self.temp = r["key"]
        self.nameList = []
        for i in (self.temp)[0]:
            self.nameList.append(i[0])
        self.gradesList = []
        for i in (self.temp)[0]:
            self.gradesList.append(i[1])
        self.resize(600, 600)
        self.setWindowTitle("Plug In Grades")
        self.button = QPushButton("Select class", self)
        self.button.clicked.connect(self.launchSelect)
    def launchSelect(self):
        print(1)
        self.p = Listselect(self, namelist=self.nameList)
        print(2)
        self.p.show()

class Listselect(QListWidget):
    def __init__(self, gradesPredict:GradePredict, namelist):
        super().__init__()
        self.gradesList = gradesPredict.gradesList
        self.nameList = namelist
        print(gradesPredict.gradesList)
        for item in self.nameList:
            self.addItem(item)
        self.itemSelectionChanged.connect(self.itemActivated_event)
    def itemActivated_event(self):
        self.chosenName = (self.currentItem().text())
        self.chosenIndexGradeType = self.nameList.index(self.chosenName)
        self.classGradeList = self.gradesList[self.chosenIndexGradeType]
        print(self.chosenName)
        print(1)
        self.classTypeList = classTypeList(self)
        self.classTypeList.show()
        self.close()
        print(2)
        print(self.chosenIndexGradeType)
        print(1000)

class classTypeList(QListWidget):
    def __init__(self, listSelect:Listselect ):
        super().__init__()
        print(3)
        self.listSelect = listSelect
        for item in ["AP", "Level", "Honors"]:
            print(4)
            self.addItem(item)
            print(6)
        self.itemSelectionChanged.connect(self.itemActivated_event)
        print(5)
    def itemActivated_event(self):
        self.chosenName = (self.currentItem().text())
        print(102)
        self.close()
        classGradeList = self.listSelect.classGradeList
        print(103)
        grade = grades(self.chosenName, classGradeList)
        print(107)
        grade.calculateAverage()


class grades:
    def __init__(self, classType, classGradeList):
        self.classType = classType
        self.classGradeList = classGradeList
        self.minorGrade = 0
        self.minorWeight = 0
        self.majorGrade = 0
        print(110)
        self.majorWeight = 0
    def calculateAverage(self):
        for item in self.classGradeList:
            print(item)
            if item[1] == "Major":
                print("Major")
                print("TOTAL OF GRADE IS"+ str(self.majorGrade))
                self.majorGrade = (float(self.majorGrade))+(float(item[0]))*float(item[2])
                self.majorWeight = (float(self.majorWeight) + float(item[2]))
                print("grade is"+str(item[0]))
                print("weight is"+ str(item[2]))
                print("Total grade"+str(float(self.majorGrade)))
                print("Total weight"+ str((float(self.majorWeight))))
            if item[1] == "Daily":
                print("daily")
                self.minorGrade = (float(self.minorGrade)) +(float(item[0]))*float(item[2])
                self.minorWeight = (float(self.minorWeight) + float(item[2]))
                print("grade is" + str(item[0]))
                print("weight is" + str(item[2]))
                print("Total grade"+(str(self.minorGrade)))
                print("Total weight" +str(self.minorWeight))
        if self.classType == "AP":
            temp = [0.8, 0.2]
        elif self.classType == "Honors":
            temp =  [0.75, 0.25]
        elif self.classType == "Level":
            temp =  [0.7, 0.3]
        print(self.majorGrade)
        print(self.majorWeight)
        print(self.minorGrade)
        print(self.minorWeight)
        finalMajorGrade = float(self.majorGrade/self.majorWeight)
        print(finalMajorGrade)
        finalDailyGrade = float(self.minorGrade/self.minorWeight)
        print(finalDailyGrade)
        finalGrade = float(temp[1])*(finalDailyGrade)+float(temp[0])*finalMajorGrade
        print("FInal grade"+finalGrade)








app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
sys.exit(app.exec_())