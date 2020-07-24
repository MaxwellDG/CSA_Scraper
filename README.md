# CSA_Scraper
A scraper for the Canadian Securities Administrators registry.

## Description
The CSA website had several blocks against traditional methods of scraping, so the term 'scraper' is used in a liberal sense. Ignoring semantics, the primary function of the program is to track administrators' registry status overtime. The client can utilize the software to retrieve data-packets (.har files) of 1 specified security at at time. The packet contains a list of every current registered administrator in the security of choice. On a future date of their choosing, the aforementioned security may be scraped again. Now, the two packets may be compared and the differences will showcase the administrators that have unregistered from their institution. A .csv is generated and the names of these administrators are fed into the file for easy organization and record-keeping.



