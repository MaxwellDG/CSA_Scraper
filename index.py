import math
import time
import re
from tkinter import E

import selenium

import tkui

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

securities = [
    "BMO NESBITT BURNS",
    "CIBC WORLD MARKETS",
    "EDWARD JONES",
    "IPC INVESTMENT CORPORATION",
    "LEEDE JONES GABLE INC.",
    "MACKIE RESEARCH CAPITAL",
    "NATIONAL BANK FINANCIAL",
    "VENTUM FINANCIAL CORP",
    "iA Private Wealth",
    "Aligned Capital Partners",
    "DESJARDINS SECURITIES",
    "ATB SECURITIES	",
    "HAYWOOD SECURITIES",
    "Canaccord Genuity Corp",
    "RAYMOND JAMES LTD.",
    "RBC DOMINION SECURITIES",
    "RICHARDSON GMP LIMITED",
    "SCOTIA SECURITIES",
    "TD SECURITIES"
]

class AdvancedScraper:

    baseUrl = "https://www.securities-administrators.ca/nrs"
    baseUrlForSelenium = "https://www.securities-administrators.ca/nrs/nrsearchprep.aspx"

    def __init__(self):
        self.currentPage = 1
        self.currentSecurity = 0
        self.totalPages = 0
        self.previousNumber = 0
        # self.proxy = ProxyManager()
        # self.server = self.proxy.start_server()
        # self.client = self.proxy.start_client()
        self.driver = self.initDriver()

    def initDriver(self):
        driver = ChromeDriverManager().install()
        cService = webdriver.ChromeService(executable_path=driver)
        webdriver.Chrome(service=cService)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--proxy-server={}'.format(self.client.proxy))
        # options.add_argument(('--headless'))
        return webdriver.Chrome(options=options)

    def getTotalPages(self):
        self.driver.implicitly_wait(10)
        totalResultsString = self.driver.find_element(By.ID, 'tblIndivResults_info')

        while not totalResultsString.text: # I dunno why but it takes a moment to recognize the string inside the div here
            time.sleep(1)

        totalResults = re.findall(r'\d{0,3}[\,]?\d{1,3}', totalResultsString.text)
        value = totalResults[-1]
        intValue = int(value.replace(',', ''))

        totalPagesHere = math.ceil(intValue / 100)
        return self.totalPages + totalPagesHere

    def getSecurityForSearch(self, entryText, listBoxSelection):
        TK.minimizeTKWindow()
        if entryText:
            self.beginEleniumNavigation(entryText)
        else:
            self.beginEleniumNavigation(self.securities[listBoxSelection[0]])

    def beginEleniumNavigation(self, searchText):
        # initial navigation into search results
        self.driver.set_page_load_timeout(30)

        self.driver.get(AdvancedScraper.baseUrlForSelenium)
        self.driver.find_element(By.ID, "textAdvSearch").click()
        self.driver.implicitly_wait(10)
        firmInput = self.driver.find_element(By.ID, "txtDetSearchFirmName")
        firmInput.send_keys(searchText)
        self.driver.find_element(By.ID, "btnSearch").click()

        # record the total pages so Selenium knows the limit for "NextPage" clicks
        self.totalPages = self.getTotalPages()
        # start Preserve Logs before first 100-person packet is sent
        if TK.alertDialogForManualClick(
                "Alert: Preserve Logs",
                "Open devtools -> click \"Network\" tab -> checkmark \"Preserve Logs\". Keep DevTools window open."):
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.NAME, "tblIndivResults_length")))
            finally:
                elementSelectLength = Select(self.driver.find_element(By.NAME, "tblIndivResults_length"))
                elementSelectLength.select_by_index(3)
                self.clickThroughPages()


    def clickThroughPages(self):
        while self.currentPage <= self.totalPages:
            try:
                self.driver.find_element(By.ID, "tblIndivResults_next").click()
                self.currentPage += 1
            except ElementClickInterceptedException as ex:
                self.driver.execute_script("window.scrollTo(0, 100)") # wiggle off the obscured image
            except StaleElementReferenceException:
                print('Stale element. Continue')
            finally:
                time.sleep(3)

        if TK.alertDialogForManualClick("Alert: Export Har File",
                                        "- In DevTools Network tab click \"Export Har...\"\n"
                                        "- Navigate to the folder you have designated as your 'Save Location' \n"
                                        "- Name files however you'd like but ensure they stay in this specific "
                                        "directory"):
            self.reset()

    def reset(self):
        self.currentPage = 1
        self.totalPages = 0


if "__main__" == __name__:
    advancedScraper = AdvancedScraper()
    TK = tkui.TkUI(advancedScraper)
    TK.initWidgets()
