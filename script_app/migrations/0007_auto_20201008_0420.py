# Generated by Django 3.1.2 on 2020-10-08 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('script_app', '0006_auto_20200829_0445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pilot',
            options={'ordering': ['created_at']},
        ),
    ]
