from tkinter import *
import tkinter.messagebox as tkMessageBox
from tkinter import filedialog as fileDialog
import os
from configparser import ConfigParser
import parserr
from index import securities


class TkUI:
    CONFIG_SECTION = 'main'
    CONFIG_KEY = 'saveDir'

    def __init__(self, advancedScraper):
        self.root = Tk()
        self.securities = securities
        self.scraper = advancedScraper
        self.config = ConfigParser()
        self.entryBox = None
        self.homeDir = self.getSaveLocation()
        self.isSaveLocation = False
        self.saveButton = None


    def getSaveLocation(self):
        if self.config.read('config.ini'): # check if this file exists
            self.isSaveLocation = True
            return self.config.get(self.CONFIG_SECTION, self.CONFIG_KEY)
        else:
            self.isSaveLocation = False
            return os.path.expanduser('~')

    def onListSelect(self, event):
        w = event.widget
        value = ""
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
        except IndexError:
            None
        if self.entryBox is not None:
            self.entryBox.delete(0, END)
            self.entryBox.insert(0, value)

    def minimizeTKWindow(self):
        try:
            self.root.wm_state('iconic')
        except:
            None

    def changeSaveDir(self):
        self.homeDir = fileDialog.askdirectory()

        if not self.config.read('config.ini'):
            self.config.add_section(self.CONFIG_SECTION)
            self.config.set(self.CONFIG_SECTION, self.CONFIG_KEY, self.homeDir)

        with open('config.ini', 'w') as f:
            self.config.write(f)
        
        self.changeSaveButtonStyle(False)

    def alertDialogForManualClick(self, title, message, location=None):
        if type(message) == str:
            return tkMessageBox.askokcancel(title=title, message=message)
        else:
            totalSize = len(message)
            dialogResponse = tkMessageBox.askokcancel(title=title, message="There are %d heads to hunt \n\n"
                                                                           "Find them at: %s" % (totalSize, location))
        return dialogResponse

    def addFileToList(self, listBox):
        fileName = fileDialog.askopenfilename()
        if fileName:
            listBox.insert(listBox.size(), os.path.basename(fileName))

    def checkForEqualRows(self, leftBox, rightBox):
        return leftBox.size() == rightBox.size()

    def compareFiles(self, listBoxBotLeft, listBoxBotRight):
        if self.checkForEqualRows(listBoxBotLeft, listBoxBotRight):
            oldFiles = listBoxBotLeft.get(0, (listBoxBotLeft.size() - 1))
            recentFiles = listBoxBotRight.get(0, (listBoxBotRight.size() - 1))

            for i in range(len(oldFiles)):
                oldFileParsed = parserr.parse(oldFiles[i], self.homeDir)
                recentFileParsed = parserr.parse(recentFiles[i], self.homeDir)
                if parserr.isComparisonOfSameSecurity(oldFiles[i], recentFiles[i], self.homeDir):
                    listOfPrey = parserr.compareDicts(oldFileParsed, recentFileParsed)

                    self.refreshFields([listBoxBotRight, listBoxBotLeft])
                    subDirFolder = os.path.join(self.homeDir, "Comparisons-CSV")
                    # this is horrible form but I'm tired. The method below returns file location but also does a bunch of other stuff
                    location = parserr.writeToCSV(subDirFolder, listOfPrey)
                    self.alertDialogForManualClick("Results: ", listOfPrey, location)
                else:
                    self.alertDialogForManualClick("Matching Error", "Security of row %s does not match.\n"
                                                                     "This row will be removed from final analysis." % (
                                                       i))

        else:
            self.alertDialogForManualClick("Indexing Error", "ListBoxes must have equal number of entries.\n"
                                                             "- Remember that each comparison must be of the same "
                                                             "security type.")

    def refreshFields(self, fields):
        for field in fields:
            field.delete(0, END)

    def changeSaveButtonStyle(self, isAddingColor):
        if isAddingColor:
            self.saveButton.configure(fg='red')
        else:
            self.saveButton.configure(fg="black")
        self.saveButton.pack()

    def generateListOfNames(self, fileNames):
        finalList = []
        for file in fileNames:
            finalList.extend(parserr.parse(file, self.homeDir))
        subDirFolder = os.path.join(self.homeDir, "Names-CSV")
        location = parserr.writeToCSV(subDirFolder, finalList)
        self.alertDialogForManualClick("Results: ", finalList, location)


    def initWidgets(self):
        self.root.title("CSA Registry")

        canvas = Canvas(self.root)
        canvas.pack()

        # Framing
        labelFrame = LabelFrame(canvas, text="CSA Registry", padx=5, pady=5, font=('Helvetica', 14, 'bold'))
        labelFrame.pack(padx=10, pady=10)
        labelFrameTippyTop = LabelFrame(canvas, text="Utilities", font=('Helvetica', 12, 'bold'))
        labelFrameTippyTop.pack(side=TOP, padx=20, pady=20, expand=YES, fill=BOTH)
        labelFrameTop = LabelFrame(canvas, text="Botting and .har Export", font=('Helvetica', 12, 'bold'))
        labelFrameTop.pack(side=LEFT, padx=20, pady=20, expand=True)
        labelFrameBot = LabelFrame(canvas, text="Parsing and Differentiation", font=('Helvetica', 12, 'bold'))
        labelFrameBot.pack(side=RIGHT, padx=20, pady=20)
        frameTop = Frame(labelFrameTop)
        frameTop.pack(side=TOP)
        frameBot = Frame(labelFrameBot)
        frameBot.pack(side=BOTTOM)

        canvas.create_window((0,0), window=labelFrame, anchor='nw')

        # Top half widgets
        entry = Entry(frameTop, width=self.securities[0].__len__() + 10)
        entry.pack(side=RIGHT, padx=10, pady=10)
        self.entryBox = entry

        listBox = Listbox(frameTop,
                          height=(self.securities.__len__()),
                          width=(self.securities[5].__len__() + 5),
                          selectmode=SINGLE,
                          name='listBox')
        for i in range(self.securities.__len__()):
            listBox.insert(int(i), self.securities[i])
        listBox.bind('<<ListboxSelect>>', self.onListSelect)
        listBox.pack(side=LEFT, padx=10, pady=10)

        buttonTopStart = Button(labelFrameTop, text="Start",
                                command=lambda: self.scraper.getSecurityForSearch(entry.get(), listBox.curselection()))
        buttonTopStart.pack(side=BOTTOM, padx=10, pady=10)

        # Bottom half widgets
        listBoxBotLeft = Listbox(frameBot, height=10, width=40)
        listBoxBotLeft.pack(side=LEFT, expand=YES, fill=BOTH, padx=10, pady=10)

        listBoxBotRight = Listbox(frameBot, height=10, width=40)
        listBoxBotRight.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10, pady=10)

        buttonBotAddLeft = Button(labelFrameBot, text="Add old file",
                                  command=lambda: self.addFileToList(listBoxBotLeft))
        buttonBotAddLeft.pack(side=LEFT, padx=10, pady=10)
        buttonBotAddRight = Button(labelFrameBot, text="Add new file",
                                   command=lambda: self.addFileToList(listBoxBotRight))
        buttonBotAddRight.pack(side=RIGHT, padx=10, pady=10)
        buttonCompare = Button(labelFrameBot, text="Compare",
                               command=lambda: self.compareFiles(listBoxBotLeft, listBoxBotRight))
        buttonCompare.pack(side=BOTTOM, padx=10, pady=10)
        buttonLongList = Button(labelFrameBot, text="Generate Names",
                                command=lambda: self.generateListOfNames(listBoxBotLeft.get(0, END)))
        buttonLongList.pack(side=TOP, padx=10, pady=10)

        # Very top widgets
        saveLocationButton = Button(labelFrameTippyTop, text="Set Save Location", command=lambda: self.changeSaveDir())
        saveLocationButton.pack(side=LEFT, padx=10, pady=10)
        self.saveButton = saveLocationButton
        if not self.config.read('config.ini'):
            self.changeSaveButtonStyle(True)

        refreshButton = Button(labelFrameTippyTop, text="Clear Fields",
                               command=lambda: self.refreshFields([listBoxBotRight, listBoxBotLeft, entry]))
        refreshButton.pack(side=LEFT, padx=10, pady=10)
        helpButton = Button(labelFrameTippyTop, text="Information",
                            command=lambda: self.alertDialogForManualClick("Information:",
                                                                           "Botting and .har Export:\n\n"
                                                                           "- Select or enter a security name\n"
                                                                           "- A browser window will open and a bot "
                                                                           "will automatically navigate to the "
                                                                           "website. DO NOT click on the website "
                                                                           "unless specified to do so\n "
                                                                           "- Follow the instructions from popup "
                                                                           "alerts\n "
                                                                           "- The final product will be a single file "
                                                                           "with that security's encrypted "
                                                                           "information\n\n "
                                                                           "Parsing and Differentiation:\n\n"
                                                                           "- Click \"Add old file\" and select a "
                                                                           ".har file\n "
                                                                           "- Click \"Add new file\" and select a "
                                                                           "more recent .har file OF THE SAME "
                                                                           "SECURITY\n "
                                                                           "- Continue to add as many pairs as you'd "
                                                                           "like\n "
                                                                           "- Click compare when you are ready\n"
                                                                           "- The popup will only state the names of "
                                                                           "people who have left their company (it "
                                                                           "will not include new additions)\n "
                                                                           "- The above information will be written "
                                                                           "to a newly created .csv file and saved in "
                                                                           "a sub-directory named \"Results-CSV\"\n "
                                                                           "- Happy hunting"))
        helpButton.pack(side=RIGHT, padx=10, pady=10)

        # Start rendering loop
        self.root.mainloop()
