#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve bash versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os, re
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import LinuxServer
import test_server
django.setup()


def update_server():
    #server_list = LinuxServer.objects.all()
    #FIXME quick way of testing a few servers
    server_list = LinuxServer.objects.filter(name='ustsesbapp')
    #server_list = ['d1vio01', 'd1vio01']
    #server_list = LinuxServer.objects.filter(name__contains='vio')
    counter = 0
    for server in server_list:
        counter += 1
        print str(counter) + ' - ' + str(server)
        server_is_active=1

        if LinuxServer.objects.filter(name=server):

            if test_server.ping(server):

                client = SSHClient()
                client.load_system_host_keys()

                #redundant testing...ssh won't connect for some reason
                #server = str(server).rstrip()
                #print server
                #print len(server)
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    print 'SSH to ' + str(server) + ' failed, changing exception'
                    LinuxServer.objects.filter(name=server).update(exception=True, modified=timezone.now())
                    
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    server_is_active=0 

                if server_is_active:
                    command = 'sudo /sbin/fdisk -l | grep Disk'
                    stdin, stdout, stderr = client.exec_command(command)
                    print stdout
                    size = stdout.readlines()
                    for line in (size):
                        print line
                    print size
                    print 'Size' + str(size[1])
                    exit
                                     
                    bash_version = re.sub(r'x86_64', '', bash_version)

                    #check existing value, if it exists, don't update
                    if str(bash_version) != str(server.bash):
                        LinuxServer.objects.filter(name=server, exception=False, active=True).update(bash=bash_version, modified=timezone.now())
                        #pretty user the timestamp is auto created even though the table doesn't reflect it... maybe it's in the model
                        change_message = 'Changed bash version to ' + str(bash_version)
                        LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
                        #FIXME - ok, we're going to create the manual log here, haven't worked it all out yet how I want to do it though
                        #We can do that or we can FK to the admin log...should we try to add our own columns?
                        #log = LinuxServer.objects.log(name=server 



#start execution
if __name__ == '__main__':
    print "Checking Bash versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    elapsed_time = timezone.now() - starting_time 
    print "Elapsed time: " + str(elapsed_time)

