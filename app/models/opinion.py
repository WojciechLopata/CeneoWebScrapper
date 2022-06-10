from app.parameters import selectors
from app.models import opinion
from BeautifulSoup import bs4
import requests
from app.utils import get_item
import os
import numpy as np
import pandas as pd 
import json
class Opinion():
    def __init__(self,opinion_id,author="",recomenadtion=None,stars=0,content="",useful=0,useless=0,publish_date=None,purchase_date=None,pros=[],cons=[]):
        self.author=author
        self.recomenadtion=recomenadtion
        self.stars=stars
        self.useful=useful
        self.useless=useless
        self.publish_date=publish_date
        self.pros=pros
        self.cons=cons
        self.publish_date=purchase_date
        self.opinion_id=opinion_id
    def extract_opinion(self):
        for key,value in selectors.items():
            setattr(self,key,key:get item(opinion, *value))
        self.opinion_id=opinion["date-entry-id"]
        return self
    def __str__(self):
        pass
    def __repr__(self):
        pass
    def to_dict(self):
        pass