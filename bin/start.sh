#!/bin/sh
#
# Add this file to crontab to start "checklist" at boot:
# @reboot /home/checklist/checklist/bin/start.sh

PROJDIR=$HOME/checklist
PIDFILE="$PROJDIR/checklist.pid"
SOCKET="$PROJDIR/checklist.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

/usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi --settings=checklist.settings socket=$SOCKET pidfile=$PIDFILE outlog=$OUTLOG errlog=$ERRLOG workdir=$PROJDIR

chmod a+w $SOCKET

