from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
def driverSetup():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return(browser)