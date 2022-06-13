from app.models import opinion
from BeautifulSoup import bs4
import requests
from app.routes import product
from app.utils import get_item
import os
import numpy as np
import pandas as pd 
import json
class Product():
    def __init__(self,product_id,opinions=[],product_name="",opinions_count=0,average_score=0,pros=[],cons=[]):
        self.product_id=product_id
        self.product_name=product_name
        self.opinions=opinions
        self.opinions_count=opinions_count
        self.average_score=average_score
        self.pros=pros
        self.cons=cons
        return self
    def extract_name(self):
        url=f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        response= requests.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
        self.product_name=get_item(page,"h1.product-top__product-info__name")
        return self

    def extract_opinions(self):
        url=f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        all_opinions=[]
        while(url):
    
            response= requests.get(url)
            page = BeautifulSoup(response.text, 'html.parser')
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
        
                single_opinion=Opinion().extract_opinion(opinion)
                self.opinions.append(single_opinion)
            
            try:
                url="https://www.ceneo.pl"+page.select_one("a.pagination__next")["href"]
            except TypeError:
                url=None    
        return self
    def opinions_to_df(self):
        return pd.read_json(jsons.dumps([opinion.to_dict() for opinion in self.opinions]))
    def calculate_stats(self):
    
        opinions=opinions_to_df()
        opinions["stars"]=opinions["stars"].map(lambda x: float(x.split('/')[0].replace(",",".")))
        self.opinions_count=len(opinions),
        self.pros_count= opinions["pros"].map(bool).sum(),
        self.cons_count=opinions["cons"].map(bool).sum(),
        self.average_score=opinions["stars"].mean().round(2),
        return self
    def draw_charts(self):

        if not os.path.exists("app/plots"):
            os.makedirs("app/plots")
        recomendation=opinions["recomendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam","Polecam",None],fill_value=0)
        recomendation.plot.pie(
            label="",
            autopct=lambda p: '{:.1f}%'.format(round(p)) if p>0 else "",
            colors=["crimson","forestgreen","lightskyblue"],
            labels=["Nie polecam","Polecam","Nie mam zdania"]
        )
        plt.title("Rekomendacje")
        plt.savefig(f"app/static/plots/{product_id}_recomendation.png")
        plt.close()
        stars=opinions["stars"].value_counts().reindex(list(np.arange(0,5.5,0.5)),fill_value=0)
        stars.plot.bar(
        color="pink"

        )
        plt.title("oceny produktu")
        plt.xlabel("liczba gwiazdek")
        plt.ylabel("liczba opinii")
        plt.grid(True,axis="y")
        plt.xticks(rotation=0)
        plt.savefig(f"app/plots/{product_id}_stars.png")
        plt.close()            
        return self
    def __str__(self):
        obiekt=self.product_name+self.product_id+self.average_score
        return obiekt
    def __repr__(self):
        return self.to_dict()
    def to_dict(self):
        return {"author": self.author,
        "recomendation":self.recomenadtion,
        "average score":self.average_score,
        "pros":self.pros,
        "cons":self.cons,}
    def export_opinions(self):
        
        if not (os.path.exists("app/opinions")):
            os.makedirs("app/opinions")
        with open(f"app/opinions/{product_id}.json","w",encoding="UTF-8") as file:
            json.dump([opinion.to_dict for opinion in self.opinions()],file,indent=4,ensure_ascii=False)
        pass
    def export_product(self):
        pass