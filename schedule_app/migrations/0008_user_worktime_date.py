# Generated by Django 4.0.4 on 2023-10-07 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_app', '0007_alter_user_breaktime_break_in_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_worktime',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
