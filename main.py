import random
import string
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from urlextract import URLExtract
from xtempmail import Email
from xtempmail.mail import EmailMessage, EMAIL
from selenium import webdriver
from webdriver_auto_update import check_driver
from fake_useragent import UserAgent

####################################################################################

# Remove this and Change Username you want like this : firstEmail = 'type your username here'
account = ''.join(random.choice(string.ascii_letters) for i in range(10))
# Change your password here
password = "0p;/9ol."

####################################################################################


path = "wd/chromedriver.exe"
check_driver('wd')

option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("−−lang=en")
ua = UserAgent()
userAgent = ua.random
option.add_argument(f'--user-agent={userAgent}')
print(userAgent)
s = Service(path)

second_account = ''.join(random.choice(string.ascii_letters) for i in range(10))

extractor = URLExtract()
driver1 = webdriver.Chrome(service=s, options=option)

email1 = Email(name=account, ext=EMAIL.MAILTO_PLUS)
email2 = Email(name=second_account, ext=EMAIL.MAILTO_PLUS)


def create_account(open_link="https://quizlet.com/", account_name=account, driver=driver1):
    driver.get(open_link)

    time.sleep(0.1)

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
        time.sleep(0.1)
        driver.find_element(By.NAME, "is_free_teacher").click()
    finally:
        pass  # If it works , don't touch this.

    try:
        time.sleep(0.1)
        driver.find_element(By.NAME, "TOS").submit()
    finally:
        pass  # If it works , don't touch this.


def check_email(data: EmailMessage, driver=driver1):
    urls = extractor.find_urls(data.text)
    driver.get(urls[1])
    data.delete()  # delete message


def refer_account(driver: webdriver = driver1) -> string:
    driver.get("https://quizlet.com/refer-a-teacher")
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Copy link']").click()

    copy_link: string = None

    for i in driver.find_elements(By.TAG_NAME, "input"):
        try:
            if i.get_attribute("value").startswith("https://quizlet.com/teacher-referral-invite"):
                copy_link = i.get_attribute("value")
                break
        finally:
            pass
    return copy_link


if __name__ == '__main__':
    print(f"Create first account for {account}")
    create_account()

    print("waiting for emails......")
    while len(email1.get_all_message()) == 0:
        continue  # wait until received message

    print("received email and opening......")
    check_email(email1.get_all_message()[0])

    link = refer_account()

    print(f"the refer link is {link}")

    email1.destroy()
    email1.close()
    driver1.quit()

    driver2 = webdriver.Chrome(service=s, options=option)
    print(f"Create second account for {second_account}")
    create_account(link, second_account, driver2)

    print("waiting for emails")
    while len(email2.get_all_message()) == 0:
        continue  # wait until received message

    print("received email and opening......")
    check_email(email2.get_all_message()[0], driver2)

    email2.destroy()
    driver2.quit()

    print("===============================================================================")
    print(f"Your Account Name:{account}")
    print(f"Your Password:{password}")
