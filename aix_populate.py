#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Django server database population script
# This will
#   -Go to the HMC and pull all frames
#   -Read all Lpar names from each frame
#   -test to see if it is active
#   -test ssh connectivity
#   -check for wpars
#   -check each wpars status and ssh connectivity
#   -update the server database accordingly for each step
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

import os, sys
from ssh import SSHClient
#import paramiko
import utilities
from django.utils import timezone
from subprocess import call, check_output


from django.contrib.admin.models import LogEntry

#these are need in django 1.7 and needed vs the django settings command
import django
from dashboard import settings
from server.models import AIXServer, Zone, Frame, Stack, Relationships
#import logging
django.setup()

#logging.basicConfig( level=logging.INFO )

def populate():

    f = open("../../.ssh/p", "r")

    #need rstrip to strip off the newline at the end
    password = str(f.read().rstrip())
    f.close()
    #do I need a ping test for p1hmc?? lol
    client = SSHClient()
    client.load_system_host_keys()

    try:
        client.connect('phmc01', username="wrehfiel", password=password)
        hmc = 'phmc01'
    except:
        print 'SSH to phmc01 has failed!'
        print '*************HAVE YOU CHANGED YOUR PASSWORD RECENTLY??***********'
        print 'Trying phmc02........'
        try:
            client.connect('phmc02', username="wrehfiel", password=password)
            hmc = 'phmc02'
        except:
            print 'SSH to phmc02 has failed!'
            print '*************HAVE YOU CHANGED YOUR PASSWORD RECENTLY??***********'
            print "Cannot contact either HMC, ABORTING."
            sys.exit()
    
    stdin, stdout, stderr = client.exec_command('lssyscfg -r sys -F name')
    #frames = stdout.readlines()[0]
    frames = stdout.readlines()
    print "Frames:"
    print frames
    #frames = ['795A-9119-FHB-SN023D965']
    frames = ['824A-8286-42A-SN21950BV']

    for frame in frames:

        #rstrip() worked on the old HMC's but not the new ones??
        frame = frame.splitlines()
        frame = ''.join(frame)

        #If the frame doesn't exist, create it
        Frame.objects.get_or_create(name=frame)
        frame = Frame.objects.get(name=frame)

        #load ssh keys
        #client = paramiko.SSHClient()
        client = SSHClient()
        client.load_system_host_keys()


        #we've already established a connection, but should put in error checking
        #FIXME needs error checking
        client.connect(hmc , username="wrehfiel", password=password)

        #for each frame, let's grab the LPARS now
        command = 'lssyscfg -m ' + str(frame) + ' -r lpar -F name'
        #print command
        sdtin, stdout, stderr = client.exec_command(command)
        server_list = stdout.readlines()
        client.close()
        
        counter = 0

        for server_name in server_list:
            #FIXME server is being stupid and just not responding and it's causing an ssh auth error somehow renaming the key, needs error checking!
            server_name = server_name.rstrip()
            update = 0
            counter += 1
            #for troubleshooting - please leave
            #print str(counter) + " - " + frame + ' -> ' + server.rstrip()


            #Before we ping and do our other tests we're going to get the ip address from
            #nslookup. If this fails it will simply return a blank.
             
            ns_command = 'nslookup ' + server_name + ' | grep Address | grep -v "#" '
            try:
                ip_address = check_output(ns_command, shell=True)
                ip_address = ip_address[9:]
            except:
                ip_address = '0.0.0.0'

            zone = Zone.objects.get(name='Unsure')


            try:
                print "==============="
                print server_name
                server = AIXServer.objects.get(name=server_name)
                print '1'
                print server.frame
                print frame
                print "frame id"
                print frame.id
                if server.frame != frame:
                    #AIXserver.objects.filter(name=server).update(frame=frame.id)
                    print '2'
                    server.frame = frame
                    print '2.5'
                    server.save()
                    #server.update(frame=frame.id)
                    print '3'
                    test = "test"
                    print '4'
                    change_message = "Changed frame for " + str(server_name) + " from " + str(server.frame) + " to " + str(frame.name)
                    print '4'
                    LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=2, change_message=change_message)
                    print '5'
            except:
                print "---------"
                print frame.name
                print len(frame.name)
                print len(str(frame))
                print server.frame
                print len(str(server.frame))
                print len(str(server.frame))
                print server_name.rstrip()
                print len(server_name.rstrip())
                #the created object is not the same, so we create it and then get the instance
                #setting exception to True so the ssh keys script will pick it up and transfer keys
                server = AIXServer.objects.get_or_create(name=str(server_name).rstrip(), frame=frame, ip_address=ip_address, os='AIX', zone=zone, active=True, exception=True,  stack_id=1)
                server = AIXServer.objects.get(name=server_name.rstrip())
                change_message = "Added LPAR " + server_name.rstrip() + "."
                LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=1, change_message=change_message)
            

            if utilities.ping(server):

                print "ping good" 
                client2 = SSHClient()


                if utilities.ssh(server, client2):
                    #Check for wpars here
                    print "Check for wpars here"
                    command = "dzdo lswpar | grep -v WPAR | grep -v -"
                    stdin, stdout, stderr = client2.exec_command(command)
                    print server
                    #print 'stdout - ' + str(stdout)
                    #FIXME we can do an 'if stderr' mail ....
                    #print 'stderr - ' + str(stderr)
                    for line in stderr:
                        print line
                    #wpar_list = stdout.readlines()[0].rstrip()
                    wpar_list = stdout.readlines()
                    if wpar_list:
                        print '-------------------'
                        for wpar in wpar_list:
                            t= wpar.split()
                            wpar_name = t[3].rstrip()
                            print wpar_name
                            
                            ns_command = 'nslookup ' + wpar_name + ' | grep Address | grep -v "#" '

                            try:
                                ip_address = check_output(ns_command, shell=True)
                                ip_address = ip_address[9:].rstrip()
                            except:
                                ip_address = '0.0.0.0'


                            #We have all of our information for the wpar, let's put it in the database
                            try:
                                temp = AIXServer.objects.get(name=wpar_name)
                            except:
                                #Here we are inheriting some of the parent LPAR objects into the WPAR
                                temp = AIXServer.objects.get_or_create(name=wpar_name, owner=server.owner, frame=server.frame, ip_address=ip_address, os='AIX', zone=server.zone, active=True, exception=True,  stack=server.stack)
                                change_message = "Added WPAR " + wpar_name + "."
                                LogEntry.objects.create(action_time=timezone.now(), user_id=11 ,content_type_id=9, object_id =264, object_repr=server, action_flag=1, change_message=change_message)

                            #Now we'll try and check if the LPAR<->WPAR relationship exists, or create it
                            try:
                                Relationships.objects.get(parent_lpar=server_name, child_wpar=wpar_name)
                            except:
                                child_wpar = AIXServer.objects.get(name=wpar_name)
                                Relationships.objects.get_or_create(parent_lpar=server, child_wpar=child_wpar)
                            

                            
                    else:
                        print "No wpars."

                            
                client2.close()




#start execution
if __name__ == '__main__':
    print "Starting populations..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    populate()
    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)




