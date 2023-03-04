import random
import string
import time

import win32clipboard
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from urlextract import URLExtract
from xtempmail import Email
from xtempmail.mail import EmailMessage, EMAIL
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from webdriver_auto_update import check_driver


path = "wd/chromedriver.exe"

check_driver('wd')


#Remove this and Change Userman you want like this : firstEmail = 'type your username here'
account = ''.join(random.choice(string.ascii_letters) for i in range(10))
# Change your password here
password = "0p;/9ol."

option = Options()
option.add_argument("--headless")
s = Service(path)

secondEmail = ''.join(random.choice(string.ascii_letters) for i in range(10))


extractor = URLExtract()
driver1 = webdriver.Chrome(service=s)


app1 = Email(name=account, ext=EMAIL.MAILTO_PLUS)
app2 = Email(name=secondEmail, ext=EMAIL.MAILTO_PLUS)



def crateAccount(link="https://quizlet.com/", account=account, driver = driver1):
    driver.get(link)

    driver.find_element(By.CSS_SELECTOR, "[aria-label='Sign up']").click()

    birthYear = Select(driver.find_element(By.CSS_SELECTOR, "[aria-label='birth_year']"))
    birthMonth = Select(driver.find_element(By.CSS_SELECTOR, "[aria-label='birth_month']"))
    birthDay = Select(driver.find_element(By.CSS_SELECTOR, "[aria-label='birth_day']"))

    birthYear.select_by_index(33)
    birthMonth.select_by_index(1)
    birthDay.select_by_index(1)

    driver.find_element(By.ID,"email").send_keys(f"{account}@mailto.plus")
    driver.find_element(By.ID,"password1").send_keys(password)

    try:
        time.sleep(1)
        driver.find_element(By.NAME,"is_free_teacher").click()

    finally:
        print("error when pressing teacher")

    try:
        time.sleep(1)
        driver.find_element(By.NAME, "TOS").submit()
    finally:
        print("error when pressing teacher")


def checkEmail(text: string,driver=driver1):
    urls = extractor.find_urls(text)
    driver.get(urls[1])

firstAccountorNot = True

def baca(data: EmailMessage,driver=driver1):
    checkEmail(data.text,driver)
    data.delete()  # delete message
    print(firstAccountorNot)
    if firstAccountorNot:
        referNewAccount()

def referNewAccount(driver=driver1):
    global firstAccountorNot,links
    firstAccountorNot = False

    driver.get("https://quizlet.com/refer-a-teacher")
    #time.sleep(100)
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Copy link']").click()

    win32clipboard.OpenClipboard()
    links = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    time.sleep(3)

    print(f"hi :{links}")




if __name__ == '__main__':
    crateAccount()
    links = ""


    try:
        while len(app1.get_all_message()) == 0:
            continue # wait
    except KeyboardInterrupt:
        app1.destroy()

    baca(app1.get_all_message()[0])
    #print(links)

    app1.destroy()
    app1.close()
    driver1.quit()


    driver2 = webdriver.Chrome(service=s)

    crateAccount(links,secondEmail,driver2)

    try:
        while len(app2.get_all_message()) == 0:
            continue # wait
    except KeyboardInterrupt:
        app2.destroy()

    baca(app2.get_all_message()[0],driver2)

    app2.destroy()

    print("===============================================================================")
    print(f"Your Account Name:{account}")
    print(f"Your Password:{password}")






