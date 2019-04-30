"""
Created on: April 2019
Sasha Prokosheva

Clean Enron data mailbox
"""
import pandas as pd
pd.set_option('display.max_colwidth', 500000)
pd.set_option('precision', 0)
import numpy as np
import re
import os


# Date
import datetime

##############################################################################################
# Parameters
##############################################################################################
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

path = dname + '/data/'
file = "skilling-j.csv"

##############################################################################################
# Functions
##############################################################################################
def getData_max_min(filter_name, df, metric, max_value, list_end = 'NA'):
    if list_end == 'top':
        filtered = df.tail(20)
    elif list_end == 'bottom':
        filtered = df.head(20)
    elif (list_end == 'NA') and (max_value == 'all'):
        filtered = df
    else:
        filtered = df[df[metric] < max_value]
    # Number of folders
    num_f = str(len(filtered))

    if max_value == 0:
        str_title = '20 ' + list_end + ' by number of emails'
    elif max_value == 'all':
        str_title = 'Folders by number of emails (Count = ' + num_f + ')'
    else:
        str_title = 'Folders with < ' + str(max_value) + ' emails (Count = ' + num_f + ')'


    return [ {'x':[filtered[metric]], 'y':[filtered[filter_name]], 'text': [filtered[filter_name]], 'orientation': 'h'},
             {'title': str_title } ]

##############################################################################################
def transform_value(value):
    return 10 ** value

##############################################################################################
# Get data
##############################################################################################
df = pd.read_csv(path + file, encoding='utf-8')

df_stats = pd.DataFrame()
df_stats.loc[0, 'Total # of Objects (incl Deleted)'] = len(df)

##############################################################################################
# Replicate all fields
##############################################################################################
# Rename columns
df.rename(index=str, columns={'Date': 'sent_date', 'From': 'sender', 'To': 'to', 'Cc': 'cc', 'Subject': 'subject', 'X-Folder': 'folder' }, inplace = True)

# Drop columns
df.drop(columns = ['Message-ID', 'Bcc', 'X-bcc', 'X-From',  'X-To', 'X-cc', 'Content-Transfer-Encoding', 'Content-Type', 'Mime-Version', 'X-FileName', 'X-Origin'], inplace = True)

# Date and time
df['sent_date'] = pd.to_datetime(df['sent_date'], utc=True)

df['sent_year'] = df['sent_date'].dt.year
df['sent_month'] = df['sent_date'].dt.month
df['sent_day'] = df['sent_date'].dt.day
df['sent_hour'] = df['sent_date'].dt.hour
df['sent_minute'] = df['sent_date'].dt.minute

df = df[df['sent_year'] >= 1990]

df['sent_date'] = pd.to_datetime(dict(year=df.sent_year, month=df.sent_month, day=df.sent_day))

# Clean Folder
df['folder'] = df['folder'].str.replace(r'\\Jeffrey_Skilling_Dec2000\\Notes Folders\\', '')


##############################################################################################
# Clean data
##############################################################################################
# Drop empty body/sender, number of items left
df = df.dropna(subset = ['body']).reset_index(drop=True)
df = df[df['body'] != ''].reset_index(drop=True)
df = df.dropna(subset = ['sender']).reset_index(drop=True)
df = df[df['sender'] != ''].reset_index(drop=True)

# sent_date, day_of_week, sent_last_month ('YES', 'NO')
df['day_of_week'] = df['sent_date'].dt.day_name()

# Make email address lower case
df['sender'] = df['sender'].str.lower()

# In / Out
df['in_out'] = df.apply(lambda row: 'OUT' if row['folder'] == '_sent_mail' or row['sender'] == 'sherri.sera@enron.com' or row['sender'] == 'jeff.skilling@enron.com' or row['sender'] == 'sherri.reinartz@enron.com' else 'IN', axis = 1)

# Reply/Forward/Original Email (YES/FWD/NO)
df['reply'] = df.apply(lambda row: 'YES' if str(row['subject']).find('RE:') == 0 or str(row['subject']).find('Re:') == 0 or str(row['subject']).find('re:') == 0 else 'FW' if str(row['subject']).find('FW:') != -1 else 'NO', axis = 1)


