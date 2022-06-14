from app.models import opinion
from bs4 import BeautifulSoup
import requests
from app.utils import get_item
import os
import numpy as np
import pandas as pd 
import json
from app.models.opinion import Opinion
class Product():
    def __init__(self,product_id,opinions=[],product_name="",opinions_count=0,average_score=0,pros=[],cons=[]):
        self.product_id=product_id
        self.product_name=product_name
        self.opinions=opinions
        self.opinions_count=opinions_count
        self.average_score=average_score
        self.pros=pros
        self.cons=cons

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
        
                single_opinion = Opinion().extract_opinion(opinion)
                self.opinions.append(single_opinion)
            
            try:
                url="https://www.ceneo.pl"+page.select_one("a.pagination__next")["href"]
            except TypeError:
                url=None    
        return self
    def opinions_to_df(self):
        opinions=pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))
        opinions["stars"] = opinions["stars"].map(lambda x: float(str(x).split("/")[0].replace(",", ".")))
        return opinions
    def calculate_stats(self):
    
        opinions=self.opinions_to_df()
        opinions["stars"]=opinions["stars"].map(lambda x: float(str(x).split('/')[0].replace(",",".")))
        self.opinions_count=len(opinions),
        self.pros_count= opinions["pros"].map(bool).sum(),
        self.cons_count=opinions["cons"].map(bool).sum(),
        self.average_score=opinions["stars"].mean().round(2),
        return self
    def draw_charts(self): 
        opinions = self.opinions_to_df()
        recomendation=opinions["recomendation"].value_counts(dropna=False).sort_index().reindex("Nie polecam","polecam",None,fill_value=0)
        recomendation.plot.pie(
            label="", 
            autopct="%1.1f%%", 
            colors=["crimson", "forestgreen", "lightskyblue"],
            labels=["Nie polecam", "Polecam", "Nie mam zdania"]
        )
        plt.title("Rekomendacja")
        plt.savefig(f"app/static/plots/{self.product_id}_recommendations.png")
        plt.close()
        stars = self.opinions_do_df().stars.value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar()
        plt.title("Oceny produktu")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True)
        plt.xticks(rotation=0)
        plt.savefig(f"app/static/plots/{self.product_id}_stars.png")
        plt.close()


    def __str__(self):
        return f"""product_id: {self.product_id}<br>
        product_name: {self.product_name}<br>
        opinions_count: {self.opinions_count}<br>
        pros_count: {self.pros_count}<br>
        cons_count: {self.cons_count}<br>
        average_score: {self.average_score}<br>
        opinions: <br><br>
        """ + "<br><br>".join(str(opinion) for opinion in self.opinions)

    def __repr__(self):
                return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions_count={self.opinions_count}, pros_count={self.pros_count}, cons_count={self.cons_count}, average_score={self.average_score}, opinions: [" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }
    def opinions_to_dict(self):
        return

    def stats_to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score,
        }
    def export_opinions(self):
        
        if not (os.path.exists("app/opinions")):
            os.makedirs("app/opinions")
        with open(f"app/opinions/{product_id}.json","w",encoding="UTF-8") as file:
            json.dump([opinion.to_dict for opinion in self.opinions()],file,indent=4,ensure_ascii=False)
        pass
    def export_product(self):
        if not os.path.exists("app/products"):
            os.makedirs("app/products")
        with open(f"app/products/{self.product_id}.json") as file:
            json.dump(self.stats_to_dict)
    def import_product(self):
        if os.path.exists(f"app/products/{self.product_id}.json"):
            with open(f"app/products/{self.product_id}.json","r",encoding="UTF-8") as file:
                product=json.load(file)
                self.product_id=product_id
                self.product_name=product_name
                self.opinions=opinions
                self.opinions_count=opinions_count
                self.average_score=average_score
                self.pros=pros
                self.cons=cons
            with open(f"app/products/{self.product_id}.json","r",encoding="UTF-8") as file:
               opinion=json.load(file)
               for opinion in opinions:
                   self.opinions.append(Opinion(**opinion))
