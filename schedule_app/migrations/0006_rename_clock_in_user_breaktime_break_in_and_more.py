# Generated by Django 4.0.4 on 2023-09-21 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_app', '0005_alter_user_breaktime_user_alter_user_worktime_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_breaktime',
            old_name='clock_in',
            new_name='break_in',
        ),
        migrations.RenameField(
            model_name='user_breaktime',
            old_name='clock_out',
            new_name='break_out',
        ),
    ]