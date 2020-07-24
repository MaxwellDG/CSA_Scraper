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
        totalResultsString = self.driver.find_element_by_id("ctl00_bodyContent_lbl_count").text
        totalResults = int(re.search(r'\d+', totalResultsString).group())
        totalPagesHere = math.ceil(totalResults / 100)
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
        self.driver.find_element_by_id("anchDetailedSearch").click()
        self.driver.implicitly_wait(30)
        firmInput = self.driver.find_element_by_id("ctl00_bodyContent_txtFirmName")
        firmInput.send_keys(searchText)

        self.driver.find_element_by_id("ctl00_bodyContent_iBtnDetailedSearch").click()
        self.driver.implicitly_wait(30)

        # record the total pages so Selenium knows the limit for "NextPage" clicks
        self.totalPages = self.getTotalPages()

        # start Preserve Logs before first 100-person packet is sent
        if TK.alertDialogForManualClick(
                "Alert: Preserve Logs",
                "Open devtools -> click \"Network\" tab -> checkmark \"Preserve Logs\". Keep DevTools window open."):
            try:

                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "ctl00_bodyContent_list_num_per_page")))
            finally:
                elementSelectLength = Select(self.driver.find_element_by_id("ctl00_bodyContent_list_num_per_page"))
                elementSelectLength.select_by_index(2)
                self.clickThroughPages()

    def clickThroughPages(self):
        while self.currentPage < self.totalPages:
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "ctl00_bodyContent_lbtnNext")))
            finally:
                self.driver.find_element_by_id("ctl00_bodyContent_lbtnNext").click()
                # find something better here than just sleeping
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
