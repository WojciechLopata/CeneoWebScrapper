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
from app.models.sortable import table_maker
from flask import send_file
from wtforms import IntegerField, SubmitField,StringField
from wtforms.validators import DataRequired ,Length
from flask_wtf import FlaskForm
from flask_table import Table, Col

app.config["SECRET_KEY"]="Admin"
class SortableTable(Table):
    def __init__(self,product_id, items, classes=None, thead_classes=None, sort_by=None, sort_reverse=False, no_items=None, table_id=None, border=None, html_attrs=None):
        self.product_id=product_id
        super().__init__(items, classes, thead_classes, sort_by, sort_reverse, no_items, table_id, border, html_attrs)
    opinion_id = Col('ID')
    author = Col("author")
    recommendation = Col("recommendation")
    stars = Col("stars")
    content =Col(" content")
    useful =Col(" useful")
    useless =Col(" useless")
    publish_date = Col('publish_date')
    purchase_date = Col('purchase_date')
    pros =Col( 'pros')
    cons = Col('cons')
    allow_sort = True
    classes=["table table-bordered"]

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('product',product_id=self.product_id,direction=direction,sort=col_key)



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
@app.route("/product/delete-<product_id>")
def product_delete(product_id):
    os.remove(f"app/opinions/json/{product_id}.json")
    os.remove(f"app/opinions/csv/{product_id}.csv")
    os.remove(f"app/opinions/xlsx/{product_id}.xlsx")
    os.remove(f"app/static/plots/{product_id}_recommendations.png")
    os.remove(f"app/static/plots/{product_id}_stars.png")
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
    opinions = pd.read_json(f"app/opinions/json/{product_id}.json",orient='records')
    df = pd.DataFrame(opinions, columns=["opinion_id", "author", "recommendation","stars","content","useful","useless","publish_date","purchase_date","pros","cons"])

    sort = request.args.get('sort', 'opinion_id')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    df = df.sort_values(by=[sort], ascending=reverse)
    output_dict = df.to_dict(orient='records')

    table = SortableTable(product_id,output_dict,
                          sort_by=sort,
                          sort_reverse=reverse,)
    table= table.__html__()

    
    

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
