import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, accuracy_score, f1_score
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

connection = sqlite3.connect("../olist.db")

df = pd.read_sql_query("SELECT * FROM TrainingDataset",connection)
df = df.dropna()
connection.close()

y = df['score']
X = df[["produit_recu","temps_livraison"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

model = LogisticRegression()

model.fit(X_train,y_train)

recall_train = round(recall_score(y_train, model.predict(X_train)),4)
acc_train = round(accuracy_score(y_train, model.predict(X_train)),4)
f1_train = round(f1_score(y_train, model.predict(X_train)),4)

print(f"Pour le jeu d'entrainement: \n le recall est de {recall_train}, \n l'accuracy de {acc_train} \n le f1 score de {f1_train}")

recall_test = round(recall_score(y_test, model.predict(X_test)),4)
acc_test = round(accuracy_score(y_test, model.predict(X_test)),4)
f1_test = round(f1_score(y_test, model.predict(X_test)),4)

print(f"Pour le jeu de test: \n le recall est de {recall_test}, \n l'accuracy de {acc_test} \n le f1 score de {f1_test}")

initial_type = [('float_input', FloatTensorType([None, 2]))]
onx = convert_sklearn(model, initial_types=initial_type)

with open("best_reg_lin_produit_recu.onnx", "wb") as f:
    f.write(onx.SerializeToString())
