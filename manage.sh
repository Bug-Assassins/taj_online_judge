#!/bin/bash

command=$1

if [[ $UID -ne $ROOT_UID ]] ; then
	echo -e "Please Run This Script with as Sudo"
	exit 127
fi

case $command in
    'runserver')
        #Run database sever first
        sudo /opt/lampp/lampp start
        if [ $? -eq 0 ]; then
            python manage.py runserver --settings=TAJ.settings
        else
            "Could Not Start Database Server"
        fi
        ;;

    'maintain')
        python manage.py clearsession
        ;;

    'sync')
        python manage.py makemigrations
        python manage.py syncdb
        ;;

    'install')
        #Installing Python, Django
        apt-get install python python-pip
        
        #Installing Necessary Python Packages
        pip install django
        pip install datetime

        #Installing Mysql Server
        apt-get install mysql-server

        #Installing Docker
        apt-get install apt-transport-https
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
	sh -c "echo deb https://get.docker.com/ubuntu docker main\
> /etc/apt/sources.list.d/docker.list"
        sh -c "echo deb https://get.docker.com/ubuntu docker main /etc/apt/sources.list.d/docker.list"
        apt-get update
        apt-get install lxc-docker

        #Installing Task Queing Stuff
        apt-get install rabbitmq-server

        echo -e "\n\nInstallation Complete. Please Configure Database and other Settings"
        ;;

    *)
        python manage.py $command
        ;;
esac
