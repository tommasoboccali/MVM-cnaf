# MVM-cnaf
we moved to pytho3
you need to do once

pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
     
     
again only once you have to get credentials.json, by going to 

https://developers.google.com/sheets/api/quickstart/python

and clicking on Enable the Google Sheets API (follow the instructions and then copy the file in the dir)
     
then the first time you run 

python3 extractIDs_lib.py

you will be redirected to a web page where you need to authorize.

then you will see in your dir the files
credentials.json
token.pickle

do NOT commit them! You are ok now!

the Gsheet used for test is

https://docs.google.com/spreadsheets/d/1MlOhG-UhXlK3htq4FqL0nN0yrl0ubAj0jRHXY4Ki6ro/edit

in paticular tab 

20200412 ISO


in cgi-bin you can test by

python3 -m http.server --cgi

and pointing to 

http://localhost:8000/cgi-bin/uploadresults_gsheet

(if you started the server from top level)
