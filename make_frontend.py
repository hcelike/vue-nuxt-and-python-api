import os

def make():
    os.system('cd frontend && sudo yarn install && cd ..')
    os.system('cd frontend && sudo yarn build') 

if __name__ == '__main__':
    make()
