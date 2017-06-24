from django.contrib import admin

from .models import Employee, Agent, Client,  Patent, Work, FileAttachment, ControlEvent


@admin.register(FileAttachment)
class FileAttachmentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Agent)
class AgentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    date_hierarchy  = 'update'
    list_display    = ('client_ch_name', 'client_en_name', 'country',
                        'status', 'created', 'update',)
    list_filter     = ('country', 'status', 'created', 'update',)
    ordering        = ('client_id', 'created', 'update', 'client_ch_name',)


@admin.register(Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    date_hierarchy  = 'update'
    list_display    = ('pk','chinese_name', 'english_name', 'employee_id', 'gender', 'created')
    list_filter     = ('created', 'update',)
    ordering        = ('created', 'update', 'chinese_name', 'english_name')
    search_fields   = ('chinese_name', 'english_name', 'employee_id')


@admin.register(Patent)
class PatentModelAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'chinese_title', 'english_title', 'application_type')
    list_filter = ('application_type',)
    search_fields = ('chinese_title', 'english_title',)
    ordering = ['application_type']


@admin.register(ControlEvent)
class ControlEventModelAdmin(admin.ModelAdmin):
    pass
