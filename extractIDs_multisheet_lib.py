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
    sheet_names = getSheetNames(service,SAMPLE_SPREADSHEET_ID)

    col_simulator_filename = {}
    col_mvm_filename={}
    dict_id = {}

    
    for s in sheet_names:
        SAMPLE_RANGE_NAME = s+Suffix_SAMPLE_RANGE_NAME
        print ("----------Studying SHEET", s)
        values = getRange(service,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME )
    
        if not values:
            print('No data found.')
            continue
        num=0
        headers = []
        col_simulator_filename[s]=-1
        col_mvm_filename[s]=-1
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
                        col_simulator_filename[s] = col
                    if values[row][col] == "MVM_filename":
                        col_mvm_filename[s] = col
                    continue


#        print (col_simulator_filename[s], col_mvm_filename[s] )
            if col_simulator_filename[s] ==-1 or col_mvm_filename[s]==-1:
                print ("BSkipping sheet",s)
                continue

#
# check if all the colums have at least the length       
#
            if (len(values[row])<col_simulator_filename[s] or len(values[row])<col_mvm_filename[s]  ):
               print ("ROW malformed (too short)")
               continue
            if (values[row][col_simulator_filename[s]]== "" or values[row][col_mvm_filename[s]]==""):
                   print('%s %s %s' % ("* ID ", s, values[row][0]))
            else:
                   print('%s %s %s' % ("ID",s, values[row][0]))
                   dict_id[values[row][0]] =row 
        dict_ids[s]=dict_id
    
    
if __name__ == '__main__':
    main()
#
# prints IDs, and prepend with a * if the filenames are emty (at least one)
#
