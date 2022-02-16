import selenium
from selenium import webdriver
import urllib
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import re


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


def getFunctionReverse(problem):
    if '+' in problem:
        return subtract
    elif '-' in problem:
        return add
    elif '*' in problem:
        return divide
    elif '/' in problem:
        return multiply


driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver.get("https://rankyourbrain.com/mental-math/mental-math-test-normal/play")
# time.sleep(25)
try:
    myElem = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'beforeAnswer')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

timer = driver.find_element_by_id('counterTotal').text
while(timer != "00:00:01"):
    timer = driver.find_element_by_id('counterTotal').text
    beforeAnswer = driver.find_element_by_id(
        'beforeAnswer').text.replace(' ', '')
    afterAnswer = driver.find_element_by_id(
        'afterAnswer').text.replace(' ', '')
    original_problem = beforeAnswer + afterAnswer
    # Cases with 2 + 2 = ___
    if afterAnswer == '':
        problem = re.split('\+|-|\/|\*|=', beforeAnswer)[:-1]
        ans = str(getFunction(original_problem)(
            int(problem[0]), int(problem[-1])))
    # Cases with ___ + 2 = 4
    elif beforeAnswer == '':
        problem = re.split('\+|-|\/|\*|=', afterAnswer)[1:]
        ans = str(getFunctionReverse(original_problem)
                  (int(problem[-1]), int(problem[0])))
    # Cases with 8 / ___ = 2
    else:
        problem = [re.split('\+|-|\/|\*|=', beforeAnswer)
                   [0], re.split('\+|-|\/|\*|=', afterAnswer)[-1]]
        if '+' in original_problem:
            ans = str(subtract(int(problem[-1]), int(problem[0])))
        elif '-' in original_problem:
            ans = str(subtract(int(problem[0]), int(problem[-1])))
        elif '*' in original_problem:
            ans = str(divide(int(problem[-1]), int(problem[0])))
        elif '/' in original_problem:
            ans = str(divide(int(problem[0]), int(problem[-1])))

    box = driver.find_element_by_id('answer')
    # print(f'A: {problem[0]}, B: {problem[-1]}, Answer: {ans}')
    box.send_keys(ans)
