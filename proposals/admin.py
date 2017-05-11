from django.contrib import admin

from .models import Employee, Agent, ContactPerson, Client,  Patent, Work, ContactPerson
from .models import Test1, Test2
# Register your models here.




@admin.register(Agent)
class AgentModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactPerson)
class ContactPersonModelAdmin(admin.ModelAdmin):
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
    list_display = ('case_id', 'chinese_title', 'english_title', 'client_type',
                    'control_item', 'control_date', 'deadline')
    list_filter = ('control_item', 'client_type')
    search_fields = ('chinese_title', 'english_title',)
    date_hierarchy = 'deadline'
    ordering = ['deadline', 'control_item', 'client_type']


@admin.register(Test1)
class Test1ModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Test2)
class Test2ModelAdmin(admin.ModelAdmin):
    pass


