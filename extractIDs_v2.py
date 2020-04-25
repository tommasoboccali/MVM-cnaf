from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
from gsheet_actions_v2 import *

def main():

    VERB=False
    
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1AQXgqCKNAuCCDGffi9QU_v_9tOP97qYQNyxx9L6pWRA'
    Suffix_SAMPLE_RANGE_NAME = '!A:AZ'

    
    service  = initGsheet(SAMPLE_SPREADSHEET_ID)
    db_s = getDBsFromMultipleSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service,VERB=VERB)
##    if VERB==True:
#        print ("DB",db_s)
    mydict = dbToDict(db_s, VERB)
    if VERB==True:
        print ("================================DICT",mydict)
    (opF, opU) = getIDsForm(mydict, VERB=VERB)

    print(" FILLED", opF)
    print (" ")
    print (" ")
    print (" ")
    print (" ")
    print(" UNFILD", opU)

#    print(mydict)


if __name__ == '__main__':
    main()
#
# prints IDs, and prepend with a * if the filenames are emty (at least one)
#
