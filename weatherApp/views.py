from django.shortcuts import render
from time import gmtime, strftime
from timezonefinder import TimezoneFinder
import pytz
import datetime
# Create your views here.
import urllib.request
import json


def index(request):
  try:
     if request.method == 'POST' :
        city = request.POST['city']
        source =urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid=b5518a57096a518acd51de4cf79b08b3').read()
        list_of_data = json.loads(source)
        data1 = {
            "lat" :list_of_data['coord']['lat'],
            "lon" :list_of_data['coord']['lon'],
            "visibility" : str(list_of_data['visibility']/1000) + ' Km',
            "feels_like" : str(list_of_data['main']['feels_like'])+ ' °C',
            "temp_min" : str(list_of_data['main']['temp_min']) + ' °C',
            "temp_max" : str(list_of_data['main']['temp_max']) + ' °C',
            "wind_speed" : str(list_of_data['wind']['speed']),
            "wind_deg" : str(degrees_to_cardinal(list_of_data['wind']['deg'])),
            "time" : str(timeAt(list_of_data['coord']['lat'],list_of_data['coord']['lon'])),
            "city" : str(request.POST['city']),
            "country_code" : str(list_of_data['sys']['country']),
            "coordinate" : str(list_of_data['coord']['lon']) +', '
            + str(list_of_data['coord']['lat']),
            "temp" : str(list_of_data['main']['temp']) + ' °C',
            "pressure" : str(list_of_data['main']['pressure']),
            "humidity" : str(list_of_data['main']['humidity']),
            "main" : str(list_of_data['weather'][0]['main']),
            "description" : str(list_of_data['weather'][0]['description']),
            "icon" : list_of_data['weather'][0]['icon'],
          }
        sourse2 = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/forecast?lat='+str(list_of_data['coord']['lat'])+'&lon='+str(list_of_data['coord']['lon'])+'&units=metric&appid=b5518a57096a518acd51de4cf79b08b3').read()
        daily_data =json.loads(sourse2)
        daily_forecast1 = []
        for x in range(5):
            daily_forecast1.append({
                "Day": datetime.datetime.fromtimestamp(daily_data['list'][x*8]['dt']).strftime('%H:%M %A'),
                "max":"",
                "min":"",
                "pressure": str(daily_data['list'][x*8+4]['main']['pressure'])+ 'hPa',
                "humidity": str(daily_data['list'][x*8+5]['main']['humidity'])+'%',
                "main": daily_data['list'][x*8+5]['weather'][0]['main'],
                "description":  daily_data['list'][x*8+5]['weather'][0]['description'],
                "icon": daily_data['list'][x*8+5]['weather'][0]['icon'],
                "speed": str(daily_data['list'][x*8+5]['wind']['speed'])+'km/h',
                "deg": degrees_to_cardinal(daily_data['list'][x*8+5]['wind']['deg']),
                "gust": daily_data['list'][x*8+5]['wind']['gust'],
                "clouds": str(daily_data['list'][x*8+5]['clouds']['all'])+'%',  
            })
        onlytemp = []
        m=8
        n=-1
        maxtemp = [-273,-273,-273,-273,-273]
        mintemp = [1000,1000,1000,1000,1000]
        for i in range(40):
            onlytemp.append({
                "temp": int(daily_data['list'][i]['main']['temp']),
            })
            if i%m == 0:
                n=n+1
            if maxtemp[n]<onlytemp[i]['temp']:
              maxtemp[n]=max(maxtemp[n],onlytemp[i]['temp'])
            if mintemp[n]>onlytemp[i]['temp']:
              mintemp[n]=min(mintemp[n],onlytemp[i]['temp'])
        for x in range(5):
            daily_forecast1[x]['max'] = str(maxtemp[x]) + '°C',
            daily_forecast1[x]['min'] = str(mintemp[x]) + '°C',
        context = {
                "data": data1,
                "min": mintemp[0],
                "max": maxtemp[0],
                "daily_forecast": daily_forecast1,
          }
        return render(request, 'main/index.html',context)
     else:
        return render(request, 'main/index.html')
  except Exception as e:
      massage = {
          "sorry":"fgfhfd",
      }
      return render(request, 'main/index.html',massage)
def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]

def timeAt(latitude,longitude):

    tf = TimezoneFinder()

# Get the time zone for the given coordinates
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)

    if timezone_str:
    # Convert the timezone string to a pytz timezone object
        timezone = pytz.timezone(timezone_str)
 
    # Get the current time in the specified timezone
        current_time = pytz.datetime.datetime.now(timezone)
       
        return  current_time.strftime('%I:%M %p')
    else:
       return "Time zone not found for the given coordinates."