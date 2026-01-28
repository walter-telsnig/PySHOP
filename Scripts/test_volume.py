import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def add_padding(arr,num):
    padd = []
    for i in np.arange(0,num):
        padd.append(np.nan)

    return padd + arr.tolist() + padd

def moving_average(arr,window):
    if window%2==0:
        window+=1

    l = len(arr)

    padd = int((window-1)/2)
    arr = add_padding(arr,padd)

    av = []

    for i in np.arange(0,l):
        av.append(np.nanmean(np.roll(arr,-i)[0:window]))

    return np.array(av)




df = pd.read_excel("C:/pySHOP/Results/Misc/Forstsee/2025-Jan-1_2026-Jan-1_1hour_HPFC_Budget_2025.xlsx/timeSeries_Forstsee_20250101.xlsx")

head = df["Forstsee storage [Mm3]"].values
inflow = df['Forstsee inflow [m3/s]'].values * 3600 / 1e6
up = df['KW_Forstsee Upflow [m3/s]'].values * 3600 / 1e6
down = df['KW_Forstsee Discharge [m3/s]'].values * 3600 / 1e6

vol = np.zeros(len(head))
vol[0] = head[0]

for i in np.arange(1,len(head)):
    vol[i] = vol[i-1]+ inflow[i-1] + up[i-1] - down[i-1]

plt.figure(figsize=(20,5))
#plt.plot(np.abs(head-vol))

plt.plot(head,color='blue',label="head")
plt.plot(vol,color='red',label="vol")








df24 = pd.read_excel("C:/pySHOP/Results/Misc/Forstsee/2024-Jan-1_2025-Jan-1_1hour_HPFC_Budget_2024.xlsx/timeSeries_Forstsee_20240101.xlsx")
df25 = pd.read_excel("C:/pySHOP/Results/Misc/Forstsee/2025-Jan-1_2026-Jan-1_1hour_HPFC_Budget_2025.xlsx/timeSeries_Forstsee_20250101.xlsx")
df26 = pd.read_excel("C:/pySHOP/Results/Misc/Forstsee/2026-Jan-1_2027-Jan-1_1hour_HPFC_Budget_2026.xlsx/timeSeries_Forstsee_20260101.xlsx")
df21 = pd.read_excel("C:/pySHOP/Results/Misc/Forstsee/2021-Jan-1_2022-Jan-1_1hour_EPEX_PHELIX_AT_2021.xlsx/timeSeries_Forstsee_20210101.xlsx")

p21 = df21['Price [€]'].values
p24 = df24['Price [€]'].values
p25 = df25['Price [€]'].values
p26 = df26['Price [€]'].values

year = ["2021","2024","2025","2026"]
price = [p21,p24,p25,p26]
for i in np.arange(0,len(price)):
    p=price[i]

    av = moving_average(p,24)

    diff = np.abs(p-av)
    print(year[i] + ": " + str(np.mean(diff)))

    #####
    d = 0
    for j in np.arange(1,len(p)):
        d += np.abs(p[j]-p[j-1])
    print(year[i] + ": " + str(d))








