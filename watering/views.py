from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from models import Branch
from temp_mon import *
# Create your views here.

def index1(request):
    return HttpResponse("Test")


def index(request):
    t = loader.get_template('watering/base_watering.html')

    temperatures = read_temp()
    devices = get_devices()
    dd = []
    for dev, temp in devices.iteritems():
        dd.append({'device': dev, 'temp': temp})
    branches = Branch.objects.all()
    c = Context({
        'title': 'This is my app. It uses Django templates',
        'result': branches,
        'temp_result': dd,
    })
    return HttpResponse(t.render(c))
