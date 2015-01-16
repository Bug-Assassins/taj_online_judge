#!/bin/bash

command='$1'

if [ $command -eq 'runserver']; then

    #Run database sever first
    sudo /opt/lampp/lampp start
    if [ $? -eq 0 ]; then
        python manage.py runserver
    else
        "Could Not Start Database Server"
    fi

elif [ $command -eq 'maintain']; then
    python manage.py clearsession

elif [ $command -eq 'sync']; then
    python manage.py makemigration
    python manage.py syncdb

else
    python manage.py command
