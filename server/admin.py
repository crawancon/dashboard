from django.contrib import admin
from server.models import AIXServer, LinuxServer, Errpt, VIOServer, Power7Inventory, Zone, Storage
#from server.models import CapacityPlanning
from django.contrib.admin.models import LogEntry

# Register your models here.


class AIXServerAdmin(admin.ModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'frame', 'ip_address', 'zone', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    list_filter = ['frame', 'os', 'os_level', 'zone', 'active', 'exception', 'centrify', 'xcelys', 'bash', 'ssl']
    search_fields = ['name', 'frame', 'ip_address', 'os', 'os_level', 'zone', 'centrify', 'xcelys', 'bash', 'ssl']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'frame', 'active', 'exception', 'created', 'modified', 'zone', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl', 'java', 'log']

class LinuxServerAdmin(admin.ModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ['name', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'ssl']
    list_filter = ['os', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'ssl']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys','ssl']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'ssl', 'java', 'log']



#testing the proxy model
class VIOServerAdmin(admin.ModelAdmin):
    pass
    def queryset(self, request):
        return self.model.objects.filter(name__contains='vio')
    save_on_top = True
    list_display = ['name', 'frame', 'active','exception', 'modified', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    list_filter = ['frame', 'os', 'os_level', 'active', 'exception', 'centrify', 'xcelys', 'bash', 'ssl']
    search_fields = ['name', 'os', 'os_level', 'centrify', 'xcelys', 'bash', 'ssl']
    readonly_fields = ['created', 'modified']
    fields = ['name', 'frame', 'active', 'exception', 'created', 'modified', 'ip_address', 'os', 'os_level', 'centrify', 'xcelys', 'bash','ssl', 'java', 'log']

class Power7InventoryAdmin(admin.ModelAdmin):
    list_max_show_all = 500
    save_on_top = True
    list_display = ('name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    list_filter = ('curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    search_fields = ('name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'curr_mem', 'curr_max_mem')
    #fields = ('name', 'lpar_id', 'curr_shared_proc_pool_name', 'curr_min_proc_units', 'curr_proc_units', 'curr_max_proc_units', 'curr_min_mem', 'cur_mem', 'max_mem')





class LogEntryAdmin(admin.ModelAdmin):
    """Creating an admin view of the Django contrib auto admin history/log table thingy"""
    #note the loss of _id on user_id and content_type_id in the list display
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_time', 'user_id', 'content_type_id')
    search_fields = ('action_time', 'user_id', 'content_type_id', 'object_repr', 'action_flag', 'change_message')
    save_on_top = True
    fields = ('action_time', 'user_id', 'content_type_id', 'object_repr', 'action_flag', 'change_message')
    order = ('-action_time')
    def has_add_permissions(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        #returning false causes table to gray out in the admin page for some reason
        return True

class ErrptAdmin(admin.ModelAdmin):
    list_display = ['name', 'modified', 'report']

class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name',]

class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']

#class CapacityPlanningAdmin(admin.ModelAdmin):
#    list_display = ('name', 'os', 'ip_address', 'curr_procs', 'curr_mem', 'storage', 'database_name')
#    list_filter = ('name', 'os', 'ip_address', 'curr_procs', 'curr_mem', 'storage', 'database_name')
#    search_fields = ('name', 'os', 'ip_address', 'curr_procs', 'curr_mem', 'storage', 'database_name')
#    save_on_top = True
#    fields = ('name', 'os', 'ip_address', 'curr_procs', 'curr_mem', 'storage', 'database_name')


admin.site.register(AIXServer, AIXServerAdmin)
admin.site.register(LinuxServer, LinuxServerAdmin)
admin.site.register(VIOServer, VIOServerAdmin)
admin.site.register(Power7Inventory, Power7InventoryAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Errpt, ErrptAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Storage, StorageAdmin)
#admin.site.register(CapacityPlanning, CapacityPlanningAdmin)
