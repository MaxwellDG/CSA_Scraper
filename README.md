# CSA_Scraper
A scraper of the Canadian Securities Administrators registry.

## Description
The CSA website has several blocks against traditional methods of scraping, so the term 'scraper' is used in a liberal sense. Ignoring semantics, the primary function of the program is to track administrators' registry status overtime. The client can utilize the software to retrieve data-packets (.har files) of 1 specified security at at time. The packet contains a list of every current registered administrator in the security of choice. On a future date of their choosing, the aforementioned security may be scraped again. Now, the two packets may be compared and the differences will showcase the administrators that have unregistered from their institution. A .csv is generated and the names of these administrators are written into the file for easy organization and record-keeping.

## Demo

### Main User Interface

![Main_Interface_Photo](https://github.com/MaxwellDG/CSA_Scraper/blob/master/CSA-Photo1.png?raw=true)

### DevTools Example

The DevTools Network Tab that users will be prompted to navigate to. This is done by the user because the Selenium bot will need to pause for 'Preserve Logs' to be 
manually toggled.

![DevTools_Photo](https://github.com/MaxwellDG/CSA_Scraper/blob/master/CSA-Photo2.png?raw=true)

### Output

An example of a generated .csv file after comparison.

![Output_Photo](https://github.com/MaxwellDG/CSA_Scraper/blob/master/CSA-Photo3.png?raw=true)

A generated .csv file after selecting 'Generate Names' will look very similar; typically with thousands more rows.






### * Important if you want to use this software *
This software was created for a client, but there is no copyright protection if you would also like to have it.
Still, I left out some parts from the GitHub version that you will need to add yourself.

- You must use a VPN to avoid lockouts
- If lockouts persist after excess usage, there is a BrowserMob-Proxy file that can be uncommented
- You must install the appropriate webdriver for your browser and add it to your PATH. Here's a handout for you if you're using Chrome: https://chromedriver.chromium.org/downloads

Alternatively you can email me directly at maxwellmdg@gmail.com and I can send you a functioning .exe appropriate for your system.

