# Generated by Django 4.1.3 on 2022-11-29 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='status',
            field=models.CharField(choices=[('r', 'running'), ('b', 'broke')], default='r', max_length=1),
        ),
    ]
