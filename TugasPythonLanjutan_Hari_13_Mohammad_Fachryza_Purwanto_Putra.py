import pandas as pd, json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt 
import numpy as np 
  
with open(r'covid.json') as f: 
    data = json.load(f) 

df = json_normalize(data['Countries'])

new_df = df[(df.CountryCode == 'ID') | (df.CountryCode == 'KR') | (df.CountryCode == 'VN')].copy()

width = 0.25
r1 = np.arange(len(new_df.Country))
r2 = [x + width for x in r1]
r3 = [x + width for x in r2]


fig, ax = plt.subplots(figsize=(10,8))

plt.bar(r1, new_df.TotalConfirmed, width=width, label = 'Total Kasus Positif')
plt.bar(r2, new_df.TotalRecovered, width=width, label = 'Total Kasus Sembuh')
plt.bar(r3, new_df.TotalDeaths, width=width, label = 'Total Kematian')
ax.set_title("Kasus COVID-19 sampai 9 September 2020")
ax.set_xlabel("Negara")
ax.set_ylabel("Jumlah")

plt.xticks([r + width for r in range(len(new_df.Country))], ['Indonesia', 'Korea Selatan', 'Vietnam'])

for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.05, p.get_height()+1500))

plt.legend()
plt.show()

print("Analisa :\nMelihat grafik kasus COVID-19 dari 3 negara yaitu Indonesia, Korea Selatan dan Vietnam, maka diketahui bahwa Indonesia tercatat memiliki jumlah kasus positif COVID-19 terbanyak dibandingkan dengan Korea Selatan dan Vietnam.")