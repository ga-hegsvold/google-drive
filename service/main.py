from __future__ import print_function
import httplib2
import io

from apiclient import discovery
from oauth2client import tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth

# If modifying these scopes, delete your previously saved credentials
# at ~/_.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)


def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def uploadFile(filename, filepath, mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def downloadFile(file_id, filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))


def searchFile(size, query):
    results = drive_service.files().list(
        pageSize=size,
        fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))


def export(self, spreadsheet_id, fformat, filename=None):
    fformat = getattr(fformat, 'value', fformat)
    request = self.driveService.files().export(fileId=spreadsheet_id, mimeType=fformat.split(':')[0])
    import io
    ifilename = spreadsheet_id+fformat.split(':')[1] if filename is None else filename
    fh = io.FileIO(ifilename, 'wb')
    downloader = http.MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


#uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
#downloadFile('1f7nky9ysp6EhzJ5iMvQ2dP2g50B41jQO3XDRjYM94IY','character.csv')
export('1f7nky9ysp6EhzJ5iMvQ2dP2g50B41jQO3XDRjYM94IY','csv','character.csv')
#createFolder('Google')
#searchFile(10,"name contains 'Getting'")
