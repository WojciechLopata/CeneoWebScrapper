from flask_table import Table, Col
from flask import Flask, request, url_for
import pandas as pd
import json

"""
A example for creating a Table that is sortable by its header
"""



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
        return url_for('table_maker', sort=col_key, direction=direction)


def table_maker(id):
    opinions = pd.read_json(f"app/opinions/json/{id}.json",orient='records')
    df = pd.DataFrame(opinions, columns=["opinion_id", "author", "recommendation","stars","content","useful","useless","publish_date","purchase_date","pros","cons"])

    sort = request.args.get('sort', 'opinion_id')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    df = df.sort_values(by=[sort], ascending=reverse)
    output_dict = df.to_dict(orient='records')

    table = SortableTable(output_dict,
                          sort_by=sort,
                          sort_reverse=reverse)
    return table.__html__()
