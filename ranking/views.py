from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from ranking.models import Client

# Create your views here.


def upload(request):
    cli = request.POST.get("cli")
    score = request.POST.get("score")
    client = Client.objects.filter(cli=cli)
    if client:
        client = client[0]
        client.score = score
        client.save()
    else:
        Client.objects.create(cli=cli, score=score)

    return JsonResponse({"errno":0, "message":"ok"})


def get_list(request):
    page_num = request.GET.get("page")
    per_page = request.GET.get("rows")
    cli = request.GET.get("cli")
    pagn = Paginator(Client.objects.all().order_by("-score"),per_page=per_page)
    data = list(pagn.get_page(page_num))
    sort_data = []
    start = (int(page_num)-1)*int(per_page)
    i = 1
    for client in data:
        sort_data.append({"cli":client.cli, "score":client.score, "sort_num": start+i})
        i += 1
    cur_cli = Client.objects.get(cli=cli)
    cur_no = len(Client.objects.filter(score__gt=cur_cli.score))
    sort_data.append({"cli":cli, "score":cur_cli.score, "sort_num":cur_no+1})
    result = {
        "count":len(sort_data),
        "page":page_num,
        "data": sort_data
    }

    return JsonResponse(result)
