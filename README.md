# webscraper

python scripts for scraping websites

command to run on command line to open browser

1. Run this command from the command line
   Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"
2. Navigate to: https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&app_token=16477aee05006f11833e9af2ea072e3e60970a8428a540ca7f0c468fa48786bf
3. Filter on Cases
4. Run frtom command line: python scraper.py
5. Review results in csv files created for each table in the page
