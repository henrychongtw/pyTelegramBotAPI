import time
from datetime import datetime
import csv

# from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES =  ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1Uxu4Akzcx-NfUUFdKQ1_ycQp83pKCSWjaevgGGEbI0c'
SAMPLE_SPREADSHEET_ID = '1kHvTdq4tpuNbrZPP_poO8TNJ_3zVmvxbFKxnQvt4YjA'

SAMPLE_RANGE_NAME = 'Sheet1!A:B'

dict_w = {'a': '1234', 'b': '12341'}
list = [["value1"], ["value2"], ["Value3"]]
resource ={
    "majorDimension": "ROWS",
    "values": list
}

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME, body=resource, valueInputOption="USER_ENTERED").execute()
    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                # range=SAMPLE_RANGE_NAME).execute()
    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    # values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()
