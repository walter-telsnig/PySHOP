import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_interpolated_cubature(masl,vol):
    new_masl = []
    new_vol = []

    for i in np.arange(0, len(masl)):

        if i == len(masl) - 1:
            new_masl.append(masl[i])
            new_vol.append(vol[i])
            continue

        slope = (vol[i + 1] - vol[i]) / (masl[i + 1] - masl[i])

        if masl[i] == masl[i+1]:
            print(masl[i])

        steps = np.arange(0, masl[i + 1] - masl[i], 0.01)

        for s in steps:
            new_masl.append(masl[i] + s)
            new_vol.append(vol[i] + s * slope)

    return new_masl, new_vol



file = "L:\Staukurven.xlsx"

df = pd.DataFrame()

########################################################################################################################
# Fragant, Freibach, Koralpe, Kamering
########################################################################################################################
wb = pd.read_excel(file,sheet_name="Staukurven")

res_list = ["Oschenik", "GS/HW", "Soboth", "Freibach", "Feldsee", "Haselstein", "Innerfragant",
            "Wurten", "Wölla", "Goessnitz", "Kamering", "Zirmsee"]



for res in res_list:

    dict = {}

    masl = wb[res].values
    vol = wb[res+".1"].values

    masl = [x for x in masl if not np.isnan(x)]         # clean list from nans
    vol = [x for x in vol if not np.isnan(x)]           # clean list from nans

    new_masl, new_vol = get_interpolated_cubature(masl,vol)

    dict[res + " HEAD [masl]"] = new_masl
    dict[res + " VOL [m3]"] = new_vol

    df_to_add = pd.DataFrame(dict)

    df = pd.concat([df,df_to_add],axis=1)

########################################################################################################################
# Malta
########################################################################################################################
wb = pd.read_excel(file,sheet_name="Staukurven_VBM")

res_list = ["KOEL", "GALG", "GOESS", "GRMS", "ROTTAU"]

for res in res_list:

    dict = {}

    masl = wb[res + " Kote"].values
    vol = wb[res + " Wasserinhalt"].values
    E = wb[res + " Energieinhalt"].values


    masl = [x for x in masl if not np.isnan(x)]         # clean list from nans
    vol = [x for x in vol if not np.isnan(x)]           # clean list from nans
    E = [x for x in E if not np.isnan(x)]           # clean list from nans

    new_masl, new_vol = get_interpolated_cubature(masl,vol)
    new_masl, new_E = get_interpolated_cubature(masl,E)

    dict[res + " HEAD [masl]"] = new_masl
    dict[res + " VOL [1000m3]"] = new_vol
    dict[res + " E [MWh]"] = new_E

    df_to_add = pd.DataFrame(dict)

    df = pd.concat([df,df_to_add],axis=1)

df.to_excel( "L:\Staukurven_neu.xlsx")



###
# res: "Oschenik", "GS/HW", "Soboth", "Freibach", "Feldsee", "Haselstein", "Innerfragant", "Wurten", "Wölla",
# "Goessnitz", "Kamering", "Zirmsee"
###

#res = "Soboth"
#plt.plot(df[res + " HEAD [masl]"].values,df[res + " VOL [m3]"].values)

###
# MALTA:
# res: "KOEL", "GALG", "GOESS", "GRMS", "ROTTAU"
###

#res = "GOESS"
#plt.plot(df[res + " HEAD [masl]"].values,df[res + " VOL [1000m3]"].values)
#plt.plot(df[res + " HEAD [masl]"].values,df[res + " E [MWh]"].values)
