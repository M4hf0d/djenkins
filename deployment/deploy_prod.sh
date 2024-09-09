#!/bin/sh

ssh root@167.71.32.72<<EOF
  cd Event-Registration
  git pull
  source /opt/envs/Event-Registration/bin/activate
  pip install -r requirements.txt
  ./manage.py makemigrations
  ./manage.py migrate  --run-syncdb
  sudo service gunicorn restart
  sudo service nginx restart
  exit
EOF