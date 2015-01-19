#!/bin/bash

command='$1'

case $command in
    'runserver')
        #Run database sever first
        sudo /opt/lampp/lampp start
        if [ $? -eq 0 ]; then
            python manage.py runserver
        else
            "Could Not Start Database Server"
        fi
        ;;

    'maintain')
        python manage.py clearsession
        ;;

    'sync')
        python manage.py makemigration
        python manage.py syncdb
        ;;

    'install')
        #Installing Python, Django
        sudo apt-get install python
        sudo apt-get install python-pip
        sudo pip install django
        sudo pip install datetime
elif [ $command - eq]
else
    python manage.py command
