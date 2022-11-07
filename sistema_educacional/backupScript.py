import local_settings
import settings
import os
import datetime
from time import sleep

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def criar_backup():

    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None

    # Informações do local Settings
    DB_HOST = local_settings.DB_HOST
    DB_USER = local_settings.DB_USER
    DB_PASSWORD = local_settings.DB_PASSWORD
    DB_NAME = local_settings.DB_NAME

    # Realizando o Backup do banco de dados
    dir = os.path.join(settings.BASE_DIR, 'backups')
    if not os.path.exists(dir):
        os.makedirs(dir)
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    name = '{}-backup.sql.gz'.format(now)
    file_path = os.path.join(dir, name)
    os.system(f'mysqldump -h {DB_HOST} -u {DB_USER} -p\'{DB_PASSWORD}\' \'{DB_NAME}\' --set-gtid-purged=OFF --no-tablespaces --column-statistics=0 | gzip -9 -c > {file_path}')
    sleep(10)

    # Validando credenciais
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "OAuth_token.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        response = service.files().list(
            q="name='BackupFolder' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()

        # Caso a pasta não exista
        if not response['files']:
            file_metadata = {
                "name": "BackupFolder",
                "mimeType": "application/vnd.google-apps.folder"
            }
            file = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = file.get('id')
        else:
            # Caso a pasta exista, pego seu id
            folder_id = response['files'][0]['id']

        # Realizando o ‘backup’ das informações
        file_metadata = {
            "name": name,
            "parents": [folder_id]
        }

        media = MediaFileUpload(f'{dir}/{name}')
        upload_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    except HttpError as e:
        print("Error "+str(e))


# Se executado como script
if __name__ == '__main__':
    criar_backup()
