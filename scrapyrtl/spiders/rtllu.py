import scrapy
from ..items import ArticleItem, MostReadItem
import unicodedata
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from datetime import datetime
from pprint import pprint

###
#   Author: Ries Christian
#   Description: Crawl every news article that is found on 
#   rtl.lu/news/national then save data to mongo db collection
##
class rtlluSpider(scrapy.Spider):
    name = 'rtllu'
    # dont leave our target
    allowed_domains = ['rtl.lu']
    # define where we want to start crawling
    start_urls = ['https://www.rtl.lu/news/national']

    # let's start crawling
    def parse(self, response):
        # go through every link found on the page
        for link in response.css('a.block-link__overlay::attr(href)'):
            url = link.extract()
            # only crawl national news articles
            if "news/national/a" in url:
                yield response.follow(link.get(), callback=self.parse_article)

    # Parse news articles info incl. most read articles
    def parse_article(self, response):
        # get metainfo from site (authors and timestamp)
        metainfo = response.css('.article-heading__metainfo::text').getall()
        meta_stripped = list(map(str.strip, metainfo))

        # only look at articles with date (ex. Liveticker has no date)
        if len(meta_stripped) > 0:
            # and also dont look at articles without authors
            if meta_stripped[0]:
                # get article url
                url = response.request.url
                # extract article id from url 
                id = os.path.basename(url).split('.')[0]

                # collect meta info (authors, date)
                meta = response.css('div.article-heading__metainfo')
                # collect full title from head meta info
                ogtitle = response.xpath("//meta[@property='og:title']/@content")[0]

                # kicker & main title
                kicker = ogtitle.extract().split(':')[0].strip()
                title = ogtitle.extract().split(':')[1].strip()
               
                # Split authors into an array and strip unpleasant string "Vum "
                authors = meta_stripped[0].strip('Vum ').split(', ')

                # Get the article date
                if "Update:" in meta_stripped[1]:
                    dt = meta_stripped[1].strip('Update: ')
                else:
                    dt = meta_stripped[1]

                # convert to datetime object (from: dd.mm.YYYY HH:MM)
                timestamp = datetime.strptime(dt, '%d.%m.%Y %H:%M')

                # Get article text by paragraphs and join together
                body = ""
                paragraphs = response.css('.article-body__detail p ::text').getall()
                for p in paragraphs:
                    body += p.strip() + " "

                # utf8 encoding
                body = unicodedata.normalize("NFKD", body)

                most_read = []
                # get most read articles in sidebar
                mr_articles = response.css('div.card.card--most-read-aside')
                for mr_article in mr_articles:
                    url = mr_article.css('a::attr(href)').extract_first()
                    # Build most read article item and insert to list
                    most_read.append(MostReadItem(
                        _id = os.path.basename(url).split('.')[0],
                        title = mr_article.css('span.card__title::text').get(),
                        kicker = mr_article.css('span.card__kicker::text').get(),
                        url = url
                    ))

                # Build article item
                article = ArticleItem(
                    _id = id,
                    title = title,
                    kicker = kicker,
                    timestamp = timestamp,
                    authors = authors,
                    text = body,
                    url = url,
                    most_read = most_read
                )

                return article

class todayrtllu(scrapy.Spider):
    name = "todayrtllu"
    # dont leave our target
    allowed_domains = ['rtl.lu']
    # define where we want to start crawling
    start_urls = ['https://today.rtl.lu/news/luxembourg']
    
        


       