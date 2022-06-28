from math import prod
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
from wtforms import IntegerField, SubmitField,StringField
from wtforms.validators import DataRequired ,Length
from flask_wtf import FlaskForm

app.config["SECRET_KEY"]="Admin"


# Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("Podaj ID produktu ", validators=[DataRequired(),Length(max=11,min=6,message="Id które podałeś jest niepoprawne, Spróbuj ponownie")])
	submit = SubmitField("Podaj")



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

@app.route('/extraction', methods=['GET', 'POST'])
def extraction():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        product=Product(name)
        product.extract_name()
        if(product.product_name):
            if not product.extract_opinions().calculate_stats():
                return render_template("extract.html.jinja",
                name = name,
		        form = form,
                error="Produkt nie ma opinii")
            product.extract_opinions().calculate_stats().draw_charts()
            product.export_opinions()
            product.export_product()
        else:
            return render_template("extract.html.jinja",
            name = name,
		    form = form,
            error="Podaj poprawne id")
        return redirect (url_for("product",product_id=name))
    return render_template("extract.html.jinja", 
		name = name,
		form = form)
    
@app.route("/products")
def products():
    products=[filename.split(".")[0] for filename in os.listdir("app/opinions/json")]
    stats={}

    for product in products:
        id=product
        product=Product(product)
        product.import_product()
        stats[id]=(product.list_helper())

    return render_template ("products.html.jinja",products=products,stats=stats)
@app.route('/product/<product_id>')
def product(product_id):
    product=Product(product_id)
    product.import_product()
    stats=product.stats_to_dict()
    opinions=product.opinions_to_df()
    table=table_maker(product_id)
    

    return render_template("product.html.jinja", product_id=product_id,table=table)
@app.route('/download/<product>.<format>')    
def download (format,product):
    path="opinions/"+format+'/'+product+"."+format
    return send_file(path,as_attachment=True)
@app.route("/test")
def test():
    return send_file("opinions/csv/96827995.csv")
@app.route("/chart<product_id>")
def charts(product_id):
    return render_template("charts.html.jinja",product_id=product_id)
