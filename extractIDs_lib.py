from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
from gsheet_actions import *


def main():

    
    # The ID and range of a sample spreadsheet.
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
                for col in range(0,len(values[row])):
                    if values[row][col]  == "":
                        continue
                    headers.append(values[row][col])
                    if values[row][col] == "simulator_filename":
                        col_simulator_filename = col
                    if values[row][col] == "MVM_filename":
                        col_mvm_filename = col
            # Print columns A and E, which correspond to indices 0 and 4.
                continue
            if col_simulator_filename ==-1 or col_mvm_filename==-1:
                print ("ERROR: could not find filename columns", col_simulator_filename,col_mvm_filename)
#            print('%s %s %s %s' % ("ID", row[0], row[col_simulator_filename], row[col_mvm_filename]))
                sys.exit(1)
            if (values[row][col_simulator_filename]== "" or values[row][col_mvm_filename]==""):
                print('%s %s' % ("* ID", values[row][0]))
            else:
                print('%s %s' % ("ID", values[row][0]))
            dict_ids[values[row][0]] =row 
    
if __name__ == '__main__':
    main()
#
# prints IDs, and prepend with a * if the filenames are emty (at least one)
#
