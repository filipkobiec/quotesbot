import datetime
import json
import os
import jsonlines
import scrapy

DICT = {
    'https://weather.com/pl-PL/pogoda/10dni/l/e5137ad59d68e86155f4cf59f3f44bb5e7bfe3b64adb102d1e81c677e3bb3ec3': 'cracow',
    'https://weather.com/pl-PL/pogoda/10dni/l/90936a42cebbd51867bdaeddac9ffaf9163a3fb51304b94da5358538a6ec36bf': 'warsow',
}

class QuotesSpider(scrapy.Spider):
    name = "google"
    
    start_urls = [
        'https://weather.com/pl-PL/pogoda/10dni/l/e5137ad59d68e86155f4cf59f3f44bb5e7bfe3b64adb102d1e81c677e3bb3ec3',
        'https://weather.com/pl-PL/pogoda/10dni/l/90936a42cebbd51867bdaeddac9ffaf9163a3fb51304b94da5358538a6ec36bf'
    ]


    def parse(self, response):
        currentDate = datetime.date.today()
        values = []
        fileName =  DICT[response.url] + '.jsonl'

        for i, forecast in enumerate(response.css('details.DaypartDetails--DayPartDetail--2XOOV')):
            date = currentDate + datetime.timedelta(days=i)
            tempStr = forecast.css('span.DetailsSummary--highTempValue--3PjlX::text').get().replace('°', '')
            temp = int(tempStr)
            lowTemp = int(forecast.css('span.DetailsSummary--lowTempValue--2tesQ::text').get().replace('°', ''))
            cloudyValue = forecast.css('.DetailsSummary--extendedData--307Ax::text').get()
            rain = int(forecast.css('span.DailyContent--value--1Jers::text').get().replace('%', ''))
            values.append({
                    'date': date,
                    'temp': temp,
                    'lowTemp': lowTemp,
                    'cloudyValue': cloudyValue,
                    'rain': rain
                })
        with jsonlines.open(os.path.join('data/google', fileName), "a") as writer:
            writer.write(json.dumps({
            'currentDate': currentDate,
            'values': values
            }, default=str, ensure_ascii=False))
        
