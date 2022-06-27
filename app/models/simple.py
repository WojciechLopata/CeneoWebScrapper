
from flask_table import Table, Col
import json
from flask import url_for, request


"""Lets suppose that we have a class that we get an iterable of from
somewhere, such as a database. We can declare a table that pulls out
the relevant entries, escapes them and displays them.
"""
id=96827995

class Item(object):
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
        return [
            Item(1, 'Z', 'zzzzz'),
            Item(2, 'K', 'aaaaa'),
            Item(3, 'B', 'bbbbb')]

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]

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

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for(request.endpoint, **request.view_args, sort=col_key, direction=direction, _anchor='main-table')

def table_maker(id):
    with open(f"app/opinions/json/{id}.json", "r", encoding="UTF-8") as jf:
        items = json.load(jf)
    table = SortableTable(items)

    # or {{ table }} in jinja
    return(table.__html__())

    