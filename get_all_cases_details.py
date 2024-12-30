import pandas as pd
from get_case_details import get_case_details


def update_case_details(file_name, output_file, num_rows=None):
    """
    Updates the case details in the DataFrame and saves the updated DataFrame to a CSV file.

    Args:
        file_name (str): The name of the input CSV file.
        output_file (str): The name of the output CSV file.
        num_rows (int, optional): The number of rows to process. If None, process all rows.
    """
    cases = pd.read_csv(file_name)

    # Iterate through rows using iterrows()
    for index, row in cases.head(num_rows).iterrows():
        case_no = row["case_no"]
        cino = row["cino"]
        app_token = row["app_token"]

        payload = {
            "court_code": 7,
            "state_code": 16,
            "dist_code": 3,
            "court_complex_code": 1160009,
            "case_no": case_no,
            "cino": cino,
            "hideparty": "",
            "search_flag": "CScaseNumber",
            "search_by": "CSact",
            "ajax_req": True,
            "app_token": app_token,
        }

        next_hearing_date, case_stage, court_number = get_case_details(payload)

        cases.at[index, "next_hearing_date"] = next_hearing_date
        cases.at[index, "case_stage"] = case_stage
        cases.at[index, "court_number"] = court_number

    # Save the updated DataFrame back to a CSV file
    cases.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Example usage
    update_case_details("table-1.csv", "case_details1.csv", num_rows=5)
