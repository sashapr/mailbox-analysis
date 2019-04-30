## Mailbox Analysis
### Script to download Outlook inbox and visualize it using Plotly Dash
#### Dashboard example: https://mailbox-analysis.herokuapp.com/

This tool was designed to analyze heavily swamped corporate inboxes. Especially, it could be useful for team mailboxes: When several individuals operate one mailbox in Microsoft Outlook. Data visualization can serve as a starting point for a conversation about how the team can improve the processes connected to this mailbox: When are the most of emails coming? Who are the users that send most of emails? What is the structure of the mailbox? Who gets replies vs who sends emails? These and many other quesitons can be answered using these scripts. Dashboard can be modified accordingly, the example provided is just a rather simple overview. 

### Contents
[I. Files in repo](#i-files-in-repo) <br/>
[II. Example: Mailbox of J. Skilling, ex-CEO of ENRON](#ii-example-enron) <br/>

### I. Files in repo
There are three python codes in this repo:
1. Download data (mailbox_download.py) -- file to download data from MS Outlook (enron_download cleans data for Enron mailbox)
2. Clean data (enron_clean) -- file to modify and prepare data to be uploaded to Plotly Dash dashboard
3. Create dashboard (enron_dash) -- file to publish data as a Plotly Dash app


### II. Example: Enron
As an example, I used one of the mailboxes from [ENRON mail dataset](https://www.cs.cmu.edu/~./enron/).
