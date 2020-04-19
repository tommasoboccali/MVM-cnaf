#!/usr/bin/env python3
import cgi, os
import cgitb; cgitb.enable()
import json
import pathlib
import hashlib
 
from datetime import datetime
form = cgi.FieldStorage()

#for gsheet
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import os
import json
from gsheet_actions_newtemplate import *
 
def md5sum(filename):
  return hashlib.md5(open(filename, 'rb').read()).hexdigest()

def printForm(opU,opF):
    form_template_file=open ("../templates/form.html", "r")
    form_template=form_template_file.read()
    print("Content-Type: text/html\n\n")

    options_Site=""
    for i in opU.keys() :
        options_Site+='<option value="%s">%s</option>' %(i,i)
        
    print(form_template.format(options_map=json.dumps(opU),options_Site=options_Site))


def receiveAndSaveToGoogleSheet(dict_ids, col_simulator_filenames, col_mvm_filenames, col_campaigns, col_daqs, col_firmwares, col_comments,service, SAMPLE_SPREADSHEET_ID, all_s,VERB=False):

    CNAF_Prefix ='/storage/data/'
#    CNAF_Prefix='/Users/tom/DBClone/work/MVM/data'
    print("Content-Type: text/html\n\n")
    testID = form.getvalue("TestID")
    site = form.getvalue("Site")
    campaign = form.getvalue("Campaign")
    mvmonlyR = form.getvalue("mvmonly")
    mvmonly = True
    if mvmonlyR:
        mvmonly = True
    else:
        mvmonly = False
    file_DTA = form['file1']
    file_RWA = form['file2']
    file_mvm = form['file3']
    #
    # i issue an error if the first two are different suffix apart
    #
    if (os.path.splitext(file_DTA.filename)[0] != os.path.splitext(file_RWA.filename)[0]):
        print ("ERROR! The two simulator files should have the same name apart from the suffix. I got ",file_simulator.filename, file_simulator_2.filename)
        sys.exit(3)
    filename_simulator_no_suffix = os.path.splitext(file_DTA.filename)[0]

    path_at_CNAF = CNAF_Prefix + '/' + site+ '/'+campaign+ '/'+testID+'/'
#mkdir this path
    try:
      pathlib.Path(path_at_CNAF).mkdir(parents=True, exist_ok=True)
    except:
        print ("===== Creating Directory file ", path_at_CNAF, " failed! Aborting<br>")
        sys.exit(6)

    if mvmonly == False:
        try:
            open(path_at_CNAF+file_DTA.filename, 'wb').write(file_DTA.file.read())
        except:
            print ("===== Saving file ",file_DTA.filename, " to ", path_at_CNAF, " failed! Aborting<br>")
            sys.exit(5)
        try:
            open(path_at_CNAF+file_RWA.filename, 'wb').write(file_RWA.file.read())
        except:
            print ("===== Saving file ",file_RWA.filename, " to ", path_at_CNAF, " failed! Aborting<br>")
            sys.exit(5)

        if os.path.exists(path_at_CNAF+file_DTA.filename) == False or os.path.exists(path_at_CNAF+file_RWA.filename) == False:
            print ("====== FAILED FILE UPLOAD!!!!! NOT COINTINUING <br>")
            sys.exit(4)

    try:
        open(path_at_CNAF+file_mvm.filename, 'wb').write(file_mvm.file.read())
    except:
        print ("===== Saving file ",file_mvm.filename, " to ", path_at_CNAF, " failed! Aborting<br>")
        sys.exit(5)

    if os.path.exists(path_at_CNAF+file_mvm.filename) == False :
        print ("====== FAILED FILE UPLOAD!!!!! NOT COINTINUING <br>")
        sys.exit(4)

#    if file_simulator.filename :
#        open('/dev/null', 'wb').write(file_simulator.file.read()) #FIXME: do something better than writing to dev null
#    if file_mvm.filename :
#        open('/dev/null', 'wb').write(file_mvm.file.read()) #FIXME: do something better than writing to dev null
#    if file_simulator_2xs.filename :
#        open('/dev/null', 'wb').write(file_simulator_2.file.read()) #FIXME: do something better than writing to dev null
    
    print("File Upload was ok<br>")
    #
    # now I fix them in the gsheet
    #
    print("Filling the gsheet", '<br>')
    print ("SITE    = " , site, '<br>')
    print ("CAMPAIGN= " , campaign, '<br>')
    print ("Test ID = " ,testID , '<br>')
    print ("F_DTA   = " , file_DTA.filename, '<br>')
    print ("F_RWA   = " ,file_RWA.filename , '<br>')
    print ("F_MVM   = " ,file_mvm.filename , '<br>')
    print ("MVMONLY = " , mvmonly , '<br>')

