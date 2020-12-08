66% Capital Risk Management 
==========================

[![pipeline status](https://gitlab.com/sixty-six-percent/active/space-boa/badges/master/pipeline.svg)](https://gitlab.com/sixty-six-percent/active/space-boa/-/commits/master)

### Dependencies

- MongoDB >= 4.2
- Python >=3.5

### Environment Variables

Application secrets are stored in a `.env` that is not/should never be committed 

### Getting Started

To run locally:

1. Clone the repo and `cd` into it
2. Put the `.env` file in the root directory
3. Install the python dependencies, `pip3 install -r requirements.txt`
4. From the root directory run `python3 app.py`
6. (Frontend) In a separate terminal tab, in the `frontend/` directory run `yarn install` and `yarn dev` 

### Deploying to Production

We run our flask app on AWS EC2 with an Ubuntu 16.04 lts instance. This version matters for some of the deployment scripts.

To deploy:

1. Create an instance at EC2
2. Point DNS records to the instance (the config mentions the subdomains)
3. ssh into the production server. `ssh root@<domain>` (your public key is in `~/.ssh/authorized_keys` or use the .pem from Ec2) 
4. `mkdir /home/www` 
5. `cd /home/www`
6. If there is no git username on the server, `git config --global user.name <your username>; git config --global user.email <your email>`
7. `git clone` the repository from gitlab (you will need to add an ssh key to gitlab first) and `cd` into it
8. Put your `.env` file into the root directory
9. run `python3 make_server.py` which installs the dependencies for ubuntu, python, and starts the server (the repo directory will be renamed `flask_project`)
10. run `certbot` to get ssl 
11. Now, you should be running 
12. You can check the logs by running `supervisorctl` 

### Making Changes in Production

1. ssh into the production server. `ssh root@<domain>` (your public key is in `~/.ssh/authorized_keys`)
2. go to the project directory `cd /home/www/flask_project`
3. build the frontend with `python3 make_deploy.py` which:  
     - pulls the changes from remote git repo with `git pull` (the server's public key is at github already)
     - builds the frontend with `make_frontend.py`
     - restarts the server with `supervisorctl restart flask_project`
