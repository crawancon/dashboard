#UNIX Dashboard views.py

from __future__ import division #But don't tell anyone, for the sake of the world.
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from server.models import AIXServer, LinuxServer, Relationships, HistoricalAIXData

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context

import datetime
     
def index(request):
    first_ten_servers = AIXServer.objects.order_by('name')[:10]
    context = {'first_ten_servers': first_ten_servers}
    return render(request, 'server/index.html', context)

def stacks(request):
    red_servers = AIXServer.objects.filter(stack__name = 'Red', decommissioned=False).order_by('name')
    yellow_servers = AIXServer.objects.filter(stack__name = 'Yellow', decommissioned=False).order_by('name')
    green_servers = AIXServer.objects.filter(stack__name = 'Green', decommissioned=False).order_by('name')
    orange_servers = AIXServer.objects.filter(stack__name = 'Orange', decommissioned=False).order_by('name')
    #server_list = AIXServer.objects.filter(stack__name ='Red')
    context = {'red_servers' : red_servers,
        'yellow_servers': yellow_servers,
        'green_servers': green_servers,
        'orange_servers': orange_servers}
    return render(request, 'server/stacks.html', context)


def wpars(request):
    context = RequestContext(request)
    relationship_list = Relationships.objects.all()
    context = {'relationships': relationship_list}
    return render(request, 'server/wpars.html', context)


#def pie(request):
#    red_servers = AIXServer.objects.filter(stack__name = 'Red').order_by('name')
#    context = {'red_servers' : red_servers}
#    return render(request, 'server/3d_pie.htm', context)

def pie_3d(request, string):
    request.GET.get('string')
    data = {}
    version_list = AIXServer.objects.filter(active=True, exception=False, decommissioned=False).values_list(string , flat=True).distinct()
    version_list = list(set(version_list))
    total_server_count = AIXServer.objects.filter(active=True, exception=False, decommissioned=False).count()
    for version in (version_list):
        if string == 'aix_ssh':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, aix_ssh=version).count()
            title = "Current distribution of AIX SSH on " + str(total_server_count) + " AIX servers"
        elif string == 'cent_ssh':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, cent_ssh=version).count()
            title = "Current distribution of Centrify SSH on " + str(total_server_count) + " AIX servers"
        elif string == 'os_level':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, os_level=version).count()
            title = "Current distribution of OS Level on " + str(total_server_count) + " AIX servers"
        elif string == 'centrify':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, centrify=version).count()
            title = "Current distribution of Centrify on " + str(total_server_count) + " AIX servers"
        elif string == 'xcelys':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, xcelys=version).count()
            title = "Current distribution of Xcelys on " + str(total_server_count) + " AIX servers"
        elif string == 'bash':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, bash=version).count()
            title = "Current distribution of Bash on " + str(total_server_count) + " AIX servers"
        elif string == 'ssl':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, ssl=version).count()
            title = "Current distribution of SSL on " + str(total_server_count) + " AIX servers"
        elif string == 'imperva':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, imperva=version).count()
            title = "Current distribution of Imperva on " + str(total_server_count) + " AIX servers"
        elif string == 'netbackup':
            num = AIXServer.objects.filter(active=True, exception=False, decommissioned=False, netbackup=version).count()
            title = "Current distribution of Netbackup on " + str(total_server_count) + " AIX servers"
        percentage = "{0:.1f}".format(num/total_server_count * 100)
        new_list = [str(version), percentage]
        data[version] = percentage

    name = "Percentage"
    return render(request, 'server/pie_3d.htm', {'data': data, 'name': name, 'title': title})


