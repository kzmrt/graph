# Generated by Django 2.1.4 on 2018-12-10 10:37

import datetime
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
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ロケーション名')),
                ('memo', models.CharField(blank=True, default='', max_length=255, verbose_name='メモ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_datetime', models.DateTimeField(default=datetime.datetime(2001, 1, 1, 0, 0), verbose_name='データ日時')),
                ('temperature', models.FloatField(verbose_name='気温')),
                ('humidity', models.FloatField(verbose_name='湿度')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='monitor.Location', verbose_name='ロケーション')),
            ],
            options={
                'db_table': 'weather_data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='weatherdata',
            unique_together={('location', 'data_datetime')},
        ),
    ]
