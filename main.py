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

# Remove this and Change Username you want like this : firstEmail = 'type your username here'
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


def create_account(link="https://quizlet.com/", account_name=account, driver=driver1):
    driver.get(link)

    driver.find_element(By.CSS_SELECTOR, "[aria-label='Sign up']").click()

    birthYear = Select(driver.find_element(By.CSS_SELECTOR, "[aria-label='birth_year']"))
    birthMonth = Select(driver.find_element(By.CSS_SELECTOR, "[aria-label='birth_month']"))
    birthDay = Select(driver.find_element(By.CSS_SELECTOR, "[aria-label='birth_day']"))

    birthYear.select_by_index(33)
    birthMonth.select_by_index(1)
    birthDay.select_by_index(1)

    driver.find_element(By.ID, "email").send_keys(f"{account_name}@mailto.plus")
    driver.find_element(By.ID, "password1").send_keys(password)

    try:
        time.sleep(1)
        driver.find_element(By.NAME, "is_free_teacher").click()

    finally:
        print("error when pressing teacher")

    try:
        time.sleep(1)
        driver.find_element(By.NAME, "TOS").submit()
    finally:
        print("error when pressing teacher")


first_account_or_not = True


def check_email(data: EmailMessage, driver=driver1):
    urls = extractor.find_urls(data.text)
    driver.get(urls[1])
    data.delete()  # delete message
    print(first_account_or_not)
    if first_account_or_not:
        refer_account()


def refer_account(driver=driver1):
    global first_account_or_not, links
    first_account_or_not = False

    driver.get("https://quizlet.com/refer-a-teacher")
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Copy link']").click()

    win32clipboard.OpenClipboard()
    links = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    time.sleep(3)


if __name__ == '__main__':
    create_account()
    links = ""

    while len(app1.get_all_message()) == 0:
        continue  # wait until received message
    check_email(app1.get_all_message()[0])

    app1.destroy()
    app1.close()
    driver1.quit()

    driver2 = webdriver.Chrome(service=s)

    create_account(links, secondEmail, driver2)

    while len(app2.get_all_message()) == 0:
        continue  # wait until received message
    check_email(app2.get_all_message()[0], driver2)

    app2.destroy()
    driver2.quit()

    print("===============================================================================")
    print(f"Your Account Name:{account}")
    print(f"Your Password:{password}")
