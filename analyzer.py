from cProfile import label
import os
import numpy as np
from numpy import average
import pandas as pd
from matplotlib import colors, pyplot as plt
print(*[filename.split(".")[0] for filename in os.listdir("./opinions")],sep="\n")
id=input("Podaj id produktu którego opinie chcesz sprawdzić ")
opinions=pd.read_json(f"opinions/{id}.json")
opinions_count=len(opinions)
pros_count=opinions["pros"].map(bool).sum()
cons_count=opinions["cons"].map(bool).sum()
opinions["stars"]=opinions["stars"].map(lambda x: float(x.split('/')[0].replace(",",".")))
average_score=opinions["stars"].mean().round(2)
recomendation=opinions["recomendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam","Polecam",None],fill_value=0)
recomendation.plot.pie(
    label="",
    autopct=lambda p: '{:.1f}%'.format(round(p)) if p>0 else "",
    colors=["crimson","forestgreen","lightskyblue"],
    labels=["Nie polecam","Polecam","Nie mam zdania"]
)
plt.title("Rekomendacje")
plt.savefig(f"plots/{id}_recomendation.png")
plt.close()
stars=opinions["stars"].value_counts().reindex(list(np.arange(0,5.5,0.5)),fill_value=0)
stars.plot.bar(
color="pink"

)
plt.title("oceny produktu")
plt.xlabel("liczba gwiazdek")
plt.ylabel("liczba opinii")
plt.grid(True,axis="y")
plt.xticks(rotation=0)
plt.savefig(f"plots/{id}_stars.png")
plt.close()