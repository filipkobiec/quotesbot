import datetime
import json
import os
import jsonlines
import scrapy

DICT = {
    'https://pogoda.interia.pl/prognoza-dlugoterminowa-krakow,cId,4970': 'cracow',
    'https://pogoda.interia.pl/prognoza-dlugoterminowa-warszawa,cId,36917': 'warsow',
}

class QuotesSpider(scrapy.Spider):
    name = "interia"
    
    start_urls = [
        'https://pogoda.interia.pl/prognoza-dlugoterminowa-krakow,cId,4970',
        'https://pogoda.interia.pl/prognoza-dlugoterminowa-warszawa,cId,36917'
    ]


    def parse(self, response):
        currentDate = datetime.date.today()
        values = []
        fileName =  DICT[response.url] + '.jsonl'

        for i, forecast in enumerate(response.css('.weather-forecast-longterm-list-entry')):
            date = currentDate + datetime.timedelta(days=i)
            temp = int(forecast.css('span.weather-forecast-longterm-list-entry-forecast-temp::text').get().replace('°C', ''))
            lowTemp = int(forecast.css('span.weather-forecast-longterm-list-entry-forecast-lowtemp::text').get().replace('°C', ''))
            cloudyValue = int(forecast.css('span.weather-forecast-longterm-list-entry-cloudy-cloudy-value::text').get())
            weatherValues = forecast.css('span.weather-forecast-longterm-list-entry-precipitation-value::text').getall()
            rain = float(weatherValues[0].replace(',', '.'))
            if (len(weatherValues) < 2): snowValue = 0.0
            else: snowValue = float(weatherValues[1].replace(',', '.'))
            values.append({
                    'date': date,
                    'temp': temp,
                    'lowTemp': lowTemp,
                    'cloudyValue': cloudyValue,
                    'rain': rain,
                    'snow': snowValue
                })
        with jsonlines.open(os.path.join('data/interia', fileName), "a") as writer:
            writer.write(json.dumps({
            'currentDate': currentDate,
            'values': values
            }, default=str))
        
