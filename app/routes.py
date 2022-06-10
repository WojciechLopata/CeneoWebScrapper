from app import app
from flask import render_template,redirect,url_for,request
import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd
from matplotlib import colors, pyplot as plt
from app.models.product import Product

selectors={
            "author":["span.user-post__author-name"],
            "recomendation":["span.user-post__author-recomendation > em"],
            "stars":["span.user-post__score-count"],
            "content":["div.user-post__text"],
            "usefull":["button.vote-yes > span"],
            "useless":["button.vote-no > span"],
            "published":["span.user-post__published > time:nth-child(1)","datetime"],
            "purchased":["span.user-post__published > time:nth-child(2)","datetime"],
            "pros":["div[class$=positives] ~ div.review-feature__item",None,True],
            "cons":["div[class$=negatives] ~ div.review-feature__item",None,True]

}
@app.route('/')
def index():
    return render_template("index.html.jinja")
@app.route("/autor")
def autor():
    return render_template("autor.html.jinja")
@app.route("/extraction",methods=["POST","GET"])
def extraction():
    if not request.method == "POST" :
        return render_template ("extract.html.jinja")
    product_id=request.form.get("product_id")
    product=Product(product_id)
    product.extract_name()
    if(product.product_name):
        product.extract_opinions().calculate_stats().draw_charts()
    else: 
        pass
    
    if not (os.path.exists("app/opinions")):
        os.makedirs("app/opinions")

    ##print(author,recomendation,opinion_id,stars,content,usefull,useless,published,purchased,sep="\n")
    with open(f"app/opinions/{product_id}.json","w",encoding="UTF-8") as file:
        json.dump(all_opinions,file,indent=4,ensure_ascii=False)
    return redirect (url_for("product",product_id=product_id))
@app.route("/products")
def products():
    products=[filename.split(".")[0] for filename in os.listdir("app/opinions")]
    return render_template ("products.html.jinja",products=products)
@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html.jinja", product_id=product_id,opinions=opinions)