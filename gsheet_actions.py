from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

# If modifying these scopes, delete the file token.pickle.

# The ID and range of a sample spreadsheet.



def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def insert_single_cell(row, column, text, service,SAMPLE_SPREADSHEET_ID ):

    colnum_str = colnum_string(column+1)
    row_insert = row+1
    body = {'values': [[text]]}
    range_insert = '20200412 ISO!'+colnum_str+str(row_insert)+":"+colnum_str+str(row_insert)

    print ("Inserting ",text , " in rage", range_insert )
    
    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=range_insert,
        valueInputOption="RAW",
        body=body).execute()

def initGsheet(SAMPLE_SPREADSHEET_ID):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    return service


def getRange(service,SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME ):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values



