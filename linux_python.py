#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Python versions
#
# Boomer Rehfield - 7/8/2015
#
#########################################################################

import os
import re
from paramiko import SSHClient
from multiprocessing import Pool

# these are need in django 1.7 and needed vs the django settings command
from django.utils import timezone
import django

from server.models import LinuxServer
import utilities

django.setup()


def update_server(server):

    if utilities.ping(server):

        client = SSHClient()
        if utilities.ssh(server, client):
            print server.name
            command = 'python -V'
            stdin, stdout, stderr = client.exec_command(command)

            # https://bugs.python.org/issue18338
            # Apparently this is an old bug and only fixed in Python 3.4 and 2.7
            # where the version is sent to stderr

            try:
                version = stderr.readlines()[0].rstrip()
                version = re.sub('Python ', '', version)
            except:
                version = 'None'
            
            if version == 'None':
                try:
                    version = stdout.readlines()[0].rstrip()
                    version = re.sub('Python ', '', version)
                except:
                    version = 'None'

            print version

            # check existing value, if it exists, don't update
            if str(version) != str(server.python):
                utilities.log_change(server, 'python', str(server.python), str(version))

                LinuxServer.objects.filter(name=server).update(python=version, modified=timezone.now())
            client.close()


if __name__ == '__main__':
    print "Checking Python versions..."
    starting_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(10)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - starting_time
    print "Elapsed time: " + str(elapsed_time)
