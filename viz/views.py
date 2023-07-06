import json
from random import randrange

from adrf.views import APIView
from django.http import HttpResponse
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts.chart import RectChart
from pyecharts_snapshot.main import make_a_snapshot


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def chart_base() -> RectChart:
    c = (
        Line()
        .add_xaxis(["python", "node", "java", "c#", "scala", "Rust"])
        .add_yaxis("like", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("dislike", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Chart", subtitle="Subtitle"))
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(chart_base().dump_options_with_quotes()))


class DownloadView(APIView):
    async def get(self, request, *args, **kwargs):
        response = await self.generate_chart()
        response['Content-Disposition'] = 'attachment; filename="chart.png"'
        return response

    async def generate_chart(self):
        chart_ = chart_base()
        chart_.render("snapshot.html")
        image_file_name = "snapshot.png"
        await make_a_snapshot("snapshot.html", image_file_name)
        # await make_snapshot(snapshot, "snapshot.html", image_file_name)
        with open(image_file_name, "rb") as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/png")

    # async def make_graph(self, file):
    #     await make_a_snapshot("tmp.html", "tmp.png")


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index.html").read())
