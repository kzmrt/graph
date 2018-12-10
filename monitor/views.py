from django.http import HttpResponse
from django.views import generic
from .models import Location, WeatherData
from django.contrib.auth.mixins import LoginRequiredMixin
import io
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger('development')


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Location
    paginate_by = 5
    ordering = ['-updated_at']
    template_name = 'monitor/index.html'


class DetailView(generic.DetailView):
    model = Location
    template_name = 'monitor/detail.html'


# グラフ作成
def setPlt(pk):
    # 折れ線グラフを出力

    weather_data = WeatherData.objects.select_related('location').filter(location_id=pk)  # 対象ロケーションの気象データを取得
    x = [data.data_datetime for data in weather_data] # 日時
    y1 = [data.temperature for data in weather_data] # 気温
    y2 = [data.humidity for data in weather_data]  # 湿度
    plt.plot(x, y1, x, y2)


# svgへの変換
def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


def get_svg(request, pk):
    setPlt(pk)  # create the plot
    svg = pltToSvg()  # convert plot to SVG
    plt.cla()  # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response