df['enron'] = df.apply(lambda row: 'YES' if str(row['sender']).find('@enron') >= 0 else 'NO', axis = 1)

# Clean from \n and \t
df = df.replace('\n', '', regex=True)
df = df.replace('\t', '', regex=True)

# Clean To and Cc
df['to'] = df['to'].astype(str)
df['cc'] = df['cc'].astype(str)
df = df[df['cc'].apply(lambda x: 'Subject:' not in x)]
df = df[df['sender'].apply(lambda x: '40enron@enron.com' not in x)]

##############################################################################################
# Non-replies emails
##############################################################################################
df_nr = df[df['reply'] == 'NO']

##############################################################################################
# Duplicated emails
##############################################################################################
df_stats.loc[0, '% of Duplicated'] = "{:.2%}".format(len(df[df.duplicated(subset=['body', 'cc', 'sender', 'sent_date', 'subject', 'to'], keep='first') == True]) / len(df) )

df = df[df.duplicated(subset=['body', 'cc', 'sender', 'sent_date', 'subject', 'to'], keep='first') == False]
df_stats.loc[0, 'Cleaned Data'] = len(df)

##############################################################################################
# DFs for GRAPHS
##############################################################################################
# 1. Folders
##############################################################################################
folders_list = pd.pivot_table(df, index=['folder'], values=['body'], aggfunc=len).sort_values(('body'), ascending=True)
folders_list = pd.DataFrame(folders_list.to_records())
folders_list.columns = ['folder', 'count']
folders_list = folders_list.reset_index(drop = True)

df_stats.loc[0, '# of Folders in Inbox'] = len(folders_list)

# SAVE
folders_list.to_csv(path + 'folders_list.csv', encoding='utf-8', index = False)
df_stats.to_csv(path + 'df_stats.csv', encoding='utf-8', index = False)
##############################################################################################
# 2. Daily counts
##############################################################################################
sent_date_count = df[df['in_out'] == 'OUT'].groupby(['sent_date', 'day_of_week'])['body'].count().reset_index(name='count')
in_date_count = df[df['in_out'] == 'IN'].groupby(['sent_date', 'day_of_week'])['body'].count().reset_index(name='count')

# SAVE
sent_date_count.to_csv(path + 'sent_date_count.csv', encoding='utf-8', index = False)
in_date_count.to_csv(path + 'in_date_count.csv', encoding='utf-8', index = False)

##############################################################################################
# 3. Average number of emails per weekday
##############################################################################################
df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'], ordered=True)
in_day_mean = df[df['in_out'] == 'IN'].groupby(['sent_date','day_of_week'])['body'].count().reset_index().groupby('day_of_week').mean().round(0).reset_index()
sent_day_mean = df[df['in_out'] == 'OUT'].groupby(['sent_date','day_of_week'])['body'].count().reset_index().groupby('day_of_week').mean().round(0).reset_index()

# SAVE
in_day_mean.to_csv(path + 'in_day_mean.csv', encoding='utf-8', index = False)
sent_day_mean.to_csv(path + 'sent_day_mean.csv', encoding='utf-8', index = False)
##############################################################################################
# 4. Average number of incoming emails by hour
##############################################################################################
in_hour_mean = df[df['in_out'] == 'IN'].groupby(['sent_date','sent_hour'])['body'].count().reset_index().groupby('sent_hour').mean().round(2).reset_index()

in_hour_mean_orig = df_nr[df_nr['in_out'] == 'IN'].groupby(['sent_date','sent_hour'])['body'].count().reset_index().groupby('sent_hour').mean().round(2).reset_index()

out_hour_mean = df[df['in_out'] == 'OUT'].groupby(['sent_date','sent_hour'])['body'].count().reset_index().groupby('sent_hour').mean().round(2).reset_index()

out_hour_mean_orig = df_nr[df_nr['in_out'] == 'OUT'].groupby(['sent_date','sent_hour'])['body'].count().reset_index().groupby('sent_hour').mean().round(2).reset_index()

