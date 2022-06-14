from app.parameters import selectors
from app.models import opinion
from bs4 import BeautifulSoup
import requests
from app.utils import get_item
import os
import numpy as np
import pandas as pd 
import json
class Opinion():
    def __init__(self,opinion_id=0,author="",recomenadtion=None,stars="",content="",useful=0,useless=0,publish_date=None,purchase_date=None,pros=[],cons=[]):
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
    def extract_opinion(self,opinion):
        for key,value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id=opinion["data-entry-id"]
        return self
    def __str__(self):
        return f"opinion_id: {self.opinion_id}<br>" + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in selectors.keys())
    def __repr__(self):
        return f"Opinion(opinion_id={self.opinion_id}, " + ", ".join(f"{key}={str(getattr(self, key))}" for key in selectors.keys()) + ")"
    def to_dict(self):
        return {"author": self.author,
        "id":self.opinion_id,
        "recomendation":self.recomenadtion,
        "stars":self.stars,
        "pros":self.pros,
        "cons":self.cons,
        "publish date":self.publish_date,
        "purchase date":self.purchase_date}
