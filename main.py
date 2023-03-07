from RetrieveGrades import *
import DriverSetup
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, \
    QVBoxLayout, QListWidget, QAbstractItemView
from DriverSetup import *
import shelve
from datetime import date
from pathlib import Path
majorGradeWeight = 0
majorGradeTotal = 0
minorGradeWeight = 0
minorGradeTotal = 0
fullGradeList = 0
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
            w.button2.show()
            w.button3.show()
            self.close()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("main Window")
        self.resize(600,600)
        self.button = QPushButton("Retrieve Grades", self)
        self.button2 = QPushButton("Get Average", self)
        self.button2.move(0,30)
        self.button2.hide()
        self.button3 = QPushButton("Plug In grades", self)
        self.button3.move(0, 60)
        self.button3.hide()
        self.button.clicked.connect(self.launchGradeRetrieve)
        self.button2.clicked.connect(self.button2Event)
        self.button3.clicked.connect(self.launchGradePlguin)
        self.tempGradeList = [[],[],[],[],[],[],[]]
        path = Path('Grades/grades' + str(date.today()) + '.db.dat')
        if path.is_file():
            self.button2.show()
            self.button3.show()
            x = shelve.open('Grades/grades' + str(date.today()) + '.db')
            self.gradeList = x["key"]
            self.gradeList = self.gradeList[0]
            classListTosave = []
            for i in self.gradeList:
                classListTosave.append(i[0])
            s = shelve.open('PermenantFiles/classes.db')['key'] = [classListTosave]

        else:
            print("No such file")
    def launchGradeRetrieve(self):
        driver = Driver()
        self.w = RetrieveGradesWindow(driver)
        self.w.show()
    def button2Event(self):
        self.p = GradePredict(self)
        self.p.show()
    def launchGradePlguin(self):
        self.pluginWindow = addGrades(mainWindow=self)
        self.pluginWindow.show()
        self.hide()
    def setTempList(self, tempList):
        self.tempGradeList = tempList
