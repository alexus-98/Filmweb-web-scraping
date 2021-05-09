
import pandas as pd
import scrapy
import csv
import time

#creating empty dataframe with results
df = pd.DataFrame({'title': [], 'year': [], 'rate': [], 'votes': []})
i = 0
#path = 'C:\\Users\\Admin\\PycharmProjects\\SCRAPING\\filmweb_spider02\\filmweb_spider02\\spiders\\filmweb_spider02.py'
start = time.time()

#creating scrapy spider class
class filmwebspider(scrapy.Spider):
    name = 'filmweb_spider02'
    # allowed_domains = ['https://www.filmweb.pl/serials/search?orderBy=popularity&descending=true&page={}']
    start_urls = ['https://www.filmweb.pl/serials/search?orderBy=popularity&descending=true&page={}']

    def parse(self, response):
        global df, i,start
        quotes = response.xpath("//div[@class='filmPreview__card']")
        for quote in quotes:
            title = quote.xpath(
                ".//h2[@class='filmPreview__title']/text()").extract_first()
            year = quote.xpath(
                ".//div[@class='filmPreview__year']/text()").extract_first()
            rate = quote.xpath(
                ".//span[@class='rateBox__rate']/text()").extract_first()
            votes = quote.xpath(
                ".//span[@class='rateBox__votes rateBox__votes--count']/text()").extract_first()
            temp = {'title': title, "year": year, "rate": rate, "votes": votes}
            df = df.append(temp, ignore_index=True)
            yield temp

        next_page_url = response.xpath(
            "//li[@class='pagination__item pagination__item--next']//a/@href").extract_first()
        if next_page_url:
            print(i)
            i += 1
            absolute_next_page_url = response.urljoin(next_page_url)
            if i <= 99:
                yield scrapy.Request(absolute_next_page_url)
            else:
                #df.to_csv('my_output.csv')
                print(df)
                end = time.time()
                print(f"Runtime of the program is {end - start}")