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

def getSheetNames(service,SAMPLE_SPREADSHEET_ID):
    sheet = service.spreadsheets()
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    names = []
    for i in sheets:
        names.append(i.get("properties", {}).get("title", 0))
    return names


def getRange(service,SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME ):
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def getIDsFromAllSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service, VERB=True):

    
    col_simulator_filename = {}
    col_mvm_filename={}
    col_campaign = {}
    dict_ids = {}

    sheet_names = getSheetNames(service,SAMPLE_SPREADSHEET_ID)
 
    
    for s in sheet_names:
        SAMPLE_RANGE_NAME = s+Suffix_SAMPLE_RANGE_NAME
        if (VERB==True):
            print ("----------Studying SHEET", s)
        values = getRange(service,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME )
    
        if not values:
            if (VERB==True):
                print('No data found in Sheet, skipping ....',s)
            continue
        num=0
        headers = []
        col_simulator_filename[s]=-1
        col_mvm_filename[s]=-1
        col_campaign[s]=-1
        dict_id = {}
        for row in range(0,len(values)):
            num=num+1
            if num <= 2 :
                #this is the ISO requirement line, it MUST be here
                continue
            if num ==3 :
                for col in range(0,len(values[row])):
                    if values[row][col]  == "":
                        continue
                    headers.append(values[row][col])
                    if values[row][col] == "simulator_filename":
                        col_simulator_filename[s] = col
                    if values[row][col] == "MVM_filename":
                        col_mvm_filename[s] = col
                    if values[row][col] == "campaign":
                        col_campaign[s] = col
                continue

#        print (col_simulator_filename[s], col_mvm_filename[s] )
            if col_simulator_filename[s] ==-1 or col_mvm_filename[s]==-1 or col_campaign==-1:
                if (VERB==True):
                    print ("Skipping sheet",s, ", does not contain filename or campaign columns")
                continue

#
# check if all the colums have at least the length       
#
            if (len(values[row])<col_simulator_filename[s] or len(values[row])<col_mvm_filename[s] or len(values[row])<col_campaign[s] ):
               if (VERB==True):
                 print ("ROW malformed (too short)")
               continue
            if (values[row][col_simulator_filename[s]]== "" or values[row][col_mvm_filename[s]]==""):
                if (VERB==True):
                    print('%s %s %s' % ("* ID ", s, values[row][0]))
                    dict_id[values[row][0]] =(row,False)
            else:
                if (VERB==True):
                    print('%s %s %s' % ("ID",s, values[row][0]))
                dict_id[values[row][0]] =(row,True)
        dict_ids[s]=dict_id
    
    return (dict_ids,col_simulator_filename,col_mvm_filename,col_campaign)


#
# dict_ids is a map containing campaign, and then pairs of (id,filled) ... filled == True means there is already a filename
#
