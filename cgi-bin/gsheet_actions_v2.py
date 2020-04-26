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

def insert_single_cell(row, column, text, service, sheet, SAMPLE_SPREADSHEET_ID, VERB=False ):

    colnum_str = colnum_string(column+1)
    row_insert = row+1
    body = {'values': [[text]]}
    range_insert = sheet+'!'+colnum_str+str(row_insert)+":"+colnum_str+str(row_insert)

    if VERB==True:
        print ("Inserting ",text , " in rage", range_insert )
    
    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=range_insert,
        valueInputOption="RAW",
        body=body).execute()
    return (result['updatedCells'] == 1)

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

def malformedHeader(header):
    # need to have MVM_filename, simulator_filename, campaign, N
    if 'N' not in header or 'campaign'  not in header or 'MVM_filename'  not in header or 'simulator_filename'  not in header:
        return True
    return False

def malformedRow(row, VERB=False):
    #
    # request #1: there must be an Id
    #
    if 'N' not in row.keys():
        if VERB==True:
            print ("No N (testID) value in the header")
        return True
    if row['N'][0] == "":
        if VERB==True:
            print ("No N (testID) value for the row")
        return True
    # request #2: I want campaign
    if 'campaign' not in row.keys():
        if VERB==True:
            print ("No campaign value in the header")
        return True
    if row['campaign'][0] == "":
        if VERB==True:
            print ("No campaign value for the row")
        return True
    return False


def getDBFromSheet(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service, sheet_name, VERB=False):
    db = {}
    s = sheet_name
    SAMPLE_RANGE_NAME = s+Suffix_SAMPLE_RANGE_NAME
    if (VERB==True):
            print ("----------Studying SHEET", s)
    values = getRange(service,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME )
    if not values:
            if (VERB==True):
                print('No data found in Sheet, skipping ....',s)
                return (None)
    header=[]
    num=0
    for row in range(0,len(values)):
            num=num+1
            if num <= 2 :
                #this is the ISO requirement line, it MUST be here
                continue
            if num ==3 :
# this is the header
                for col in range(0,len(values[row])):
                    header.append(values[row][col])
                continue
            if malformedHeader(header)== True:
                if (VERB==True):
                        print ("Malformed header, not considering sheet", s)
                return None
            if values[row][0]  == "":
                if (VERB==True):
                        print ("Skipping empty line")
                continue
            db[row]={}
            for i in range(0,len(header)):
                if (i<len(values[row])):
                    db[row][header[i]]= (values[row][i],row,i)
                else:
                    db[row][header[i]]=("",row,i)
            
    return db

def dbToDict(db, VERB=False):
    mydict = {}
    for site in db.keys():
       mydict[site]={}
       for krow in db[site].keys():
           # check if row is ok
#            print ("ROW",krow,db[site][krow])
            if malformedRow(db[site][krow]) == True:
                if VERB==True:
                    print ("Malformed Row", malformedRow(db[site][krow]) )
                continue
            valrow = db[site][krow]
#this is the loop over lines 1,2,3,4,5.... in the table
#            print (site,krow,valrow)
            campaign = valrow['campaign']
#            print ("------------------ campaign",campaign,campaign[0])
            if campaign[0] not in mydict[site]:
               mydict[site][campaign[0]] = {}
            id = valrow['N'][0]
#            print ("AAAAAAAAAAAAAAA",id, valrow['N'])
            if id not in mydict[site][campaign[0]]:
               mydict[site][campaign[0]][id] = {}
            mydict[site][campaign[0]][id]  = (db[site][krow])
    return mydict
            

def getDBsFromMultipleSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service,VERB=False):

    sheet_names = getSheetNames(service,SAMPLE_SPREADSHEET_ID)

    db_s = {}
    for s in sheet_names:
        if s == "ISO 80601-2-80 requirements":
            continue
        if (VERB==True):
            print ("----------Studyng SHEET", s)
        (db)= getDBFromSheet(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service, s, VERB)
        if db is None:
            if (VERB==True):
                print ("Skipping SHEET", s, "since it is malformed")
            continue
        db_s[s] = db
            
    return (db_s)

def getIDsForm(mydict, VERB=True):
    
    # I need to define options as a map
    optionmapUNFILLED = {}
    optionmapFILLED = {}
    for site in mydict.keys():
        if (VERB==True):
            print ("Key ",site)
            print (mydict[site].values())

        for campaign in mydict[site].keys():
           for id in mydict[site][campaign].keys():
              if mydict[site][campaign][id]['MVM_filename'][0] == "" and mydict[site][campaign][id]['simulator_filename'][0] == "":
                 # to be put in UNFILLED
                 if site not in optionmapUNFILLED.keys():
                     optionmapUNFILLED[site] = {}
                 if campaign not in optionmapUNFILLED[site].keys():
                     optionmapUNFILLED[site][campaign] = []
                 optionmapUNFILLED[site][campaign].append(id)
              else:
                 if site not in optionmapFILLED.keys():
                     optionmapFILLED[site] = {}
                 if campaign not in optionmapFILLED[site].keys():
                     optionmapFILLED[site][campaign] = []
                 optionmapFILLED[site][campaign].append(id)
    return (optionmapFILLED,optionmapUNFILLED)

