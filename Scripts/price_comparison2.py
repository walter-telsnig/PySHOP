import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("C:/pySHOP/Input/Price_Curve/HPFC_Budget_2024.xlsx", sheet_name="AT")
df.drop_duplicates(inplace=True)
prices = df["Price"].tolist()
dates = df["Delivery Date"].tolist()

p4 = []
d4 = []
for i in np.arange(0,len(prices),4):
    p4.append(np.nansum(prices[i:i+4]))
    d4.append(dates[i])

plt.figure(figsize=(20,5))
plt.plot(dates,prices)
plt.plot(d4,p4)
