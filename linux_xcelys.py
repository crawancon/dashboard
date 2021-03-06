#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to retrieve Linux Xcelys versions and drop them into Django dashboard
#
# Boomer Rehfield - 11/13/2014
#
#########################################################################

import os
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

            stdin, stdout, stderr = client.exec_command('[ -f /opt/xcelys/version ] && cat /opt/xcelys/version || echo "None"')
            xcelys_version = stdout.readlines()[0].rstrip()

            print server.name + " - " + xcelys_version
            if xcelys_version != "None":
                xcelys_version = xcelys_version[36:-16]

            print server.name + " - " + xcelys_version
            if str(xcelys_version) != str(server.xcelys):
                utilities.log_change(server, 'Xcelys', str(server.xcelys), str(xcelys_version))
                LinuxServer.objects.filter(name=server, exception=False, active=True).update(xcelys=xcelys_version, modified=timezone.now())


if __name__ == '__main__':
    print "Checking Xcelys versions..."
    start_time = timezone.now()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

    server_list = LinuxServer.objects.filter(decommissioned=False)

    pool = Pool(10)
    pool.map(update_server, server_list)

    elapsed_time = timezone.now() - start_time
    print "Elapsed time: " + str(elapsed_time)