def stacked_column(request, string, string2):
    request.GET.get('string')
    request.GET.get('string2')
    data = {}


    title = "Historical distribution of OS Level on AIX servers by " + string2
    #total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=last_sunday).count()
    if string2 == 'week':
        #today = datetime.date.today().strftime('%Y-%m-%d')
        #I don't think I really need the total server count as the graph is dynamic
        #total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=today).count()

        #time_interval is the list of dates to gather data from, whether by day, week, month 
        time_interval = []
        #number_of_servers = []

        #interval is the offset for timedelta to get last sunday every week, every month or whatever
        interval = 1

        #Here we're going to get all of the versions of whatever software exist in a given date range.
        #FIXME last_sunday should be changed so we can pick specific weeks to view rather than starting from just last week
        last_sunday = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + 1))).strftime('%Y-%m-%d')
        first_date_in_range = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + 78))).strftime('%Y-%m-%d')
        version_list = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date__range=[first_date_in_range, last_sunday]).exclude(name__name__contains='vio').exclude(os_level='None').values_list(string , flat=True).distinct()
        version_list = list(set(version_list))


        #Populate time_interval with the dates for the labels and queries
        for x in range (0, 12):
            last_sunday = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval))).strftime('%Y-%m-%d')
            time_interval.append(last_sunday)
            interval = interval + 7


        #number_of_servers.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=last_sunday).count())
        #Ok, this is a bit different, we're going to have to iterate over the date and push the number of servers into a list across dates
        version_counter = 0
        date_counter = 0
        my_array = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
        #myarray = [[], [], [], [], [], []. [], [], [], [], [], [], [], []]
        for version in version_list:
            #FIXME - this os_level check needs to go somewhere else, but it's fine here for testing I guess, but it's needed more above
            #if string == 'os_level':
            for date in time_interval:
                num = HistoricalAIXData.objects.filter(active=True, exception=False, decommissioned=False, os_level=version, date=date).count()
                if version_counter == 0:
                    my_array[version_counter][date_counter] = [num]
                else:
                    my_array[version_counter].append(num)
                date_counter += 1
            version_counter += 1

        time_interval.reverse()
        #number_of_servers.reverse()

        
    name = "Test Name"
    y_axis_title = 'Number of Servers'
    #percentage = "{0:.1f}".format(num/total_server_count * 100)
    #new_list = [str(version), percentage]
    percentage = 0
    data[version] = percentage
    return render(request, 'server/stacked_column.htm', {'data': data, 'name': name, 'title': title, 'y_axis_title':y_axis_title, 'version_list':version_list, 'time_interval':time_interval, 'my_array':my_array})



def line_basic(request, string, string2):
    request.GET.get('string')
    request.GET.get('string2')
    data = {}
    #rather than /aix/week we could change this and make it something like /total_servers/all /total_servers/linux
    #we could branch this out as well like /aix_versions/linux

    #Not filtering exceptions as they are active servers and we need a total count
    #we need the total_server_count from last sunday, which is representative of the day before, saturday, the end of last
    #week when the chart starts. (starts...i.e. the first date on the chart on the right side)
    last_sunday = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + 1))).strftime('%Y-%m-%d')
    total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=last_sunday).count()

    name = "Test Name"
    title = "Number Of Active AIX Servers - Last 12 weeks"

    #for now, we're just going to replace the data as I figure out what I'm doing with this view
    if string2 == 'week':
        #timestamp = timezone.localtime(now).strftime('%Y-%m-%d')
        today = datetime.date.today().strftime('%Y-%m-%d')
        #months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', today]
        total_server_count = HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=today).count()

        
        months = []
        number_of_servers = []
        number_of_decoms = []
        number_of_prod = []
        number_of_non_prod = []
        interval = 1
        for x in range (0, 12):
            ls = (datetime.date.today() - datetime.timedelta(days = (datetime.date.today().weekday() + interval))).strftime('%Y-%m-%d')
            months.append(ls)
            interval = interval + 7

            number_of_servers.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, date=ls).count())
            number_of_decoms.append(HistoricalAIXData.objects.filter(decommissioned=True, date=ls).count())
            number_of_prod.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone_id=2 , date=ls).count())
            number_of_non_prod.append(HistoricalAIXData.objects.filter(active=True, decommissioned=False, zone=1 , date=ls).count())

        months.reverse()
        number_of_servers.reverse()
        number_of_decoms.reverse() 
        number_of_prod.reverse()
        number_of_non_prod.reverse()

    return render(request, 'server/line_basic.htm', {'data': data, 'months': months, 'number_of_servers': number_of_servers, 'number_of_decoms': number_of_decoms, 'number_of_prod': number_of_prod, 'number_of_non_prod': number_of_non_prod, 'name': name, 'title': title, 'total_server_count': total_server_count})



def detail(request, aixserver_name):
    #try:
    #    server = AIXServer.objects.get(pk=aixserver_name)
    #except:
    #    raise Http404
    server = get_object_or_404(AIXServer, pk=aixserver_name)
    frame = get_object_or_404(AIXServer, pk=aixserver_name).frame
    frame_short_name = str(frame)[:3] + '-' + str(frame)[-5:]
    return render(request, 'server/detail.html', {'server': server, 'frame_short_name': frame_short_name})



def linux_server_detail(request, server_linuxserver_id):
    return HttpResponse("Looking at linux server detail for %s." % server_linuxserver_id)

# Create your views here.
