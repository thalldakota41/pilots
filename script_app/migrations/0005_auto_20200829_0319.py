# Generated by Django 2.2 on 2020-08-29 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_app', '0004_auto_20200827_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='poster',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='posters'),
        ),
    ]
