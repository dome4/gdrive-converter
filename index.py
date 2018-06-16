"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import json
import io

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive v3 API
# results = service.files().list(
#     pageSize=10, fields="nextPageToken, files(id, name)").execute()
# items = results.get('files', [])
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print('{0} ({1})'.format(item['name'], item['id']))




def loopFolder(current_path):
    
    for filename in os.listdir(current_path):
        
        if filename.endswith(".gdoc") or filename.endswith(".gsheet") or filename.endswith(".gslides"):
             # check if file is google file

            file_path_complete = os.path.join(current_path, filename) # path with file

            with io.open(file_path_complete, mode = 'r',encoding='utf-8') as data_file:    

                data = json.load(data_file)
                file_id = data ['doc_id']

                downloadFile(filename, file_id, current_path)
            
        elif os.path.isdir(os.path.join(current_path, filename)):
            # check if file is folder

            folder_path_complete = os.path.join(current_path, filename)
            loopFolder(folder_path_complete) # recursive method call

   

def downloadFile(filename, file_id, file_path):

    print ('{0} | id: {1} - download started'.format(filename, file_id))


# start method
root_folder = os.path.join('/home/dominic/Desktop/11_IT')
loopFolder(root_folder) 