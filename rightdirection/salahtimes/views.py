from django.shortcuts import render
from django.http import  HttpResponse
from . import functionality
from datetime import date
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name':'Navin'})


def add(request):

    num1 = int(request.GET['num1'])
    num2 = int(request.GET['num2'])
    val = num1 + num2
    return render(request, 'result.html', {'result':val})


def SalahTimes(request):

    lat = float(request.GET['lat'])
    long = float(request.GET['long'])
    timezone = int(request.GET['timezone'])
    dst = int(request.GET['dst'])
    #dst = int(request.GET['is_day'])
    #is_week = int(request.GET['is_week'])
    #is_month = int(request.GET['is_month'])

    SalahDate = str(request.GET['SalahDate'])
    SalahDate = datetime.strptime(SalahDate,'%Y-%m-%d').date()
    prayTimes = functionality.PrayTimes()

 
    times = prayTimes.getTimes(SalahDate, (lat, long), timezone, dst); # date.today(), 33.9519, -83.3576, -5 1
    data = pd.DataFrame(times, index=[0]).to_html(index_names=False, escape=False)
 
    times_dict = defaultdict(list)

    d1 = {}
    if str(request.GET['choice']) == 'week':

        for i in range(7):
            times = prayTimes.getTimes(SalahDate+ timedelta(days=i), (lat, long), timezone, dst);
            times['date'] = SalahDate+ timedelta(days=i)

            for key, value in times.items():
                times_dict[key].append(value)

        data = pd.DataFrame(times_dict, index=list(range(7))).to_html(index_names=False, escape=False)


    elif str(request.GET['choice']) == 'month': #is_month == 1:

        for i in range(30):
            times = prayTimes.getTimes(SalahDate+ timedelta(days=i), (lat, long), timezone, dst);
            times['date'] = SalahDate+ timedelta(days=i)

            for key, value in times.items():
                times_dict[key].append(value)

        data = pd.DataFrame(times_dict, index=list(range(30))).to_html(index_names=False, escape=False)


    return render(request, 'result.html', {'result':data})

