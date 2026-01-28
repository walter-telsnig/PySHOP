import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def create_timestring(timestamp):
    y = str(timestamp.year)
    m = timestamp.month
    d = timestamp.day

    if d in np.arange(1,10):
        d = "0" + str(d)
    else:
        d = str(d)

    if m in np.arange(1,10):
        m = "0" + str(m)
    else:
        m = str(m)

    return y + "_" + m + "_" + d

def find_timestring(s,l):
    # s... timestring
    # l... list of timestrings

    for item in l:
        if s in item:
            return item

    return ""




epex_file = "C:/Users/baumga1/Desktop/Misc/EPEX PHELIX AT 2022.xlsx"
epex_prices = pd.read_excel(epex_file, sheet_name="Prices")         # EPEX prices

#epex_prices["Price Date"]
#epex_prices["Average Price"]

file = "C:/Users/baumga1/Desktop/Misc/Vergleich Montel-EXAA-PHELIX AT 2022.xlsx"
xl = pd.ExcelFile(file)
sheetnames = xl.sheet_names

date = pd.Timestamp(2022,1,1)

list_of_dates = []
HPFC = []
HPFC_p = []
MONTEL = []
MONTEL_p = []
EXAA = []
EXAA_p = []

while date <= pd.Timestamp(2022,12,24):

    print(date)

    timestring = create_timestring(date)
    sheet_name = find_timestring(timestring, sheetnames)

    if sheet_name != "":

        list_of_dates.append(date)

        epex_id = np.where(epex_prices["Price Date"] == date)[0][0]
        epex_comparison = np.array(epex_prices["Average Price"][epex_id:epex_id + (24*7)].values)

        prices = pd.read_excel(file, sheet_name=sheet_name, header=4, usecols=np.arange(1,11))

        hpfc_comparison = np.array(prices["HPFC_AT"][0:24*7].values)
        HPFC.append(epex_comparison - hpfc_comparison)
        HPFC_p.append((epex_comparison - hpfc_comparison)/epex_comparison)

        if "Montel 7 days" in list(prices.columns.values):
            montel_comparison = np.array(prices["Montel 7 days"][0:24*7].values)
            MONTEL.append(epex_comparison - montel_comparison)
            MONTEL_p.append((epex_comparison - montel_comparison)/epex_comparison)

        dummy = np.array(prices["EXAA"][0:24].values)
        exaa_comparison = np.where(np.zeros(24*7) == 0, np.nan, np.nan)
        exaa_comparison[0:24] = dummy
        EXAA.append(epex_comparison - exaa_comparison)
        EXAA_p.append((epex_comparison - exaa_comparison)/epex_comparison)

    date = date + pd.Timedelta(1,unit="Day")


mean_hpfc = np.nanmean(np.array(np.abs(HPFC_p)),axis=0)
std_hpfc = np.nanstd(np.array(np.abs(HPFC_p)),axis=0)/np.sqrt(np.nansum(np.where(np.isnan(HPFC_p),0,1),axis=0))
mean_montel = np.nanmean(np.array(np.abs(MONTEL_p)),axis=0)
std_montel = np.nanstd(np.array(np.abs(MONTEL_p)),axis=0)/np.sqrt(np.nansum(np.where(np.isnan(MONTEL_p),0,1),axis=0))
mean_exaa = np.nanmean(np.array(np.abs(EXAA_p)),axis=0)
std_exaa = np.nanstd(np.array(np.abs(EXAA_p)),axis=0)/np.sqrt(np.nansum(np.where(np.isnan(EXAA_p),0,1),axis=0))

plt.errorbar(np.arange(24*7),mean_hpfc,yerr=std_hpfc,label="HPFC",color="green",capsize=5)
plt.errorbar(np.arange(24*7),mean_montel,yerr=std_montel,label="Montel",color="blue",capsize=5)
plt.errorbar(np.arange(24*7),mean_exaa,yerr=std_exaa,label="EXAA",color="purple",capsize=5)
plt.legend()
plt.tight_layout()

