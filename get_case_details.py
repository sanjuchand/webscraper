import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def get_case_details(payload):
    """
    Sends a POST request with the given payload and extracts the next hearing date,
    case stage, and court number from the response.

    Args:
        payload (dict): The form data to be sent in the POST request.

    Returns:
        tuple: A tuple containing the next hearing date, case stage, and court number.
    """
    # Define the target URL
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=home/viewHistory"

    # Send the POST request
    response = requests.post(url, data=payload)

    # Check the response
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr")

        pattern = r"([^<]+)"

        # Extract the next hearing date from the appropriate cell
        next_hearing_date = None
        if len(rows) > 5:
            cell = rows[5].find_all("td")[1].get_text(strip=True)
            next_hearing_date = re.search(pattern, cell).group(1)

        # Extract the case stage from the appropriate cell
        case_stage = None
        if len(rows) > 6:
            cell = rows[6].find_all("td")[1].get_text(strip=True)
            case_stage = re.search(pattern, cell).group(1)

        # Extract the court number from the appropriate cell
        court_number = None
        if len(rows) > 7:
            cell = rows[7].find_all("td")[1].get_text(strip=True)
            court_number = re.search(pattern, cell).group(1)

        return next_hearing_date, case_stage, court_number
    else:
        print(f"Failed with status code: {response.status_code}")
        print("Response Content:", response.text)
        return None, None, None


if __name__ == "__main__":

    payload = {
        "court_code": 7,
        "state_code": 16,
        "dist_code": 3,
        "court_complex_code": 1160009,
        "case_no": 200100098902020,
        "cino": "WBCS020368342020",
        "hideparty": "",
        "search_flag": "CScaseNumber",
        "search_by": "CSact",
        "ajax_req": True,
        "app_token": "244e7b75cbe51f6ba9d3d4c6b8d3069a22e8ab6a561b65bd8eb94e6aaf2b40ec",
    }

    next_hearing_date, case_stage, court_number = get_case_details(payload)
    print("Next Hearing Date:", next_hearing_date)
    print("Case Stage:", case_stage)
    print("Court Number:", court_number)
