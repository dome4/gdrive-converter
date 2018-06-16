from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import json
import io
import sys

"""
main method of the script
"""
def main():
    gdrive = auth()

    args1 = None
    
    try:
        # get root folder as argument
        args1 = sys.argv[1]
    except IndexError:
        print('Pleade add the root folder as first argument and try again')

    root_folder = os.path.join(args1)

    loopFolder(gdrive, root_folder)

"""
google oauth
"""
def auth():
    # Setup the Drive v3 API
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('drive', 'v3', http=creds.authorize(Http()))

    return service

"""
loop through folder
"""
def loopFolder(gdrive, current_path):
    
    for filename in os.listdir(current_path):
        
        if filename.endswith(".gdoc") or filename.endswith(".gsheet") or filename.endswith(".gslides"):
             # check if file is google file

            file_path_complete = os.path.join(current_path, filename) # path with file

            with io.open(file_path_complete, mode = 'r',encoding='utf-8') as data_file:    

                data = json.load(data_file)
                file_id = data ['doc_id']

                downloadFile(gdrive, filename, file_id, current_path)

                # remove old file
                os.remove(file_path_complete)
            
        elif os.path.isdir(os.path.join(current_path, filename)):
            # check if file is folder

            folder_path_complete = os.path.join(current_path, filename)
            loopFolder(gdrive, folder_path_complete) # recursive method call

   
"""
download google files
"""
def downloadFile(gdrive, filename, file_id, file_path):

                
    if filename.endswith(".gdoc"):
        request = gdrive.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        filename = filename[:-5] # remove file type     
        filename = filename + '.docx'
        
    elif filename.endswith(".gsheet"):
        request = gdrive.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = filename[:-7] # remove file type     
        filename = filename + '.xlsx' 
            
    elif filename.endswith(".gslides"):
        request = gdrive.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        filename = filename[:-8] # remove file type     
        filename = filename + '.pptx'

    # download files
    response = request.execute()

    # save response in file
    with open(os.path.join(file_path, filename), "wb") as writeStream:
        writeStream.write(response)

    print ('{0} | id: {1} - file download finished'.format(filename, file_id))
 

"""
run main-method
"""
if __name__ == '__main__':
    main()