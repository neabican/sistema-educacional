# Como rodar o projeto

Passos e comandos necessarios

ter o git instalado
mudar para a branch desenvolvimento  
git checkout desenvolvimento  


sudo apt-get install python3-venv  
python3 -m venv myvenv

source myvenv/bin/activate  


sudo apt-get install python3-pip  
python3 -m pip install --upgrade pip  


primeiro realizar a instalacao e configuracao do banco de dados  
pip install -r requirements.txt  

apagar as migrations existentes nos apps, deixar __init__.py e __pycache__  
python manage.py makemigrations  
python manage.py migrate  

python manage.py createsuperuser  


python manage.py runserver  
acessar: http://127.0.0.1:8000/  