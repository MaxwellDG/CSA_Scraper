from bs4 import BeautifulSoup
import re
import pprint
import os
import json
from tkinter import messagebox
import datetime
import csv


def parse(activeFile, activeDir):
    finalList = []
    workingFile = os.path.join(activeDir, activeFile)
    with open(workingFile, encoding="utf8") as f:
        data = json.load(f) # deserialize file
        for entry in data['log']['entries']:
            memberListSerialized = entry['response']['content']['text']
            memberListDeSerialized = json.loads(memberListSerialized) # an extra deserialize for the mega long string data
            parsedMembers = memberListDeSerialized['d']['data']
            finalList.extend(parsedMembers)
    print('Length of final list:', len(finalList))
    return finalList


def makeGarbageIntoJSON(data):
    str = data.replace("\'", "\"")
    p = re.compile('(?<!\\\\)\'')
    return p.sub('\"', str)


def isComparisonOfSameSecurity(oldFile, recentFile, activeDir):
    firmNames = []

    for file in [oldFile, recentFile]:
        workingFile = os.path.join(activeDir, file)
        with open(workingFile, encoding="utf8") as f:
            data = json.load(f) # deserialize file
            firstPart = data['log']['entries'][0]
            serializedString = firstPart['request']['postData']['text']
            keepGoing = makeGarbageIntoJSON(serializedString)
            dontStop = json.loads(keepGoing)
            searchURL = dontStop['nrsModel']['SearchUrl']
            firmNames.append(searchURL)
    return firmNames[0] == firmNames[1]
           

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
        for entry in listOfPrey:
            filewriter.writerow([entry['IndivName'], entry['FirmName'], '\'' + str(entry['IndivId'])])
        file.close()

    return os.path.join(activeDir, fileName)
