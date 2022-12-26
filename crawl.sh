#!/usr/bin/bash
source /home/pi/Desktop/quotesbot/tutorial-env/bin/activate
cd /home/pi/Desktop/quotesbot
scrapy crawl google
scrapy crawl interia
deactivate