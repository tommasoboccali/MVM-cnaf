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
    Suffix_SAMPLE_RANGE_NAME = '!A:AR'

    service  = initGsheet(SAMPLE_SPREADSHEET_ID)
    (dict_ids,col_simulator_filename,col_mvm_filename,col_campaign) = getIDsFromAllSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service, VERB=True)
    print (dict_ids)
        
if __name__ == '__main__':
    main()
#
# prints IDs, and prepend with a * if the filenames are emty (at least one)
#
