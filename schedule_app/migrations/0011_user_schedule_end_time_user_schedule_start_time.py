# Generated by Django 4.0.4 on 2023-10-27 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_app', '0010_merge_0009_user_breaktime_date_0009_user_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_schedule',
            name='end_time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user_schedule',
            name='start_time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]