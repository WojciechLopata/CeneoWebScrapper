from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for
import json

"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)


class SortableTable(Table):
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

    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


@app.route('/')
def index():
    sort = request.args.get('sort', 'opinion_id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(sort, reverse),
                          sort_by=sort,
                          sort_reverse=reverse)
    return table.__html__()


@app.route('/item/<int:id>')
def flask_link(id):
    element = Item.get_element_by_id(id)
    return '<h1>{}</h1><p>{}</p><hr><small>id: {}</small>'.format(
        element.opinion_id, element.author, element.recommendation,element.stars,element.content,element.useful,element.useless,element.publish_date,element.purchase_date,element.pros,element.cons)


class Item(object):
    """ a little fake database """
    def __init__(self, author="", recommendation=None, stars=0, content="", useful=0, useless=0, publish_date=None, purchase_date=None, pros=[], cons=[], opinion_id=""):
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.publish_date = publish_date
        self.purchase_date = purchase_date
        self.pros = pros
        self.cons = cons
        self.opinion_id= opinion_id

    @classmethod
    def get_elements(cls):
        with open(f"app/opinions/json/96827995.json", "r", encoding="UTF-8") as jf:
            items = json.load(jf)
       # print(items)
        return items
    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        print(sort)
        print("get_sorte_by")
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, opinion_id):
        print("get_elemment_by")
        return [i for i in cls.get_elements() if i.opinions_id == opinion_id][0]

if __name__ == '__main__':
    app.run(debug=True)

