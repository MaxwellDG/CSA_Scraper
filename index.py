import math
import time
import re

import tkui

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class AdvancedScraper:

    baseUrl = "https://www.securities-administrators.ca/nrs"
    baseUrlForSelenium = "https://www.securities-administrators.ca/nrs/nrsearchprep.aspx"
    securities = ["BMO NESBITT BURNS",
                  "CIBC WORLD MARKETS",
                  "EDWARD JONES",
                  "IPC INVESTMENT CORPORATION",
                  "LEEDE JONES GABLE INC.",
                  "MACKIE RESEARCH CAPITAL",
                  "NATIONAL BANK FINANCIAL",
                  "PI FINANCIAL CORP",
                  "RAYMOND JAMES LTD.",
                  "RBC DOMINION SECURITIES",
                  "RICHARDSON GMP LIMITED",
                  "SCOTIA SECURITIES",
                  "TD SECURITIES"]

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
        # webdriver.Chrome(ChromeDriverManager().install()) # <--- holy grail? How do I find if it's already present
        # though.. (for a conditional check)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--proxy-server={}'.format(self.client.proxy))
        # options.add_argument(('--headless'))
        return webdriver.Chrome(options=options)

    def getTotalPages(self):
        # WebDriverWait(self.driver, 30).until(EC.presence_of_element_located("#tblIndivResults_info"))
        self.driver.implicitly_wait(30)
        totalResultsString = self.driver.find_element(By.ID, 'tblIndivResults_info')
        
        # Get all the elements available with tag name 'p'
        elements = totalResultsString.find_elements(By.TAG_NAME, 'p')
        for e in elements:
            print(e)
            print(e.text)

        print("who dis")
        print(totalResultsString.text)

        totalResults = re.findall(r'\d+', totalResultsString.text)
        print("total results: ", totalResults)

        totalPagesHere = math.ceil(int(totalResults[-1]) / 100)
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
        self.driver.implicitly_wait(30)
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
        while self.currentPage < self.totalPages:
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(By.ID, "tblIndivResults_next"))
                self.driver.find_element(By.ID, "tblIndivResults_next").click();
            except :
                (org.openqa.selenium.StaleElementReferenceException ex)
            finally:
                time.sleep(5)
                self.currentPage = self.currentPage + 1

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