#
# now prepare the JSON, starting from all
#
#user: username of the user who did the upload string
#upload_timestamp: timestamp of the upload timestamp string
#campaign string
#testID string
#site string
#MVM_firmware_version string
#DAQ_software_version string
#comment string
#MVM_file: name of the MVM file string
#MVM_file_checksum: MD5 checksum of the MVM file string
#has_simulator: true if MVM_only was not selected at submission time, false otherwise boolean
#simulator_RWA_file string
#simulator_RWA_file_checksum: MD5 checksum of the simulator RWA file string
#simulator_DTA_file string
#simulator_DTA_file_checksum: MD5 checksum of the simulator DTA file string
#path_at_CNAF: path to the dataset at CNAF string
#conditions: filled automatically with column content from the spreadsheet, corresponding to the selected campaign and test
    dict_json= {}
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    dict_json['upload_timestamp'] = timestampStr

    dict_json['user'] = 'webuser'
    dict_json['site'] = site
    dict_json['campaign'] = campaign
    dict_json['testID'] = testID
#!!!!
# get the lines
    rowin_sheet=dict_ids[site][(testID,campaign)][0]
    dict_json['MVM_firmware_version'] =all_s[site][rowin_sheet][col_firmwares[site]]
    dict_json['DAQ_software_version'] = all_s[site][rowin_sheet][col_daqs[site]]
    dict_json['comment']= all_s[site][rowin_sheet][col_comments[site]]
    #
    dict_json['MVM_file']=file_mvm.filename
    dict_json['MVM_file_checksum']=md5sum(path_at_CNAF+file_mvm.filename)
    if (mvmonly == False):
        dict_json['simulator_RWA_file']=file_RWA.filename
        dict_json['simulator_DTA_file']=file_DTA.filename
        dict_json['simulator_RWA_file_checksum']=md5sum(path_at_CNAF+file_RWA.filename)
        dict_json['simulator_DTA_file_checksum']=md5sum(path_at_CNAF+file_DTA.filename)
    
    dict_json['conditions'] = all_s[site][rowin_sheet]
    dict_json['path_at_CNAF'] = path_at_CNAF
    dict_json["has_simulator"] =  1 if mvmonly == False else 0
    # dump to json

#    print (dict_json)
    try:
        with open(path_at_CNAF+'result.json', 'w') as fp:
            json.dump(dict_json, fp)
    except:
        print ("===== Saving file ",'result.json', " to ", path_at_CNAF, " failed! Aborting<br>")
        sys.exit(5)

    if os.path.exists(path_at_CNAF+'result.json') == False :
        print ("====== FAILED JSON UPLOAD!!!!! NOT COINTINUING <br>")
        sys.exit(5)
        
    print("JSON Upload was ok<br>")
    #
    # upload also this
    #

# simulator 1 and 2 ....

#    print ('===================', dict_ids[site][(testID,campaign)][0])   
        
    if (mvmonly==False):
            res = insert_single_cell(dict_ids[site][(testID,campaign)][0], col_simulator_filenames[site],filename_simulator_no_suffix, service,site, SAMPLE_SPREADSHEET_ID, VERB=VERB )
            if res == True:
                print ("XLS Edited with Simulator Filenames!<br>")
            else:
                print ("===== Error updating XLS!<br>")
                sys.exit(6)

# mvm
    res= insert_single_cell(dict_ids[site][(testID,campaign)][0], col_mvm_filenames[site],file_mvm.filename, service, site,  SAMPLE_SPREADSHEET_ID ,VERB=VERB)
    if res == True:
        print ("XLS Edited with MVM Filename!<br>")
    else:
        print ("===== Error updating XLS!<br>")
        sys.exit(6)

def main():
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1AQXgqCKNAuCCDGffi9QU_v_9tOP97qYQNyxx9L6pWRA'
    Suffix_SAMPLE_RANGE_NAME = '!A:AR'
    service  = initGsheet(SAMPLE_SPREADSHEET_ID)

    (dict_ids,col_simulator_filenames,col_mvm_filenames,col_campaigns, col_daqs, col_firmwares, col_comments, all_s) = getIDsFromMultipleSheets(SAMPLE_SPREADSHEET_ID,Suffix_SAMPLE_RANGE_NAME, service,False)

    (optionmap,opF,opU) = getIDsForm(dict_ids, False)


    if "submit" in form.keys():
        receiveAndSaveToGoogleSheet(dict_ids, col_simulator_filenames, col_mvm_filenames, col_campaigns, col_daqs, col_firmwares, col_comments,service, SAMPLE_SPREADSHEET_ID, all_s,False)
    else:
        printForm(opU,opF)

if __name__ == '__main__':
    main()

