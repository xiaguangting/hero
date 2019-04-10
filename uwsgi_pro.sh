#!/bin/bash

HOME="/projects/viceo/viceo/"
CMD="/opt/workon_home/viceo/bin/uwsgi"
PID="/var/run/uwsgi_viceo_pro.pid"
INI="pro.ini"

function start()
{
    cd ${HOME};${CMD} --ini ${INI}
}

function stop()
{
    cd ${HOME};${CMD} --ini ${INI} --stop ${PID}
}

function reload()
{
    cd ${HOME};find . -name "*.pyc" -exec rm -rf {} \;
    cd ${HOME};${CMD} --ini ${INI} --reload ${PID}
}

case $1 in
"start")
    start
;;
"stop")
    stop
;;
"restart")
    stop
    start
;;
"reload")
    reload
;;
*)
    echo "Usage: $0 start|stop|reload|restart"
;;
esac
