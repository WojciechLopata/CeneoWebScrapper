from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for
import json
import pandas as pd 
import os 
product_id=96827995
opinions = pd.read_json(f"app/opinions/{product_id}.json",orient='columns')
with open(f"app/opinions/{product_id}.csv",'w',encoding="UTF-8") as file:
            csvData = opinions.to_csv(index=False)
            print(csvData)
            file.write(csvData)