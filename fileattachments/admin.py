from django.contrib import admin
from .models import FileAttachment


@admin.register(FileAttachment)
class FileAttachmentModelAdmin(admin.ModelAdmin):
    pass

