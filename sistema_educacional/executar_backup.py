#!/usr/bin/env python3

from pathlib import Path
import local_settings
import os
import datetime
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def criar_backup():
    # Informações do local Settings
    DB_HOST = local_settings.DB_HOST
    DB_USER = local_settings.DB_USER
    DB_PASSWORD = local_settings.DB_PASSWORD
    DB_NAME = local_settings.DB_NAME

    # Realizando o Backup do banco de dados
    BASE_DIR = Path(__file__).resolve().parent.parent
    dir = os.path.join(BASE_DIR, 'backups')
    if not os.path.exists(dir):
        os.makedirs(dir)
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    name = '{}-backup.sql.gz'.format(now)
    file_path = os.path.join(dir, name)
    os.system(f'mysqldump -h {DB_HOST} -u {DB_USER} -p\'{DB_PASSWORD}\' \'{DB_NAME}\' --set-gtid-purged=OFF --no-tablespaces --column-statistics=0 | gzip -9 -c > {file_path}')
    # Drive autenticacao
    gauth = GoogleAuth()
    try:
        gauth.LoadCredentialsFile('mycreds.txt')
    except Exception:
        print("ERRO: Nao foi possivel carregar as credenciais")

    drive = GoogleDrive(gauth)
    # Upload arquivo
    file = drive.CreateFile({'parents': [{'id': '1Fd1xTGtZAN4PwUgzLxjYeJmrKJmjc2nd'}]})
    file.SetContentFile(arquivo)
    file['title'] = nome
    file.Upload()
    # Remove arquivo local
    time.sleep(5)
    os.remove(arquivo)



if __name__ == '__main__':
    criar_backup()
