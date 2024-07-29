# file_manager/google_drive.py
import io
import pickle
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from django.conf import settings
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

CREDENTIALS_PATH = 'credentials.json'

def get_drive_service(user):
  creds = None
  user_id = user.id  # Use user ID or user.email for unique identification
  pickle_path = f'token_{user_id}.pickle'

  # Load credentials from pickle file if it exists
  if os.path.exists(pickle_path):
      with open(pickle_path, 'rb') as token:
          creds = pickle.load(token)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
          creds = flow.run_local_server(port=8001)
      # Save the credentials for the next run
      with open(pickle_path, 'wb') as token:
          pickle.dump(creds, token)

  service = build('drive', 'v3', credentials=creds)
  return service


def check_file_permissions(file_id, user):
  service = get_drive_service(user)
  permissions = service.permissions().list(fileId=file_id).execute()

  for permission in permissions.get('permissions', []):
      if permission:
          return True
  return False

def download_file(file_id, file_name, user):
  service = get_drive_service(user)
  file = service.files().get(fileId=file_id).execute()
  mime_type = file['mimeType']

  # Check if the file is a Google Docs Editors file
  if mime_type.startswith('application/vnd.google-apps.'):
      # Define export MIME type
      if mime_type == 'application/vnd.google-apps.document':
          export_mime_type = 'application/pdf'
      elif mime_type == 'application/vnd.google-apps.spreadsheet':
          export_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          file_name += '.xlsx'  # Set the file name extension
      elif mime_type == 'application/vnd.google-apps.presentation':
          export_mime_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
          file_name += '.pptx'  # Set the file name extension
      else:
          export_mime_type = 'application/pdf'
      
      request = service.files().export_media(fileId=file_id, mimeType=export_mime_type)
      file_name = f"{file_name}.{export_mime_type.split('/')[-1]}"
  else:
      request = service.files().get_media(fileId=file_id)

  file_stream = io.BytesIO()
  downloader = MediaIoBaseDownload(file_stream, request)
  done = False
  while not done:
      status, done = downloader.next_chunk()
      print(f'Download {int(status.progress() * 100)}%.')
  
  print('Download complete.')
  file_stream.seek(0)
  return file_stream, file_name, mime_type  # Return the mime_type

def list_files(user):
  service = get_drive_service(user)
  results = service.files().list(pageSize=50, fields="nextPageToken, files(id, name, size)").execute()
  items = results.get('files', [])
  return items