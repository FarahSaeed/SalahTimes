from django.shortcuts import render
from django.http import  HttpResponse
from django.http import JsonResponse
from . import functionality
from datetime import date
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import datetime
import geonamescache
import json
import timezonefinder, pytz

def get_gmt_diff(lat, long):
    tf = timezonefinder.TimezoneFinder()
    # From the lat/long, get the tz-database-style time zone name (e.g. 'America/Vancouver') or None
    timezone_str = tf.certain_timezone_at(lat=lat, lng = long) #(lat=33.950001, lng=-83.383331)

    if timezone_str is None:
        print( "Could not determine the time zone")
    else:
        # Display the current time in that time zone
        timezone = pytz.timezone(timezone_str)
        dt = datetime.datetime.utcnow()
    #     print( "The time in %s is %s" % (timezone_str, dt + timezone.utcoffset(dt)) )
        gmt_diff = timezone.utcoffset(dt).total_seconds() / (60*60)
        print("gmt difference is: ", gmt_diff)
        return gmt_diff

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)

# Create your views here.

def home(request):
    countryList = []
    cityList = []

    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    cities = gc.get_cities()
  
    for country in countries:
        countryList.append(countries[country]['name'])

    for city in cities:
        cityList.append(cities[city]['name'])

    countryIndices = argsort(countryList)
    countryKeys = list(countries.keys())
    countryIndices = [ countryKeys[i] for i in countryIndices ]


    cityIndices = argsort(cityList)
    cityKeys = list(cities.keys())
    cityIndices = [ cityKeys[i] for i in cityIndices ]

    countryList = [countries[i]['name'] for i in countryIndices] #countryList = countryList[countryIndices]#sorted(countryList)

    cityList = [cities[i]['name'] for i in cityIndices]  #cityList = sorted(cityList)

    cityziplist = zip(cityList, cityIndices)
    countryziplist = zip(countryList, countryIndices)
    print(cityziplist)
    #countryList = ['Pakistan', 'United States', 'Palestine', 'Iran', 'Iraq']
    return render(request, 'home.html', {'name':'Navin', 'queryDate': datetime.date.today().strftime("%Y-%m-%d"), 'countryziplist': countryziplist,'cityziplist': cityziplist })


def add(request):

    num1 = int(request.GET['num1'])
    num2 = int(request.GET['num2'])
    val = num1 + num2
    return render(request, 'result.html', {'result':val})


def SalahTimes(request):
    from datetime import datetime, timedelta
    lat = request.GET['lat']
    long = request.GET['long']
    cityvalue = str(request.GET['cityvalue'])
    countryvalue = str(request.GET['countryvalue'])

    if cityvalue != '0' and countryvalue != '0':
        gc = geonamescache.GeonamesCache()
        cities = gc.get_cities()
        print(cities[cityvalue])
        lat = cities[cityvalue]['latitude']
        long = cities[cityvalue]['longitude']


    elif lat != '' and long != '':
        lat = float(lat)
        long = float(long)



    #timezone = int(request.GET['timezone'])
    print("###################", get_gmt_diff(lat, long) )
    timezone = get_gmt_diff(lat, long)
    dst = 0 #int(request.GET['dst'])

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

def load_cities(request):

    gc = geonamescache.GeonamesCache()

    cities = gc.get_cities()
    countryvalue = str(request.GET['country'])

    cityKeys = list(cities.keys())
    validcities = [ cities[i]['name']  for i in cityKeys if (cities[i]['countrycode'] == countryvalue) ]

    validcitieskeys = [ i  for i in cityKeys if (cities[i]['countrycode'] == countryvalue) ]

    #[cities[i]['name'] if cities['i']['countrycode'] == countryvalue for i in cityKeys]

    cityIndices = argsort(validcities)
    validcitieskeys = [ validcitieskeys[i] for i in cityIndices ]
    validcities = [ validcities[i] for i in cityIndices ]

    httpstr = ""
    for c in range(len(validcities)):
        httpstr = httpstr + '<option value=\"' + validcitieskeys[c] +'\">' + validcities[c] + '</option> \n'

    sresponse = HttpResponse("<p> changed!</p>")

    states = "" #"<p> value is not US </p>"
    if countryvalue == 'US':
        states = "Select state: <select id=\"state\" name=\"statevalue\" >"
         
        st = gc.get_us_states()
        for k,v in st.items():
            states = states + '<option value=\"' + v['code'] +'\">' + v['name'] + '</option> \n'
        states = states + "</select>"
    data = {'0':httpstr, '1': states}

    return JsonResponse(json.dumps({'cities': httpstr, 'states':  states }),safe=False)



    #return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse('<option value=\"2\">2</option>') #countryList = []
  
  
    for country in countries:
        countryList.append(countries[country]['name'])

    for city in cities:
        cityList.append(cities[city]['name'])

    countryIndices = argsort(countryList)
    cityIndices = argsort(cityList)
    cityKeys = list(cities.keys())

    cityIndices = [ cityKeys[i] for i in cityIndices ][:5]

    countryList = [countryList[i] for i in countryIndices] #countryList = countryList[countryIndices]#sorted(countryList)
    cityList = [cities[i]['name'] for i in cityIndices]  #cityList = sorted(cityList)

    cityziplist = zip(cityList, cityIndices)

    #countryList = ['Pakistan', 'United States', 'Palestine', 'Iran', 'Iraq']
    return render(request, 'home.html', {'name':'Navin', 'queryDate': datetime.date.today().strftime("%Y-%m-%d"), 'countryList': countryList, 'cityList': cityList, 'cityIndices': cityIndices, 'cityziplist': cityziplist })



def load_states(request):

    gc = geonamescache.GeonamesCache()

    cities = gc.get_cities()
    statevalue = str(request.GET['state'])

    cityKeys = list(cities.keys())
    validcities = [ cities[i]['name']  for i in cityKeys if (cities[i]['admin1code'] == statevalue) ]

    validcitieskeys = [ i  for i in cityKeys if (cities[i]['admin1code'] == statevalue) ]

    #[cities[i]['name'] if cities['i']['countrycode'] == countryvalue for i in cityKeys]

    cityIndices = argsort(validcities)
    validcitieskeys = [ validcitieskeys[i] for i in cityIndices ]
    validcities = [ validcities[i] for i in cityIndices ]

    httpstr = ""
    for c in range(len(validcities)):
        httpstr = httpstr + '<option value=\"' + validcitieskeys[c] +'\">' + validcities[c] + '</option> \n'

    sresponse = HttpResponse("<p> changed!</p>") #"<p> value is not US </p>"

    states = "" 
    #if countryvalue == 'US':
    #    states = "Select state: <select id=\"state\" name=\"statevalue\" >"
    #     
    #    st = gc.get_us_states()
    #    for k,v in st.items():
    #        states = states + '<option value=\"' + v['code'] +'\">' + v['name'] + '</option> \n'
    #    states = states + "</select>"
    data = {'0':httpstr, '1': states}

    return JsonResponse(json.dumps({'cities': httpstr}),safe=False)


