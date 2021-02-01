# ubuntu-nginx-gunicorn-postgresql-django-conf
Config for install Python3 + Nginx + gunicorn+ Postgresql  + Django3 on Ubuntu 

# Структура

code/project1/bin(start_gunicor.sh), env, project1, requirements.txt

code/project1/project1/first, project1, gunicorn_config.py, manage.py, db.sqlite3

# Необходимые инстументы #

```
sudo apt-get update
sudo apt-get upgrade 
sudo apt-get install -y htop git curl wget zip gcc build-essential make tree
sudo apt-get install python3-venv
sudo apt-get install python3-pip
sudo apt-get install nginx
sudo apt-get install supervisor 
```

# Ход #

mkdir ~/code

cd code

mkdir project1

cd project1

(/home/www/code/project1/) python3 venv env 

. env/bin/activate

pip install -U pip

pip install django

django-admin startproject project1

cd project1

pip install ipython

python3 manage.py startapp first


# Gunicorn
В /home/www/code/project1/project1

pip install gunicorn

pip freeze > ..requirements.txt

(project1): nano gunicorn_config.py


```
command = '/home/wiki/code/project1/env/bin/gunicorn'
pythonpath = '/home/wiki/code/project1/project1'
bind = '127.0.0.1:8001'
workers = 4
user = 'wiki'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=project1.settings'
```

cd ..

mkdir bin/

nano bin/start_unicorn.sh

```
#!/bin/bash
source /home/wiki/code/project1/env/bin/activate
exec gunicorn -c "/home/wiki/code/project1/project1/gunicorn_config.py" project1.wsgi
```
chmod +x bin/start_gunicorn.sh

# Nginx

sudo nano /etc/nginx/sites-enabled/default

```
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;

	index index.html index.htm index.nginx-debian.html;

	server_name _;
	
	 location /static/ {
		root /home/wiki/project1/;
	    }
	    
	location / {
		proxy_pass http://127.0.0.1:8001;
		proxy_set_header X-Forwarded-Host $server_name;
		proxy_set_header X-Real-IP $remote_addr;
		add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
		add_header Access-Control-Allow-Origin *;
	}

}
```

sudo service nginx restart

# Supervisor

sudo nano /etc/supervisor/conf.d/project1.conf

```
[program:wiki_gunicorn]
command=/home/wiki/code/project1/bin/start_gunicorn.sh
user=wiki
process_name=%(program_name)s
numprocs=1
autostart=true
autorestart=true
redirect_stderr=true
```

service supervisor start

# Postgresql

```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - ; \
RELEASE=$(lsb_release -cs) ; \
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list ; \
sudo apt update ; \
sudo apt -y install postgresql-11 ; \
sudo localedef ru_RU.UTF-8 -i ru_RU -fUTF-8 ; \
export LANGUAGE=ru_RU.UTF-8 ; \
export LANG=ru_RU.UTF-8 ; \
export LC_ALL=ru_RU.UTF-8 ; \
sudo locale-gen ru_RU.UTF-8 ; \
sudo dpkg-reconfigure locales


sudo passwd postgres
su - postgres
export PATH=$PATH:/usr/lib/postgresql/11/bin
createdb --encoding UNICODE dbms_db --username postgres
exit
```
