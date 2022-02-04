# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from datetime import datetime
import scrapy


@dataclass
class ArticleItem:
    # define the fields of a news article
    _id: str
    title: str
    kicker: str
    timestamp: datetime
    authors: str
    text: str
    url: str
    most_read: list

@dataclass
class MostReadItem:
    # define the fields of a news article
    _id: str
    title: str
    kicker: str
    url: str