import os
import io
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

store = file.Storage('_token.json')
creds = store.get()
service = build('drive', 'v3', http=creds.authorize(Http()))

file_id = os.environ.get('GOOGLEDRIVE_FILEID')
request = service.files().export_media(fileId=file_id, mimeType='text/csv')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))
