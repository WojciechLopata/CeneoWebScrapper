from app import app
from flask import render_template,redirect,url_for,request
import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd
from matplotlib import colors, pyplot as plt
from app.models.product import Product
from app.models.simple import table_maker
from flask import send_file


selectors={
            "author":["span.user-post__author-name"],
            "recommdation":["span.user-post__author-recomendation > em"],
            "stars":["span.user-post__score-count"],
            "content":["div.user-post__text"],
            "useful":["button.vote-yes > span"],
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
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product(product_id)
        product.extract_name()
        if product.product_name:
            product.extract_opinions().calculate_stats()

            product.extract_opinions().calculate_stats().draw_charts()
            product.export_opinions()
            product.export_product()
        else:
            error = "Ups... coś poszło nie tak"
            return render_template("extract.html.jinja", error=error)
        return redirect(url_for('product', product_id=product_id))
    else:
        return render_template("extract.html.jinja")
@app.route("/products")
def products():
    products=[filename.split(".")[0] for filename in os.listdir("app/opinions/json")]
    stats={}
    print(products)
    for product in products:
        id=product
        product=Product(product)
        product.import_product()
        stats[id]=(product.list_helper())

    print(stats)

    return render_template ("products.html.jinja",products=products,stats=stats)
@app.route('/product/<product_id>')
def product(product_id):
    product=Product(product_id)
    product.import_product()
    stats=product.stats_to_dict()
    opinions=product.opinions_to_df()
    table=table_maker(product_id)
    print(stats)

    return render_template("product.html.jinja", product_id=product_id,table=table)
@app.route('/download/<product>.<format>')    
def download (path,product,format):
    path=path+product+"."+format
    print(path)
    #For windows you need to use drive name [ex: F:/Example.pdf]
    return send_file(path,as_attachment=True)