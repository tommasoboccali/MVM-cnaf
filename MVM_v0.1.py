from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1MlOhG-UhXlK3htq4FqL0nN0yrl0ubAj0jRHXY4Ki6ro'
SAMPLE_RANGE_NAME = '20200412 ISO!A:AR'




def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def insert_single_cell(row, column, text, service):

    colnum_str = colnum_string(column+1)
    row_insert = row+1
    body = {'values': [[text]]}
    range_insert = '20200412 ISO!'+colnum_str+str(row_insert)+":"+colnum_str+str(row_insert)

    print ("Inserting ",text , " in rage", range_insert )
    
    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=range_insert,
        valueInputOption="RAW",
        body=body).execute()




def main():
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
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
#    print (values)

    if not values:
        print('No data found.')
    else:
        num=0
        headers = []
        col_simulator_filename=-1
        col_mvm_filename=-1
        dict_ids = {}
        for row in range(0,len(values)):
            num=num+1
            if num <= 2 :
                #this is the ISO requirement line
                continue
            if num ==3 :
                print ("header line")
                for col in range(0,len(values[row])):
                    if values[row][col]  == "":
                        continue
                    headers.append(values[row][col])
                    if values[row][col] == "simulator_filename":
                        col_simulator_filename = col
                    if values[row][col] == "MVM_filename":
                        col_mvm_filename = col
                print ("Columns are",headers)
                print ("Column for simulator_filename is ", col_simulator_filename)
                print ("Column for mvm_filename is ", col_mvm_filename)
            # Print columns A and E, which correspond to indices 0 and 4.
                continue
            if col_simulator_filename ==-1 or col_mvm_filename==-1:
                print ("ERROR: could not find filename columns", col_simulator_filename,col_mvm_filename)
#            print('%s %s %s %s' % ("ID", row[0], row[col_simulator_filename], row[col_mvm_filename]))

            if (values[row][col_simulator_filename]== "" or values[row][col_mvm_filename]==""):
                print('%s %s %s' % ("ID", values[row][0], " AVAILABLE FOR INSERTION"))
            else:
                print('%s %s %s' % ("ID", values[row][0], " has proper files"))
            dict_ids[values[row][0]] =row 

    # write PIPPO in cel in row 7
#    values[7][0]= "pippo"
#    sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")
#    print (sheet)
#    help(sheet)
#    values = [['Pippo']]
    #    body = {'values': values}
#    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#        range='20200412 ISO!A7:A7',
#        valueInputOption="RAW",
#        body=body).execute()



                #
                # try and insert file names in ID 120
                #

        # here
        simulator_test_name = "pippo"
        mvm_test_name = "pluto"
        id = "120"
        insert_single_cell(dict_ids[id], col_simulator_filename,simulator_test_name, service )
        insert_single_cell(dict_ids[id], col_mvm_filename,mvm_test_name, service )
        
    
if __name__ == '__main__':
    main()
