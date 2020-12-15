from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from datetime import datetime
from JsonUtilities import *
from selenium.webdriver.support.wait import WebDriverWait


class NotAmazonException(Exception):
    pass

def l(str):
    print("%s : %s" % (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))

Config = json_to_obj('config.json')
LOGIN_MAIL = Config['Mail']
LOGIN_PASSWORD = Config['Password']
Link = Config['AmazonLink']
CARD_NUMBER = Config['cardNumber']
LIMIT_VALUE = int(Config['LimitValue'])
timeout = 5

driver = webdriver.Chrome("./chromedriver")
driver.get(Link);
cookies = driver.find_element_by_id('sp-cc-accept').click()

while True:
    while True:
        try:
            shop = driver.find_element_by_id('merchant-info').text #Checks if sold by amazon
            if 'Amazon' not in shop:
                raise NotAmazonException("not Amazon")
            driver.find_element_by_id('buy-now-button').click()
            break
        except NotAmazonException:
            time.sleep(2)
            driver.refresh()

    element_present = EC.presence_of_element_located((By.ID, 'ap_email'))
    WebDriverWait(driver, timeout).until(element_present)

    #LOGIN
    driver.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
    driver.find_element_by_id('continue').click()
    driver.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    driver.find_element_by_id('signInSubmit').click()

    element_present = EC.presence_of_element_located((By.ID, 'payment-information'))
    WebDriverWait(driver, 10000).until(element_present)
    #-------------------- BUYING ----------------------#

    #CHECKING THE PRICE
    price = driver.find_element_by_css_selector('td.grand-total-price').text
    value = float(price.split(' ')[0].replace(',', '.'))
    if value > LIMIT_VALUE:
        l('PRICE IS TOO LARGE.')
        continue

    #CHECKING PAYMENT INFORMATION
    c = driver.find_element_by_id('payment-information')
    cardnumber = int(c.find_element_by_css_selector("span[data-field=tail]").text) #GETS CURRENT CARD NUMBER
    if cardnumber != CARD_NUMBER:
        driver.find_element_by_id('payChangeButtonId').click() #CLICKS BUTTON TO CHANGE CARD
        element_present = EC.presence_of_element_located((By.XPATH, "//span[@data-number='{}']".format(CARD_NUMBER)))
        WebDriverWait(driver, 10000).until(element_present)
        #SELECT THE RIGHT CARD
        for element in driver.find_elements_by_class_name("pmts-credit-card-row"):
            if str(CARD_NUMBER) in element.get_attribute('innerHTML'):
                element.find_element_by_xpath(".//input[@name='ppw-instrumentRowSelection']").click()
        completeChange = driver.find_element_by_class_name('apx-compact-continue-action')
        completeChange.find_element_by_xpath(".//input[@type='submit']").click() #SAVE CHANGES



    submit = driver.find_element_by_id('subtotalsSection')
    submitButton = WebDriverWait(submit, 10).until(EC.presence_of_element_located((By.XPATH,".//input[@name='placeYourOrder1']")))
    try:
        while True:
            submitButton.click()
    except Exception:
        break

    break
l('ALL DONE.')
