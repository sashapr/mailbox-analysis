"""
Created on: December 2018 - March 2019
Sasha Prokosheva

Mailbox analysis: Download data
"""
import pandas as pd
pd.set_option('display.max_colwidth', 500000)
pd.set_option('precision', 0)
import numpy as np

# Windows
import win32com.client

# Date
import datetime



##############################################################################################
# Parameters
##############################################################################################
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts
name = input("Please type mailbox address (in the format e.g. your_name@domain.ext): ")
folder = outlook.Folders(name)


##############################################################################################
# Functions
##############################################################################################
def get_messages(folder, mail, folder_name):
    for i in folder.items:
        message = {}
        message['folder'] = folder_name
        try:
            message['subject'] = i.subject
        except:
            message['subject'] = np.NAN
        try:
            message['sender'] = i.SenderName
        except:
            message['sender'] = np.NAN
        try:
            message['sender_email'] = i.Sender.GetExchangeUser().PrimarySmtpAddress
        except:
            message['sender_email'] = np.NAN
        try:
            message['sender_email2'] = i.SenderEmailAddress
        except:
            message['sender_email2'] = np.NAN
        try:
            message['to'] = i.to
        except:
            message['to'] = np.NAN
        try:
            message['cc'] = i.cc
        except:
            message['cc'] = np.NAN
        try:
            message['unread'] = i.UnRead
        except:
            message['unread'] = np.NAN
        try:
            message['body'] = i.body
        except:
            message['body'] = np.NAN
        try:
            message['size'] = i.Size
        except:
            message['size'] = np.NAN
        try:
            message['importance'] = i.Importance
        except:
            message['importance'] = np.NAN
        try:
            message['conversation_id'] = i.ConversationID
        except:
            message['conversation_id'] = np.NAN
        try:
            message['conversation_index'] = i.ConversationIndex
        except:
            message['conversation_index'] = np.NAN
        try:
            message['conversation_topic'] = i.ConversationTopic
        except:
            message['conversation_topic'] = np.NAN
        try:
            message['sent_year'] = i.SentOn.year
            message['sent_month'] = i.SentOn.month
            message['sent_day'] = i.SentOn.day
            message['sent_hour'] = i.SentOn.hour
            message['sent_minute'] = i.SentOn.minute
        except:
            message['sent_year'] = np.NAN
            message['sent_month'] = np.NAN
            message['sent_day'] = np.NAN
            message['sent_hour'] = np.NAN
            message['sent_minute'] = np.NAN
        mail.append(message)
    return mail

##############################################################################################
# Get data
##############################################################################################
mail = []

for folder in folder.Folders:
    f = folder
    f_name = folder.Name
    print(f_name, len(folder.items))
    mail = get_messages(f, mail, f_name)

    for folder1 in folder.Folders:
        f1 = folder1
        f1_name = f_name + "/" + folder1.Name
        print(f1_name, len(folder1.items))
        mail = get_messages(f1, mail, f1_name)

        for folder2 in folder1.Folders:
            f2 = folder2
            f2_name = f1_name + "/" + folder2.Name
            print(f2_name, len(folder2.items))
            mail = get_messages(f2, mail, f2_name)

            for folder3 in folder2.Folders:
                f3 = folder3
                f3_name = f2_name + "/" + folder3.Name
                print(f3_name, len(folder3.items))
                mail = get_messages(f3, mail, f3_name)

                for folder4 in folder3.Folders:
                    f4 = folder4
                    f4_name = f3_name + "/" + folder4.Name
                    print(f4_name, len(folder4.items))
                    mail = get_messages(f4, mail, f4_name)

##############################################################################################
# Save data
##############################################################################################
df = pd.DataFrame(mail)
df.to_csv('mail.csv', encoding='utf-8', index = False)
