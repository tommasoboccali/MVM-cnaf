from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
from gsheet_actions_newtemplate import *

def main():

    
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1AQXgqCKNAuCCDGffi9QU_v_9tOP97qYQNyxx9L6pWRA'
    Suffix_SAMPLE_RANGE_NAME = '!A:AZ'

    
    service  = initGsheet(SAMPLE_SPREADSHEET_ID)
    (dict_ids,col_simulator_filenames,col_mvm_filenames,col_campaigns, all_s) = getIDsFromMultipleSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service,VERB=False)

    (optionmap, opF, opU) = getIDsForm(dict_ids, VERB=False)

    print(" GLOBAL", optionmap)
    print(" FILLED", opF)
    print(" UNFILD", opU)


    
    #(dict_ids,col_simulator_filenames,col_mvm_filenames,col_campaigns,all_s) = getIDsFromMultipleSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service, VERB=True)
    #print (dict_ids)
    #print(all_s)
if __name__ == '__main__':
    main()
#
# prints IDs, and prepend with a * if the filenames are emty (at least one)
#
