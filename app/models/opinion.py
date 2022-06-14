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
        self.purchase_date=purchase_date
    def extract_opinion(self):
        for key,value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id=opinion["date-entry-id"]
        return self
    def __str__(self):
        str="autor"+self.author+"id"+self.id+"rekomendacja"+self.recomendation+"gwiazdki"+self.stars+"zalety"+self.pros+"wady"+self.cons+"data publikacji+self.publish_date+"data zakupu"+self.purchase_date
        return str
   
    def __repr__(self):
        return self.to_dict()
    def to_dict(self):
        return {"author": self.author,
        "id":self.opinion_id,
        "recomendation":self.recomenadtion,
        "stars":self.stars,
        "pros":self.pros,
        "cons":self.cons,
        "publish date":self.publish_date,
        "purchase date":self.purchase_date}
