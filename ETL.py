from pickle import FALSE

import kagglehub
import pandas as pd
import numpy as np
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Download latest version
path = kagglehub.dataset_download("sidraaazam/coffee-sales-insights-report")

print("Path to dataset files:", path)

df = pd.read_csv("Coffe_sales.csv")
print(df.head())

print("A quantidade de nulos por campo é:\n", df.isnull().sum())

print('Qtd registros atual:', df.shape[0])
df.drop_duplicates()
print('Qtd de registros removendo as duplicadas:', len(df))

print('Qtd de valores únicos:\n', df.nunique())

valor_produto_stat = df['money'].values
print("Mediana", np.median(valor_produto_stat))
print("Média", np.mean(valor_produto_stat))
print("Mínimo", np.min(valor_produto_stat))
print("Máximo", np.max(valor_produto_stat))

df_att = df[['hour_of_day', 'cash_type', 'money', 'coffee_name', 'Time_of_Day', 'Weekday', 'Month_name', 'Date', 'Time']]
df_att.to_csv("cafe_df.csv", index=False)

print(df_att.head())