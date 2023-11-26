# Generated by Django 4.0.4 on 2023-10-29 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_app', '0011_user_schedule_end_time_user_schedule_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_schedule',
            name='department',
            field=models.CharField(choices=[('P', 'Pharmacist'), ('R', 'Retail'), ('O', 'Office'), ('F', 'Filling'), ('D', 'Dispatch'), ('D/F', 'Dispatch/Filling'), ('C', 'Compounding'), ('DME', 'DME Driver'), ('DE', 'Data Entry'), ('W', 'Warehouse')], default='P', max_length=3),
        ),
    ]