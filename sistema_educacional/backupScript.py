from pathlib import Path
import local_settings
import os
import datetime


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

# Se executado como script
if __name__ == '__main__':
    criar_backup()