# SAVE
in_hour_mean.to_csv(path + 'in_hour_mean.csv', encoding='utf-8', index = False)
in_hour_mean_orig.to_csv(path + 'in_hour_mean_orig.csv', encoding='utf-8', index = False)
out_hour_mean.to_csv(path + 'out_hour_mean.csv', encoding='utf-8', index = False)
out_hour_mean_orig.to_csv(path + 'out_hour_mean_orig.csv', encoding='utf-8', index = False)

##############################################################################################
# 5. Who sends vs who gets emails
##############################################################################################
# List of TO
df_5 = df[df['in_out'] == 'OUT'][['to', 'cc']]
df_5 = df_5.replace(np.nan, '', regex=True)
df_5['to_all'] = df_5['to'] + ', ' + df_5['cc'] + ', '
df_5 = df_5.drop(['to', 'cc'], axis = 1)

# Make a string and replace string values
string = str(df_5.sum())
string = string.replace('to_all', '')
string = string.replace('nan', '')
string = string.replace('\ndtype: object', '')
string = string.replace("'", '')

# Split into names
list = string.split(', ')
list = [x.strip() for x in list if x]
list_to = np.unique(list, return_counts=True)

# Make TO df
df_to = pd.DataFrame({'to':list_to[0], 'counts':list_to[1]})
df_to.sort_values(by = ['counts'], ascending=False, inplace = True)

# Make FROM df
df_from = df[df['in_out'] == 'IN'].groupby(['sender'])['body'].count().reset_index()
df_from = df_from[df_from['sender'].apply(lambda x: len(x)<50)]

# Merge
df_to_from = pd.merge(df_to,
                      df_from,
                     left_on = 'to',
                      right_on = 'sender',
                      how = 'outer')

df_to_from['sender'] = df_to_from['sender'].combine_first(df_to_from['to'])
df_to_from.drop(columns = ['to'], inplace = True)
df_to_from.rename(columns = {'counts': 'OUT', 'body': 'IN'}, inplace = True)
df_to_from['group'] = df_to_from['sender'].str.extract('(@.*)', expand=True)

# Get rid of NAs
df_to_from.fillna(0, inplace=True)

# SAVE
df_to_from.to_csv(path + 'df_to_from.csv', encoding='utf-8', index = False)

##############################################################################################
# 7. Top 20 senders
##############################################################################################
senders_20 = pd.DataFrame(pd.pivot_table(df, index=['sender'], values=['body'], columns = ['sent_year'],  aggfunc=len).to_records())
senders_20.fillna(0, inplace=True)
senders_20.rename(columns={'sender': 'Sender', "('body', 1998)": '1998', "('body', 1999)": '1999', "('body', 2000)": '2000', "('body', 2001)": '2001'}, inplace=True)
senders_20 = senders_20[['Sender', '1999', '2000', '2001']]
senders_20['Total'] = senders_20.iloc[:,1:].sum(axis = 1)
senders_20.sort_values(by = ['Total'], ascending=False, inplace = True)
df_senders_20 = senders_20.head(20)

# SAVE
df_senders_20.to_csv(path + 'df_senders_20.csv', encoding='utf-8', index = False)

##############################################################################################
# 8. Top 20 groups
##############################################################################################
df['group'] = df['sender'].str.extract('(@.*)', expand=True)
senders_20_group = pd.DataFrame(pd.pivot_table(df[df['in_out'] == 'IN'], index=['group'], values=['body'], columns = ['sent_year'],  aggfunc=len).to_records())
senders_20_group.fillna(0, inplace=True)
senders_20_group.rename(columns={'group': 'Group', "('body', 1998)": '1998', "('body', 1999)": '1999', "('body', 2000)": '2000', "('body', 2001)": '2001'}, inplace=True)
senders_20_group = senders_20_group[['Group', '1999', '2000', '2001']]
senders_20_group['Total'] = senders_20_group.iloc[:,1:].sum(axis = 1)
senders_20_group.sort_values(by = ['Total'], ascending=False, inplace = True)
df_senders_20_group = senders_20_group.head(20)

# SAVE
df_senders_20_group.to_csv(path + 'df_senders_20_group.csv', encoding='utf-8', index = False)
