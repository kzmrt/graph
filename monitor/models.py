from django.db import models
from django.urls import reverse
from datetime import datetime as dt


class Location(models.Model):
    """場所モデル"""
    class Meta:
        db_table = 'location'

    name = models.CharField(verbose_name='ロケーション名', max_length=255)
    memo = models.CharField(verbose_name='メモ', max_length=255, default='', blank=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url(self):
        return reverse('monitor:index')


class WeatherData(models.Model):
    """気象データモデル"""
    class Meta:
        db_table = 'weather_data'
        unique_together = (('location', 'data_datetime'),)

    location = models.ForeignKey(Location, verbose_name='ロケーション', on_delete=models.PROTECT)
    data_datetime = models.DateTimeField(verbose_name='データ日時', default=dt.strptime('2001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
    temperature = models.FloatField(verbose_name='気温')
    humidity = models.FloatField(verbose_name='湿度')
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.location.name + ":" + str(self.data_datetime)