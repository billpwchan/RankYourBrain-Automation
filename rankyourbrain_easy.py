import selenium
from selenium import webdriver
import urllib
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return int((1.0*a/b) + 0.5)


def getFunction(problem):
    if '+' in problem:
        return add
    elif '-' in problem:
        return subtract
    elif '*' in problem:
        return multiply
    elif '/' in problem:
        return divide


driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver.get("https://rankyourbrain.com/mental-math/mental-math-test-easy/play")
try:
    myElem = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'beforeAnswer')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

timer = driver.find_element_by_id('counterTotal').text
while(timer != "00:00:02"):
    timer = driver.find_element_by_id('counterTotal').text
    problem = driver.find_element_by_id('beforeAnswer').text
    problem = problem[:-2]
    problem = problem.split(' ')
    ans = str(getFunction(problem)(int(problem[0]), int(problem[-1])))
    box = driver.find_element_by_id('answer')
    box.send_keys(ans)
