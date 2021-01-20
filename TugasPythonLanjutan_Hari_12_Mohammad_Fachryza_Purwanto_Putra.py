import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv (r'pulsar_stars.csv')

#SVM
set_data = df.iloc [:, 0:8]
kluster_data = df.iloc [:,8] 

x_train, x_test, y_train, y_test = train_test_split(set_data, kluster_data, test_size=0.25,random_state=150) # 75% training and 25% test

model_s = svm.SVC(kernel='linear') # Linear Kernel
model_s.fit(x_train, y_train)
y_pred_svm = model_s.predict(x_test)
print("Classification Report SVM:\n", classification_report(y_test, y_pred_svm))
print("Accuracy Score SVM:\n", accuracy_score(y_test, y_pred_svm))
print("\nConfussion Matrix SVM:\n", confusion_matrix(y_test,y_pred_svm))

# KNN
data_knn = df.iloc [:, 2:4]
kluster_knn = df.iloc [:,8]

x_train_knn, x_test_knn, y_train_knn, y_test_knn = train_test_split(data_knn, kluster_knn, test_size=0.25,random_state=150) # 75% training and 25% test

model_knn = KNeighborsClassifier(n_neighbors=14)
model_knn.fit(x_train_knn, y_train_knn)
y_pred_knn = model_knn.predict(x_test_knn)

print("Classification Report KNN:\n", classification_report(y_test_knn, y_pred_knn))
print("Accuracy Score KNN:\n", accuracy_score(y_test_knn, y_pred_knn))
print("\nConfussion Matrix KNN:\n", confusion_matrix(y_test_knn, y_pred_knn))

#mementukan K terbaik pada KNN
error = []
for i in range(1, 50):
    model_k = KNeighborsClassifier(n_neighbors=i)
    model_k.fit(x_train_knn, y_train_knn)
    y_pred_k = model_k.predict(x_test_knn)
    error.append(np.mean(y_pred_k != y_test_knn))

plt.figure(1)  
plt.plot(range(1, 50), error, color='red', marker='o', markersize=5)
plt.title('Error pada nilai K')  
plt.xlabel('K')  
plt.ylabel('Error rata-rata')
plt.show()

print("\nNilai K terbaik untuk metode KNN adalah 14")