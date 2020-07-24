from bs4 import BeautifulSoup
import os
import json
from tkinter import messagebox
import datetime
import csv


def parse(activeFile, activeDir):
    listOfLists = []
    workingFile = os.path.join(activeDir, activeFile)
    print(activeDir)
    print(workingFile)
    with open(workingFile, encoding="utf8") as f:
        data = json.load(f)
        for entry in data['log']['entries']:
            if entry['response']['content']['mimeType'] == "text/plain" or entry['response']['content']['mimeType'] == "text/plain; charset=utf-8":
                try:
                    soup = BeautifulSoup(entry['response']['content']['text'], 'html.parser')
                    tables = soup.find_all("table", class_="gridview_style")
                except KeyError:
                    messagebox.showinfo("Error: parsing", "Parsing encountered an error. Tell Max he's stupid.")
                for table in tables:
                    trs = table.find_all("tr")
                    for tr in trs:
                        tds = tr.find_all("td")
                        workingList = ['placeholder', 'placeholder']
                        for td in tds:
                            # An abomination of code. If you were smarter you could've just done like 'evens/odds' or
                            # something like that
                            try:
                                workingList[0] = td.a.text
                            except AttributeError:
                                workingList[1] = td.span.text
                                listOfLists.append(workingList)
    return listOfLists


def compareDicts(oldList, newList):
    listFreshPrey = []
    for entry in oldList:
        if entry not in newList:
            listFreshPrey.append(entry)
    return listFreshPrey


def compareDictsNewEntries(oldDict, newDict):
    listOfEscapees = []
    for entry in newDict:
        if entry not in oldDict:
            listOfEscapees.append((entry, newDict[entry]))
    return listOfEscapees


def writeToCSV(activeDir, listOfPrey):
    todaysDate = datetime.datetime.now().strftime('%Y-%m-%d')
    fileName = "%s.csv" % todaysDate
    number = 2
    while os.path.isfile(os.path.join(activeDir, fileName)):
        fileName = "%s-%s.csv" % (todaysDate, number)
        number = number + 1

    if not os.path.exists(activeDir):
        os.makedirs(activeDir)
    with open(os.path.join(activeDir, fileName), 'w', newline="") as file:
        filewriter = csv.writer(file, delimiter=',')
        for list in listOfPrey:
            for entry in list:
                filewriter.writerow([entry[0], entry[1]])
        file.close()

    return os.path.join(activeDir, fileName)
