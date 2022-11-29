# Generated by Django 4.1.3 on 2022-11-29 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('broke_date', models.DateTimeField(blank=True, null=True)),
                ('x', models.IntegerField(default=100)),
                ('y', models.IntegerField(default=100)),
                ('z', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Instructions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('axis', models.CharField(max_length=1)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='space_api.station')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
