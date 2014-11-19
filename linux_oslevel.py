#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux OS levels and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
import re
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import ping_server
django.setup()


def update_server():
    server_list = LinuxServer.objects.all()
    #FIXME quick way of testing a few servers
    #server_list = LinuxServer.objects.filter(name='d0mwcdb')
    #server_list = ['d1vio01', 'd1vio01']
    #server_list = LinuxServer.objects.filter(name__contains='vio')
    for server in server_list:
        #print server
        server_is_active=1

        if LinuxServer.objects.filter(name=server, active=True, exception=False):
            response = ping_server.ping(server)
            if response == 0:
                client = SSHClient()
                client.load_system_host_keys()

                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    #print 'SSH to ' + str(server) + ' failed, changing exception'
                    LinuxServer.objects.filter(name=server).update(exception=True, modified=timezone.now())
                    
                    #LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    server_is_active=0 

                if server_is_active:
                    command = 'lsb_release -a | grep Distributor'
                    stdin, stdout, stderr = client.exec_command(command)

                    #need rstrip() because there are extra characters at the end
                    os = stdout.readlines()[0].rstrip()
                    os = re.sub('Distributor ID:', '', os)
                    os = re.sub('\s*', '', os)


                    if os == 'RedHatEnterpriseServer':
                        os = 'RHEL'
                    else:
                        os = 'Unknown'


                    command = 'lsb_release -a | grep Release'
                    stdin, stdout, stderr = client.exec_command(command)

                    oslevel = stdout.readlines()[0].rstrip()
                    oslevel = re.sub('Release:', '', oslevel)
                    oslevel = re.sub('\s*', '', oslevel)

                    #check existing value, if it exists, don't update
                    if str(oslevel) != str(server.os_level) or str(os) != str(server.os):
                        LinuxServer.objects.filter(name=server, exception=False, active=True).update(os=os, os_level=oslevel, modified=timezone.now())
                        #pretty user the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                        change_message = 'Changed os_level to ' + +str(os) + ' ' + str(oslevel)
                        LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                        #FIXME - ok, we're going to create the manual log here, haven't worked it all out yet how I want to do it though
                        #We can do that or we can FK to the admin log...should we try to add our own columns?
                        #log = LinuxServer.objects.log(name=server 


            else:
                #print str(server) + ' not responding to ping, setting to inactive.'
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(active=False, modified=timezone.now())
                #FIXME I need a check here otherwise it isn't really a change, it's updating the same value
                LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')




#start execution
if __name__ == '__main__':
    print "Checking OS versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
