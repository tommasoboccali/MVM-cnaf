from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

from gsheet_actions import *

def main():
    SAMPLE_SPREADSHEET_ID = '1MlOhG-UhXlK3htq4FqL0nN0yrl0ubAj0jRHXY4Ki6ro'
    SAMPLE_RANGE_NAME = '20200412 ISO!A:AR'

    service  = initGsheet(SAMPLE_SPREADSHEET_ID)
    values = getRange(service,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME )

    
    if not values:
        print('No data found.')
        sys.exit(2)
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
#                print ("header line")
                for col in range(0,len(values[row])):
                    if values[row][col]  == "":
                        continue
                    headers.append(values[row][col])
                    if values[row][col] == "simulator_filename":
                        col_simulator_filename = col
                    if values[row][col] == "MVM_filename":
                        col_mvm_filename = col
#                print ("Columns are",headers)
#                print ("Column for simulator_filename is ", col_simulator_filename)
#                print ("Column for mvm_filename is ", col_mvm_filename)
            # Print columns A and E, which correspond to indices 0 and 4.
                continue
            if col_simulator_filename ==-1 or col_mvm_filename==-1:
                print ("ERROR: could not find filename columns", col_simulator_filename,col_mvm_filename)
                sys.exit(1)
#            print('%s %s %s %s' % ("ID", row[0], row[col_simulator_filename], row[col_mvm_filename]))

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
        print ("Writing filenames for ID =",id)

        insert_single_cell(dict_ids[id], col_simulator_filename,simulator_test_name, service, SAMPLE_SPREADSHEET_ID )
        insert_single_cell(dict_ids[id], col_mvm_filename,mvm_test_name, service, SAMPLE_SPREADSHEET_ID )
        
    
if __name__ == '__main__':
    main()
