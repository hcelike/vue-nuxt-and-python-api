import os
import platform
import make_frontend



def main():
    print(os.name) #returns os name in simple form
    print(platform.system()) #returns the base system, in your case Linux
    print(platform.release())
    print(platform.linux_distribution())
    os.system('sudo apt-get update')
    os.system('sudo apt -y upgrade')

    # python 
    os.system('sudo apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev nginx gunicorn3 supervisor python-setuptools')
    os.system('sudo apt-get install libjpeg-dev zlib1g-dev')
    os.system('sudo pip3 install --upgrade pip')

    # node 
    os.system('sudo apt-get update')
    os.system('curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -')
    os.system('sudo apt-get install nodejs -y')

    # yarn
    os.system('curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -')
    os.system('echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')
    os.system('sudo apt update && sudo apt install yarn')
    
    # start server
    os.system('pip3 install -r requirements.txt')
    os.rename(os.getcwd(), '/home/www/flask_project')

    # do the front-end build
    make_frontend.make()

    os.system('python3 make_nginx.py')

    os.system('supervisord')

    # cron
    #os.system('crontab crontab.conf')

    # certbot
    os.system('sudo apt-get update')
    os.system('sudo apt-get install software-properties-common')
    os.system('sudo add-apt-repository ppa:certbot/certbot')
    os.system('sudo apt-get update')
    os.system('sudo apt-get install python-certbot-nginx')
    
    
if __name__ == '__main__':
    main()
