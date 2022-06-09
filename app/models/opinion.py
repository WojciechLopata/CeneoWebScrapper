import json

class Opinion():
    def __init__(self,product_id):
        with open(f"/opinions/{product_id}.json") as file:
            self.opinion=json.loads(file)
    def display(self):
        print(self.opinion)
            