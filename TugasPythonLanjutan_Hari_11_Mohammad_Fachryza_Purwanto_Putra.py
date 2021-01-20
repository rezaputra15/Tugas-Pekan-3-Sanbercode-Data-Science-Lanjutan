from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs 
import pandas as pd, numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

alamat = "https://pokemondb.net/pokedex/all"
safeAdd = Request(alamat, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(safeAdd)
data = bs(html, 'html.parser')

table = data.find("table", {"id":"pokedex"})
rows = data.findAll("tr")

row_data = []
for row in rows:
    cell_data = []
    if row.contents[1].get_text().strip() == "501": #stop function
        break

    for item in row.findAll(["th","td"]): #gathering function
        cell_data.append(item.get_text().strip())
    row_data.append(cell_data)

df = pd.DataFrame(row_data)
df.columns = df.iloc[0]
df = df[1:]
df = df.reset_index(drop=True)
df.to_csv(r"pokemon-fachreyzaputra.csv", index=False)
#print(df.info())


data = pd.read_csv(r"pokemon-fachreyzaputra.csv")
data[["#", "Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]] = data[["#", "Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].apply(pd.to_numeric)
#print(data.info())

data[["Alog", "Dlog"]] = np.log(data[["Attack", "Defense"]])

log_data = data.iloc[:, 10:12]
log_array = np.array(log_data)

# menentukan K / n_cluster elbow method
sse = []
k_list = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters = k).fit(log_array)
    centroids = kmeans.cluster_centers_
    prediksi = kmeans.predict(log_array)
    nilai_sse = 0
    
    for i in range(len(log_array)):
        titik_pusat = centroids[prediksi[i]]
        nilai_sse += (log_array[i, 0] - titik_pusat[0]) ** 2 + (log_array[i, 1] - titik_pusat[1]) ** 2
    
    sse.append(nilai_sse)
    k_list.append(k)

#print nilai K terbaik
print("Nilai K terbaik adalah 3")

plot1 = plt.figure(1)
plt.plot(k_list,sse)

# --- Menstandarkan Ukuran Variabel ---
scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(log_array)

# mencari zona clustering
kmeans = KMeans(n_clusters=3, random_state=200)
kmeans.fit(x_scaled)
data['kluster'] = kmeans.labels_

# --- Memvisualkan hasil kluster ---
plot2 = plt.figure(2)
output = plt.scatter(x_scaled[:,1], x_scaled[:,0], s = 20, c = data.kluster, marker = "o", alpha = 0.5)
centers = kmeans.cluster_centers_
plt.scatter(centers[:,0], centers[:,1], c='red', s=50, alpha=1 , marker="s")
plt.title("Hasil Klustering K-Means")
plt.xlabel("Atk")
plt.ylabel("Def")
plt.colorbar(output)
plt.show()

# save csv hasil klustering
data.to_csv(r"pokemon-cluster-fachreyzaputra.csv", index=False)