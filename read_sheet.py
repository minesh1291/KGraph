from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from pprint import pprint
import pandas as pd

from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "../../keys/my-kaggle-competitions-sserve-sheet.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)


# If modifying these scopes, delete the file token.json.

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1WETLYrP2ZT4zrir27GWLidS-L4hQC-6hlMwPN3I0q6E"
SAMPLE_RANGE_NAME = "JD Skills!A1:B500"


def read_sheet():
    service = build("sheets", "v4", credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )

    values = result.get("values", [])
    data_df = pd.DataFrame(values[1:], columns=values[0])
    pprint(data_df)
    data_df.dropna().to_csv("data_df.csv")

def main():
    read_sheet()


if __name__ == "__main__":
    main()
