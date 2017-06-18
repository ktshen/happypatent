# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-18 05:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import happypatent.users.utils
import proposals.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
                ('agent_id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name="Agent's ID")),
                ('agent_title', models.CharField(max_length=50, unique=True, verbose_name="Agent's title")),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Address')),
                ('beneficiary_name', models.CharField(blank=True, max_length=50, verbose_name='Beneficiary Name')),
                ('remittance_bank', models.CharField(blank=True, max_length=50, verbose_name='Remittance Bank')),
                ('beneficiary_no', models.CharField(blank=True, max_length=50, verbose_name='Beneficiary A/C No.')),
                ('contact_person_name', models.CharField(blank=True, max_length=30, verbose_name="Contact Person's Name")),
                ('contact_person_phone_number', models.CharField(blank=True, max_length=50, verbose_name="Contact Person's Phone Number")),
                ('contact_person_email', models.EmailField(blank=True, max_length=254, verbose_name="Contact Person's Email")),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
                ('client_id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name="Client's ID")),
                ('abbr_client', models.CharField(max_length=30, verbose_name="Client's name in abbreviated form")),
                ('client_ch_name', models.CharField(max_length=50, verbose_name='Client Chinese name')),
                ('client_en_name', models.CharField(max_length=50, verbose_name='Client English name')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('post_address', models.CharField(max_length=100, verbose_name='Post Office Address')),
                ('english_address', models.CharField(blank=True, max_length=100, verbose_name='English Address')),
                ('invoice_address', models.CharField(blank=True, max_length=100, verbose_name='Invoice(Application form) address')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Phone Number')),
                ('fax_number', models.CharField(blank=True, max_length=50, verbose_name='Fax Number')),
                ('contact_person_name', models.CharField(blank=True, max_length=30, verbose_name="Contact Person's Name")),
                ('contact_person_title', models.CharField(blank=True, max_length=30, verbose_name="Contact Person's Title")),
                ('contact_person_phone_number', models.CharField(blank=True, max_length=50, verbose_name="Contact Person's Phone Number")),
                ('contact_person_email', models.EmailField(blank=True, max_length=254, verbose_name="Contact Person's Email")),
                ('repr_chinese_name', models.CharField(max_length=50, verbose_name="Representative's Chinese name")),
                ('repr_english_name', models.CharField(max_length=50, verbose_name="Representative's English name")),
                ('vat_no', models.CharField(blank=True, max_length=30, verbose_name='VAT No.')),
                ('number_employee', models.CharField(blank=True, choices=[('above', 'Above 500 employees'), ('under', 'Under 500 employees')], max_length=30, verbose_name='Number of employees')),
                ('primary_owner', models.CharField(max_length=50, verbose_name='Primary owner')),
                ('secondary_owner', models.CharField(blank=True, max_length=50, verbose_name='Secondary owner')),
                ('status', models.CharField(blank=True, max_length=30, verbose_name='Status')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'Applicant',
                'verbose_name_plural': 'Applicants',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(blank=True, max_length=10, verbose_name='ID Number')),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=10, verbose_name='Gender')),
                ('county', models.CharField(blank=True, max_length=30, verbose_name='County/City')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Address')),
                ('home_number', models.CharField(blank=True, max_length=15, verbose_name='Home Number')),
                ('mobile_number', models.CharField(blank=True, max_length=15, verbose_name='Mobile Number')),
                ('office_number', models.CharField(blank=True, max_length=15, verbose_name='Office Number')),
                ('spouse_name', models.CharField(blank=True, max_length=50, verbose_name='Spouse Name')),
                ('education', models.TextField(blank=True, verbose_name='Education')),
                ('experience', models.TextField(blank=True, verbose_name='Experience')),
                ('profile_pic', models.ImageField(blank=True, upload_to='photos/', validators=[happypatent.users.utils.image_validate], verbose_name='Profile Picture')),
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
                ('chinese_name', models.CharField(max_length=30, verbose_name='Chinese Name')),
                ('english_name', models.CharField(max_length=30, verbose_name='English Name')),
                ('email', models.EmailField(max_length=254)),
                ('engagement_date', models.DateField(default=django.utils.timezone.now, verbose_name='Engagement Date')),
                ('title_id', models.CharField(blank=True, choices=[('0', '---------'), ('1', 'CEO'), ('2', 'Director'), ('3', 'Manager'), ('4', 'Senior Engineer'), ('5', 'Engineer')], default='0', max_length=30, verbose_name='Title ID')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('employer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='proposals.Client', verbose_name='Employer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=proposals.utils.get_upload_path)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
                ('case_id', models.CharField(max_length=30, unique=True, verbose_name='Case ID')),
                ('chinese_title', models.CharField(max_length=100, verbose_name='Chinese Title')),
                ('english_title', models.CharField(max_length=100, verbose_name='English Title')),
                ('application_type', models.CharField(blank=True, choices=[('0', '---------'), ('invention', 'Invention'), ('utility', 'Utility'), ('design', 'Design')], default='0', max_length=30, verbose_name='Type')),
                ('country', models.CharField(choices=[('TW', 'TW'), ('US', 'US'), ('CN', 'CN'), ('JP', 'JP'), ('KR', 'KR'), ('EP', 'EP'), ('GB', 'GB'), ('DE', 'DE'), ('FR', 'FR')], max_length=30, verbose_name='Country')),
                ('request_examination', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=30, verbose_name='Request Examination')),
                ('examination_date', models.DateField(blank=True, null=True, verbose_name='Date of request examination')),
                ('case_status', models.CharField(blank=True, choices=[('0', '---------'), ('1', 'Draft/Translation'), ('2', 'Preliminary examination'), ('3', 'Response/Amendment-1'), ('4', 'Response/amendment-2'), ('5', 'Rejection'), ('6', 'Publication'), ('7', 'Re-examination'), ('8', 'Appeal'), ('9', 'Re-appeal'), ('10', 'Administrative litigation'), ('11', 'Paying issue fee'), ('12', 'Patent allowed'), ('13', 'Client abandon'), ('14', 'Invalidation examination')], default='0', max_length=30, verbose_name='Status')),
                ('filing_date', models.DateField(blank=True, null=True, verbose_name='Filing Date')),
                ('application_no', models.CharField(blank=True, max_length=30, verbose_name='Application No.')),
                ('publication_date', models.DateField(blank=True, null=True, verbose_name='Publication Date')),
                ('publication_no', models.CharField(blank=True, max_length=30, verbose_name='Publication No.')),
                ('patent_date', models.DateField(blank=True, null=True, verbose_name='Date of patent')),
                ('patent_no', models.CharField(blank=True, max_length=30, verbose_name='Patent No.')),
                ('patent_term', models.DateField(blank=True, null=True, verbose_name='Patent Term.')),
                ('certificate_no', models.CharField(blank=True, max_length=30, verbose_name='Certificate No.')),
                ('pre_decision_date', models.DateField(blank=True, null=True, verbose_name='Date of preliminary decision')),
                ('pre_decision_no', models.CharField(blank=True, max_length=30, verbose_name='Preliminary decision No.')),
                ('re_examine_date', models.DateField(blank=True, null=True, verbose_name='Date of re-examination')),
                ('control_item', models.CharField(blank=True, choices=[('0', '---------'), ('1', 'File new application'), ('2', 'File Chinese description'), ('3', 'Request examination'), ('4', 'File patent invalidation'), ('5', 'File re-examination'), ('6', 'File amendment'), ('7', 'File response'), ('8', 'Pay issue fee'), ('9', 'Pay maintenance fee'), ('10', 'Pay annuity fee'), ('11', 'File appeal'), ('12', 'File re-appeal'), ('13', 'File administrative litigation'), ('14', 'Other')], default='0', max_length=30, verbose_name='Control Item')),
                ('control_date', models.DateField(blank=True, null=True, verbose_name='Control Date')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Deadline')),
                ('description_pages', models.IntegerField(blank=True, null=True, verbose_name='Number of description pages')),
                ('drawing_pages', models.IntegerField(blank=True, null=True, verbose_name='Number of drawing pages')),
                ('figures_number', models.IntegerField(blank=True, null=True, verbose_name='Number of figures')),
                ('owner', models.CharField(blank=True, max_length=50, verbose_name='Owner')),
                ('priority', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=30, verbose_name='Priority')),
                ('prio_country', models.CharField(blank=True, choices=[('TW', 'TW'), ('US', 'US'), ('CN', 'CN'), ('JP', 'JP'), ('KR', 'KR'), ('EP', 'EP'), ('GB', 'GB'), ('DE', 'DE'), ('FR', 'FR')], max_length=30, verbose_name='(Priority) Country')),
                ('prio_application_no', models.CharField(blank=True, max_length=30, verbose_name='(Priority) Application No.')),
                ('prio_filing_date', models.DateField(blank=True, null=True, verbose_name='(Priority) Filing Date')),
                ('file_holder_position', models.CharField(blank=True, max_length=100, verbose_name='File-holder position')),
                ('IDS_infomation', models.CharField(blank=True, max_length=100, verbose_name='IDS Information')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proposals.Client')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('foreign_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patent_foreign_agent', to='proposals.Agent')),
                ('inventor', models.ManyToManyField(blank=True, to='proposals.Employee', verbose_name='Inventor')),
                ('local_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patent_local_agent', to='proposals.Agent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
                ('work_id', models.CharField(max_length=30, unique=True, verbose_name='Work ID')),
                ('case_id', models.CharField(max_length=30, verbose_name='Case ID')),
                ('person_charge', models.CharField(max_length=50, verbose_name='Person in charge')),
                ('work_type_id', models.CharField(choices=[('1', 'File new application'), ('2', 'File document'), ('3', 'Request examination'), ('4', 'File patent invalidation'), ('5', 'File re-examination'), ('6', 'File amendment'), ('7', 'File response'), ('8', 'Pay issue fee'), ('9', 'Pay maintenance fee'), ('10', 'Pay annuity fee'), ('11', 'File appeal'), ('12', 'File re-appeal'), ('13', 'File administrative litigation'), ('14', 'Other')], default='1', max_length=50, verbose_name='Work Type ID')),
                ('work_stage_id', models.CharField(max_length=30, verbose_name='Work Stage ID')),
                ('control_deadline', models.DateField(verbose_name='Control Deadline')),
                ('distribution_deadline', models.DateField(blank=True, null=True, verbose_name='Distribution Deadline')),
                ('control_person', models.CharField(blank=True, max_length=50, verbose_name='Control Person')),
                ('distributor', models.CharField(blank=True, max_length=50, verbose_name='Distributor')),
                ('status', models.CharField(blank=True, max_length=50, verbose_name='Status')),
                ('closed_case', models.BooleanField(default=False, verbose_name='Closed Case')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
