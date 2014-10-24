#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to storage size of each of the servers
#
# Boomer Rehfield - 10/24/2014
#
#########################################################################

import os
from ssh import SSHClient
from django.utils import timezone
from django.contrib.admin.models import LogEntry
#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Storage
import ping_server
django.setup()



def update_server():
    #right now we are just getting these for the VIO servers
    #server_list = AIXServer.objects.filter(name__contains='auto').exclude(name__contains='vio')
    server_list = AIXServer.objects.all().exclude(name__contains='vio')
    #FIXME need to exclude vio servers
    #server_list = AIXServer.objects.filter(name__contains='p1vio01')
    counter  = 1
    for server in server_list:
        server_is_active=1

        #Make sure the server is set to active and not an exception
        if AIXServer.objects.filter(name=server, active=True, exception=False):
            response = ping_server.ping(server)
            
            #typically = is false, but that's what ping gives back for a positive
            if response == 0:
                client = SSHClient()
                client.load_system_host_keys()

                #without try, it will break the script if it can't SSH
                try:
                    client.connect(str(server), username="wrehfiel")
                except:
                    print 'SSH to ' + str(server) + ' failed, changing exception'
                    AIXServer.objects.filter(name=server).update(exception=True, modified=timezone.now())

                    #LogEntry.objects.create(action_time='2014-08-25 20:00:00', user_id=11, content_type_id=9, object_id =264, object_repr=server, action
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='SSH failed, changed exception.')
                    continue 


                stdin, stdout, stderr = client.exec_command('sudo /scripts/disksize_dashboard.sh')
                #stdin, stdout, stderr = client.exec_command('ls /')

                #we have to do errpt differently due to the way it is handled by stdout
                print '======================'
                print str(counter) + ' - '  + str(server)
                for line in stdout:
                    print line.rstrip()
                
                counter += 1
                try:
                    Storage.objects.get(name=server)
                    Storage.objects.filter(name=server).update(size=line.rstrip())
                except:
                    Storage.objects.get_or_create(name=server, size=line.rstrip())

                #    print '1'
                #except:
                #    print '2'
                #if report == '':
                #    report = "The errpt was empty."
              
                #let's get the PK for the server
                #server_name = AIXServer.objects.get(name=server)
                #we don't care about the old record and we'll just overwrite it
                #Errpt.objects.get_or_create(name=server, report=report, modified=timezone.now())
                #change_message = 'Updated errpt.'
                #LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id=264, object_repr=server, action_flag=2, change_message=change_message)
            else:
                AIXServer.objects.filter(name=server).update(active=False)
                print str(server) + ' not responding to ping, setting to inactive.'
                AIXServer.objects.filter(name=server, exception=False, active=True).update(modified=timezone.now())
                LogEntry.objects.create(action_time=timezone.now(), user_id=11, content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message='Ping failed, changed to inactive.')




#start execution
if __name__ == '__main__':
    print "Storage size for each server..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    from server.models import AIXServer
    update_server()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)