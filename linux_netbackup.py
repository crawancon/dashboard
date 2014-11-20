#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve netbackup version and drop them into Django dashboard
#
# Boomer Rehfield - 11/18//2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import re
import test_server
django.setup()


def update_server():
    server_list = LinuxServer.objects.all()
    #FIXME quick way of testing a few servers
    #do not use a list/dict as it needs the actual object for the 'server'
    #server_list = LinuxServer.objects.filter(name='u3midcap2')
    for server in server_list:
        server_is_active=1

        if LinuxServer.objects.filter(name=server):

            if test_server.ping(server):

                #LinuxServer.objects.filter(name=server).update(active=True)
                client = SSHClient()
                client.load_system_host_keys()
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    #SSH fails so we set it to an exception, update the modified time, and add a log entry
                    LinuxServer.objects.filter(name=server).update(exception=True, modified=timezone.now())
                    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    continue


                stdin, stdout, stderr = client.exec_command('[ -f /usr/openv/netbackup/bin/version ] && cat /usr/openv/netbackup/bin/version || echo "None"')
                netbackup_version = stdout.readlines()[0]

                 
                #check existing value, if it exists, don't update
                if str(netbackup_version) != str(server.netbackup):
                    LinuxServer.objects.filter(name=server, exception=False, active=True).update(netbackup=netbackup_version, modified=timezone.now())
                    #pretty sure the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                    change_message = 'Changed netbackup to ' + str(netbackup_version)
                    LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                    #FIXME - ok, we're going to create the manual log here, haven't worked it all out yet how I want to do it though
                    #We can do that or we can FK to the admin log...should we try to add our own columns?
                    #log = LinuxServer.objects.log(name=server 




#start execution
if __name__ == '__main__':
    print "Checking Netbackup versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
