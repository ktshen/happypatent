from django.contrib import admin

from .models import Agent, Patent, Proposal, FileAttachment, ControlEvent, Inventor


@admin.register(FileAttachment)
class FileAttachmentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Agent)
class AgentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Proposal)
class ProposalModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Inventor)
class InventorModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Patent)
class PatentModelAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'chinese_title', 'english_title', 'application_type')
    list_filter = ('application_type',)
    search_fields = ('chinese_title', 'english_title',)
    ordering = ['application_type']


@admin.register(ControlEvent)
class ControlEventModelAdmin(admin.ModelAdmin):
    pass
