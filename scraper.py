import re
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def GetDriver(debugger_address="127.0.0.1:9222"):
    """Initialize and return a Selenium WebDriver instance."""
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", debugger_address)
        chrome_driver = "/opt/homebrew/bin/chromedriver"
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        return None


def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    headers.extend(["case_no", "cino", "app_token"])
    logging.info(f"[+] Found headers: {headers}")
    return headers


def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    # print every row in the table
    # rows = table.find_all("tr")[2:4]
    # for tr in rows:
    #     print(str(tr))
    for tr in table.find_all("tr")[2:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
            cells.extend(["case_no", "cino", "app_token"])
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
                a_tag = td.find("a")
                if a_tag:
                    # Perform some action if <a> tag is found
                    a_href = a_tag["href"]
                    app_token = re.search(r"app_token=(\w+)", a_href).group(1)

                    a_onclick = a_tag["onclick"]
                    case_no = re.search(r"viewHistory\((\d+)", a_onclick).group(1)
                    cino = re.search(r"viewHistory\(\d+,'(\w+)", a_onclick).group(1)
                    cells.extend([case_no, cino, app_token])

        rows.append(cells)
    return rows


def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")


def main():
    driver = GetDriver()
    if not driver:
        return

    try:
        # Execute Main Logic
        table_of_cases = driver.find_element(By.XPATH, "//*[@id='dispTable']")
        table_of_cases_html = table_of_cases.get_attribute("outerHTML")
        soup = BeautifulSoup(table_of_cases_html, "html.parser")

        # extract all the tables from the web page
        tables = get_all_tables(soup)
        logging.info(f"[+] Found a total of {len(tables)} tables.")

        # iterate over all tables
        for i, table in enumerate(tables, start=1):
            # get the table headers
            headers = get_table_headers(table)
            # get all the rows of the table
            rows = get_table_rows(table)
            # save table as csv file
            table_name = f"table-{i}"
            print(f"[+] Saving {table_name}")
            save_as_csv(table_name, headers, rows)
    except Exception as e:
        logging.error(f"Error executing main logic: {e}")
        return None


if __name__ == "__main__":
    main()
