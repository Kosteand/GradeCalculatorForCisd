import tkinter as tk
from RetrieveGrades import *
import DriverSetup
m = tk.Tk()
driver = DriverSetup.driverSetup()
login = getLogin()
retrieveData(driver, login)