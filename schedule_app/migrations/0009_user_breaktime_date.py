# Generated by Django 4.0.4 on 2023-10-11 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_app', '0008_user_worktime_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_breaktime',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
