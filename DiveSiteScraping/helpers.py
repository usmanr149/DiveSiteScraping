import re
import time

from selenium.webdriver.common.by import By

def scrape_facebook_about_page(driver):
    club_email = None
    phone = None
    club_url = None

    elementLocator = driver.find_elements(By.CLASS_NAME, "x92rtbv")

    if len(elementLocator) > 0:
        elementLocator[0].click()
    time.sleep(2)

    potentials = driver.find_elements(By.CLASS_NAME, "x193iq5w.xeuugli.x13faqbe.x1vvkbs")
    for idx in range(len(potentials)):
        if club_email is None:
            email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', potentials[idx].text)
            if len(email) > 0:
                club_email = email
        if phone is None and potentials[idx].text == 'Mobile':
            if idx - 1 > 0:
                phone = potentials[idx - 1].text
        if club_url is None and potentials[idx].text == 'Website':
            if idx - 1 > 0:
                club_url = potentials[idx - 1].text

    return club_email, phone, club_url