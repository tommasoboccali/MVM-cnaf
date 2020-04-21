#!/usr/bin/env python3

import os

print ("Content-type: text/html\n\n")
print (" ")
print (" ")

for param in os.environ.keys():
    print ("%20s %s <br>" % (param,os.environ[param]))

