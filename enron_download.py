"""
Created on: April 2019
Sasha Prokosheva

Download Enron data mailbox for person = "skilling-j"
"""
import pandas as pd
pd.set_option('display.max_colwidth', 500000)
pd.set_option('precision', 0)
import numpy as np
import re

# To save dictionary to csv
import unicodecsv as csv_unicode
import os
import csv

# To read several files
import glob

# Date
import datetime

##############################################################################################
# Parameters
##############################################################################################
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

path_data = dname + '/data/'
person = "skilling-j"
fields = ["Message-ID: ", "\nDate: ", "\nFrom: ", "\nTo: ", "\nSubject: ", "\nCc: ", "\nMime-Version: ", "\nContent-Type: ", "\nContent-Transfer-Encoding: ", "\nBcc: ", "\nX-From: ", "\nX-To: ", "\nX-cc: ", "\nX-bcc: ", "\nX-Folder: ", "\nX-Origin: ", "\nX-FileName: "]
csv_columns =  ["Message-ID", "Date", "From", "To", "Subject", "Cc", "Mime-Version", "Content-Type", "Content-Transfer-Encoding", "Bcc", "X-From", "X-To", "X-cc", "X-bcc", "X-Folder", "X-Origin", "X-FileName", "body"]

##############################################################################################
# Functions
##############################################################################################
def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]

###############################################################################################
# Parse emails
###############################################################################################
os.chdir(path_data + 'maildir/ + person)
folders = [item for item in glob.glob(path_data + 'maildir/' + person + "/*")]

list = []

for folder in folders:
    emails = [item for item in glob.glob(folder + "/*")]
    for email in emails:
        with open(email, 'r') as eml:
            text = eml.read()
            fields_upd = [x for x in fields if text.find(x) != -1]
            dict = {}
            for i in range(len(fields_upd)):
                if i == 0:
                    dict[fields_upd[i][:-2]] = find_between(text, fields_upd[i], fields_upd[i+1])
                elif (i > 0) and (i < len(fields_upd) - 1):
                    f_name = fields_upd[i].strip(' ').strip('\X-').strip('\n').strip(':')
                    dict[f_name] = find_between(text, fields_upd[i], fields_upd[i+1])
                else:
                    f_name = fields_upd[i].strip(' ').strip('\X-').strip('\n').strip(':')
                    dict[f_name] = find_between(text, fields_upd[i], '\n\n')
            dict['body'] = text.split('\n\n', 1)[1]
            list.append(dict)

###############################################################################################
# Save DF to csv
###############################################################################################
df = pd.DataFrame(list)
df.to_csv(path_data + person + '.csv', encoding = 'utf-8', index=False)
