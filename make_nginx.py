import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def make():
    os.system('sudo /etc/init.d/nginx start')
    os.system('sudo rm /etc/nginx/sites-enabled/default')
    os.system('sudo touch /etc/nginx/sites-available/flask_project')
    os.system('sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/flask_project')

    os.system('sudo touch /etc/nginx/sites-available/frontend')
    os.system('sudo ln -s /etc/nginx/sites-available/frontend /etc/nginx/sites-enabled/frontend')

    os.system('cp nginx_server.conf /etc/nginx/sites-enabled/flask_project')    
    os.system('cp nginx_frontend.conf /etc/nginx/sites-enabled/frontend')    
    os.system('sudo /etc/init.d/nginx restart')


if __name__ == '__main__':
    make()
