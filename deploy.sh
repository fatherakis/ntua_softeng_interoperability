#!/usr/bin/env bash

#Deploy API etc

python3 -m venv ../tl_env
sudo pip install -r requirements.txt

#in the backround (fork):
(cd cli && chmod +x ./install && source ./install; wait) & wait


#optional argument: the port => http server
if [ $# -ge 1 ]
  then
    python3 manage.py runserver localhost:$1
  else
    python3 manage.py runserver_plus localhost:9103 --cert-file cert.pem --key-file key.pem --insecure
fi