class GradePredict(QWidget):
    def __init__(self, mainWindow:MainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        r = shelve.open('Grades/grades' + str(date.today()) + '.db')
        print(originalGradeBeforePlugIns)
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
        self.listSelectForClasses = Listselect(gradesPredict=self, namelist=self.nameList, mainWindow=self.mainWindow)
        print(2)
        self.listSelectForClasses.show()

class Listselect(QListWidget):
    def __init__(self, gradesPredict:GradePredict, namelist, mainWindow:MainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.gradesList = gradesPredict.gradesList

        self.nameList = namelist
        s = shelve.open('PermenantFiles/classes.db')['key'] = [self.nameList]
        print(gradesPredict.gradesList)
        for item in self.nameList:
            self.addItem(item)
        self.itemSelectionChanged.connect(self.itemActivated_event)
    def itemActivated_event(self):
        self.chosenName = (self.currentItem().text())
        print(5)
        self.chosenIndexGradeType = self.nameList.index(self.chosenName)
        print(6)
        print(self.mainWindow.tempGradeList)
        print(7)
        print(self.mainWindow.tempGradeList[self.chosenIndexGradeType])
        print(8)
        self.addongradeList = self.mainWindow.tempGradeList[self.chosenIndexGradeType]
        self.classGradeList = self.gradesList[self.chosenIndexGradeType]
        print(self.chosenName)
        self.classTypeList = classTypeList(self, self.mainWindow)
        self.classTypeList.show()
        self.close()

class classTypeList(QListWidget):
    def __init__(self, listSelect:Listselect, mainWindow:MainWindow ):
        self.mainWindow = mainWindow
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
        self.close()
        classGradeList = self.listSelect.classGradeList
        grade = grades(self.chosenName, classGradeList, self.listSelect.addongradeList)
        grade.calculateAverage(self.mainWindow)


class grades:
    def __init__(self, classType, classGradeList, tempList):
        self.classType = classType
        self.tempList = tempList
        self.classGradeList = classGradeList
        self.minorGrade = 0
        self.minorWeight = 0
        self.majorGrade = 0
        print(110)
        self.majorWeight = 0
    def calculateAverage(self, mainWindow:MainWindow):
        for item in self.tempList:
            print(item)
            if item[1] == "Major":
                print("Major")
                print("TOTAL OF GRADE IS" + str(self.majorGrade))
                self.majorGrade = (float(self.majorGrade)) + (float(item[0])) * float(item[2])
                self.majorWeight = (float(self.majorWeight) + float(item[2]))
                print("grade is" + str(item[0]))
                print("weight is" + str(item[2]))
                print("Total grade" + str(float(self.majorGrade)))
                print("Total weight" + str((float(self.majorWeight))))
            if item[1] == "Daily":
                print("daily")
                self.minorGrade = (float(self.minorGrade)) + (float(item[0])) * float(item[2])
                self.minorWeight = (float(self.minorWeight) + float(item[2]))
                print("grade is" + str(item[0]))
                print("weight is" + str(item[2]))
                print("Total grade" + (str(self.minorGrade)))
                print("Total weight" + str(self.minorWeight))

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
        majorGradeTotal = (self.majorGrade)
        majorGradeWeight = (self.majorWeight)
        minorGradeTotal = (self.minorGrade)
        minorGradeWeight = (self.minorWeight)
        finalMajorGrade = float(self.majorGrade/self.majorWeight)
        print(finalMajorGrade)
        finalDailyGrade = float(self.minorGrade/self.minorWeight)
        print(finalDailyGrade)
        finalGrade = float(temp[1])*(finalDailyGrade)+float(temp[0])*finalMajorGrade
        print("Final grade"+str(finalGrade))
class addGrades(QWidget):
    def __init__(self, mainWindow:MainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.resize(600, 600)
        self.setWindowTitle("NewGradeEntryBox")
        msg = QLabel(self)
        msg.setText("Grade:")
        msg.move(0, 100)
        msg2 = QLabel(self)
        msg2.setText("Weight:")
        msg2.move(0, 150)
        self.gradeLine = QLineEdit(self)
        self.gradeLine.move(51, 100)
        self.weightLine = QLineEdit(self)
        self.weightLine.move(51, 150)
        self.finishButton = QPushButton("Finished Entering Grades", self)
        self.finishButton.move(0,200)
        self.enterButton = QPushButton("Enter Another Grade", self)
        self.enterButton.move(130, 200)
        self.finishButton.clicked.connect(self.finishButtonEvent)
        print(2)
        self.enterButton.clicked.connect(self.enterButtonEvent)
    def enterButtonEvent(self):
        self.classSelect = ClassSelect(self)
        self.classSelect.show()
        self.grade = self.gradeLine.text()
        self.weight = self.weightLine.text()
    def finishButtonEvent(self):
        self.mainWindow.show()
        self.close()

    def gotClassName(self, index):
        self.mainWindow.tempGradeList[index].append([self.grade, "Major", self.weight, ""])
        ##self.mainWindow.tempGradeList[index].append([self.grade, "Major", self.weight, ""])



class ClassSelect(QListWidget):
    def __init__(self, addGrades:addGrades):
        super().__init__()
        self.addGrades = addGrades
        print(5)
        r = shelve.open('PermenantFiles/classes.db')
        classList2 = (r['key'])
        print(6)
        classList2 = classList2[0]
        for item in classList2:
            print(item)
            self.addItem(item)
        self.itemSelectionChanged.connect(self.itemActivated_event)
    def itemActivated_event(self):
        self.index = self.currentRow()
        self.chosenName = (self.currentItem().text())
        self.close()
        self.addGrades.gotClassName(self.index)
        print(self.chosenName)

path = Path('Grades/grades' + str(date.today()) + '.db.dat')
if path.is_file():
    r = shelve.open('Grades/grades'+str(date.today())+'.db')
    originalGradeBeforePlugIns = (r['key'])
    print(originalGradeBeforePlugIns)
    fullGradeList = originalGradeBeforePlugIns


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
sys.exit(app.exec_())