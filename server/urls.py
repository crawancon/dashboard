# UNIX Dashboard urls.py

from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^jquerytest/$', views.jquerytest, name='jquerytest'),

    url(r'^stacks/(?P<os>(.*)+)/(?P<zone>(.*)+)$', views.stacks, name='stacks'),
    url(r'^stacks/(?P<os>(.*)+)/(?P<zone>(.*)+)/$', views.stacks, name='stacks'),


    url(r'^frames$', views.frames, name='frames'),
    url(r'^frames/$', views.frames, name='frames'),
    url(r'^wpars$', views.wpars, name='wpars'),
    url(r'^wpars/$', views.wpars, name='wpars'),
    url(r'^java$', views.java, name='java'),
    url(r'^java/$', views.java, name='java'),

    url(r'^local_users.txt$', views.local_users, name='local_users'),
    url(r'^local_users.txt/$', views.local_users, name='local_users'),
    #url(r'^pie_ssh/$', views.pie_ssh, name='pie_ssh'),
    #url(r'^3d_pie/aix_ssh|cent_ssh/$', views.pie_ssh, name='pie_ssh'),

    url(r'^pie_3d/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)$', views.pie_3d, name='pie_3d'),

    url(r'^stacked_column/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.stacked_column, name='stacked_column'),

    #quick one off to get total number of servers
    url(r'^stacked_column_total/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.stacked_column_total, name='stacked_column_total'),


    #url(r'^stacked_column/(?P<os>(.*)+)/(?P<zone>(.*)+)/(?P<service>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)/$', views.stacked_column, name='stacked_column'),


    url(r'^line_basic/(?P<os>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.line_basic, name='line_basic'),
    url(r'^line_basic/(?P<os>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)/$', views.line_basic, name='line_basic'),


    url(r'^column_basic_proc_pools/(?P<frame>(.*)+)/(?P<pool_name>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)$', views.column_basic_proc_pools, name='column_basic_proc_pools'),
    url(r'^column_basic_proc_pools/(?P<frame>(.*)+)/(?P<pool_name>(.*)+)/(?P<period>(.*)+)/(?P<time_range>(.*)+)/$', views.column_basic_proc_pools, name='column_basic_proc_pools'),

    #treemap view of the AIX affinity values
    url(r'^treemap/$', views.treemap, name='treemap'),
    url(r'^treemap$', views.treemap, name='treemap'),


    url(r'^(?P<aixserver_name>(.*)+)/$', views.detail, name='detail'),

    #Git statistics for the dashboard
    url(r'^git_stats_dashboard$', views.git_stats_dashboard, name='git_stats_dashboard'),
    url(r'^git_stats_dashboard/$', views.git_stats_dashboard, name='git_stats_dashboard'),

    #Git statistics for ansible-dev
    url(r'^git_stats_ansible_dev$', views.git_stats_ansible_dev, name='git_stats_ansible_dev'),
    url(r'^git_stats_ansible_dev/$', views.git_stats_ansible_dev, name='git_stats_ansible_dev'),

    #Testing area

    #Testing dataTables with django
    url(r'^aix_server_table$', views.aix_server_table, name='aix_server_table'),
    url(r'^aix_server_table/$', views.aix_server_table, name='aix_server_table'),

)
