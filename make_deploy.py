import os
import make_frontend

def make():
    os.system('git pull')
    os.system('pip3 install -r requirements.txt')
    os.system('supervisorctl restart flask_project')
    os.system('crontab crontab.conf')
    make_frontend.make()
    os.system('supervisorctl restart frontend')
    os.system('sudo kill -9 `sudo lsof -t -i:8081`')
    os.system('sudo kill -9 `sudo lsof -t -i:8000`')
    

if __name__ == '__main__':
    make()
