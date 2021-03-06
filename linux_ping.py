#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to ping sweep decommed servers
#
# Boomer Rehfield - 10/03/2015
#
#########################################################################

import os
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
import django
from django.utils import timezone

from server.models import LinuxServer
import utilities

django.setup()

# This line is set in my profile but putting it here so others can run the scripts
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'


def update_server(server):

    # Examples of how you can filter servers
    # server_list = LinuxServer.objects.all()
    # server_list = LinuxServer.objects.filter(decommissioned=False, zone=2) #zone 1= non prod, zone 2 = prod
    # server_list = LinuxServer.objects.filter(name__contains='hdp')
    # server_list = LinuxServer.objects.filter(name='p1rhrep')
    # server_list = LinuxServer.objects.filter(decommissioned=False, active=False)  #only ping sweep ones nailed as inactive

    # You can run this against AIX servers as well from here
    # aix_server_list = AIXServer.objects.filter(decommissioned=False)

    # Run two filters (change one to server_list2 or whaterver)
    # server_list = list(chain(aix_server_list, server_list))

    # switch out the below two lines to only ping the first twenty servers
    # in the database
    # for server in server_list[:20]:

    # print str(counter) + ' - ' + str(server)
    print server.name
    if utilities.ping(server):
        print "good"
    else:
        print "no ping"


if __name__ == '__main__':
    print "Performing ping sweep..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(10)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
