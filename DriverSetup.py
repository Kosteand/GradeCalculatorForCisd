from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import time
class Driver:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        #self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)
        self.driver.get("https://launchpad.classlink.com/conroeisd")
    def checkForElementByXPath(driver, Xpath):
        try:
            element = driver.driver.find_element(By.XPATH, Xpath)
        except:
            return(False)
        return(True)
    def SSOLogin(driver, Username, Password):
        driver.username = Username
        driver.password = Password
        Password_input = driver.driver.find_element(By.NAME, "password")
        Password_input.send_keys(driver.password)
        Username_input = driver.driver.find_element(By.NAME, "username")
        Username_input.send_keys(driver.username)
        #WebDriverWait(driver.driver, 30).until(
            #EC.presence_of_element_located((By.ID, "signin")))
        Login = driver.driver.find_element(By.ID, "signin")
        Login.click()
        time.sleep(1.5)
        existsBoolean = driver.checkForElementByXPath("/html/body/div[2]/div/div[2]/div[1]/form/div[1]/input")
        if existsBoolean != True:
            return(True)
        else:
            driver.driver.refresh()
            return(False)

    def openStudentAccess(self):  # Not used currently
        time.sleep(1)
        StudentAccess = self.driver.find_element(By.XPATH, "//application[1]")
        StudentAccess.click()
        time.sleep(2)
        self.driver.get("https://pac.conroeisd.net/assignments.asp")
        time.sleep(2)
    def getGrades(self):
        print("IAM RUNNING")
        allTablesList = []
        allGrade = []
        nameList = []
        for i in range(1, 8):
            table = "/html/body/center/center" + i * "/center"
            tableGradesXPath = table + "/table[1]/tbody/tr[2]/td/table/tbody[1]"
            tableName = table + "/table[1]/tbody/tr[1]/td/font/strong"
            tableName = self.driver.find_element(By.XPATH, tableName)
            tableName = tableName.get_attribute("innerHTML")
            tableName = (tableName.split("•"))[0]
            temp = self.driver.find_element(By.XPATH,tableGradesXPath).find_elements(By.XPATH, "tr")
            temp.pop(- 1)
            temp.pop(0)
            allGrade.append(temp)
            nameList.append(tableName)
            temp = []
        allGradesWithWeight = []
        tempGradeWithWeightList = []
        for i in allGrade:
            for item in i:
                gradeName = item.find_element(By.XPATH, "td[3]")
                gradeWeight = item.find_element(By.XPATH, "td[6]")
                temp = item.find_element(By.XPATH, "td[9]")
                temp = temp.get_attribute("innerHTML")
                gradeWeight = gradeWeight.get_attribute("innerHTML")
                grade = item.find_element(By.XPATH, "td[5]")
                grade = grade.get_attribute("innerHTML")
                if grade.__contains__("\"red\">Z"):
                    grade = 0
                if grade == "-" or (temp == "0.00" ):
                    print("x")
                    gradeWeight = 0
                    grade = 0
                gradeType = item.find_element(By.XPATH, "td[4]")
                grade = (float(grade) * 10) + 50
                tempList = [grade, gradeType.get_attribute("innerHTML"), gradeWeight, gradeName.get_attribute("innerHTML")]
                tempGradeWithWeightList.append(tempList)
            allGradesWithWeight.append(tempGradeWithWeightList)
            tempGradeWithWeightList = []
        gradesWithNamesAndWeights = []
        for item in range(len(nameList)):
            gradesWithNamesAndWeights.append([nameList[item], allGradesWithWeight[item]])
        return(gradesWithNamesAndWeights)