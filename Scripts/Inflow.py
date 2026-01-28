import pandas as pd
import numpy as np

########################################################################################################################
# load inflow data for a reservoir
# if use_inflow is set to False, a time series with zero inflow is loaded
########################################################################################################################
def load_RAV(res, starttime,endtime,use_inflow=True):

    if use_inflow:
        dateRange = pd.date_range(start=pd.Timestamp(starttime.year, 1, 1),
                                  end=pd.Timestamp(endtime.year + 1, 1, 1),
                                  freq='MS')[:-1]

        year_diff = (dateRange[-1].year - dateRange[0].year) + 1

        file = "C:/pySHOP/Input/Inflow.xlsx"
        df = pd.read_excel(file, sheet_name="Inflow")
        RAV_year = df[res].values                            #m3/month

        feb = 1 / (28 * 24 * 3600)
        f30 = 1 / (30 * 24 * 3600)
        f31 = 1 / (31 * 24 * 3600)

        RAV_factors = [f31,feb,f31,f30,f31,f30,f31,f31,f30,f31,f30,f31]

        RAV = np.array(RAV_year) * np.array(RAV_factors)
        RAV = RAV.tolist() * year_diff
    else:
        dateRange = [starttime]
        RAV = [0]

    return dateRange, RAV


########################################################################################################################
# load inflow data for a topology
########################################################################################################################
def load_inflow(shop,ignore=[]):
    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    list_of_reservoirs = shop.model.reservoir.get_object_names()

    for res in list_of_reservoirs:
        if res not in ["Drau","Moell","Woerthersee"]:
            if not res in ignore:
                inflow_time, inflow_value = load_RAV(res, starttime, endtime)
            else:
                inflow_time, inflow_value = load_RAV(res, starttime, endtime, use_inflow = False)

            shop.model.reservoir[res].inflow.set(pd.Series(inflow_value, index=inflow_time))

    return shop

########################################################################################################################
# load inflow data for a topology
########################################################################################################################
def load_inflow_hourly(shop,sheet_name, ignore=[]):
    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    list_of_reservoirs = shop.model.reservoir.get_object_names()

    #file = "C:\pySHOP\Input\Inflow_quarterhourly_2.xlsx"
    file = "C:\pySHOP\Input\Inflow_hourly_2.xlsx"
    df = pd.read_excel(file, sheet_name=sheet_name)

    for res in list_of_reservoirs:
        if res not in ["Drau","Moell","Woerthersee"]:
            inflow_value = df[res].values
            inflow_time = df["Date"].values
        else:
            inflow_value = [0]
            inflow_time = [starttime]

        shop.model.reservoir[res].inflow.set(pd.Series(inflow_value, index=inflow_time))

    return shop


########################################################################################################################
# Set reservoir start levels
########################################################################################################################
def set_res_start_level(shop,updated_start_level={}):
    # default values:
    # Fragant:
    start_level = {
    "Grosssee":  2407,
    "Grosssee_adv": 2407,
    "Feldsee":  2218.26,
    "Wurten":  1686.81,
    "Wurten_big": 1686.81,
    "Oschenik":  2377.00,
    "Innerfragant":  1197.40,
    "Haselstein":  1469,
    "Haselstein_big":  1470.72,
    "Woella":  1540.02,
    "Goessnitz":  746,
    "Moell":  339.01,
    "Zirmsee": 2500,
    "Brettsee": 2510,
    "Kegelesee": 2170,
    # Malta:
    "Koelnbrein":  1880,
    "Muehldorfersee":  2295.35,
    "Galgenbichl":  1695,
    "Goesskar":  1695,
    "Rottau":  597,
    "Rottau650": 597,
    "Kolbnitz": 702.5,
    # Koralpe:
    "Soboth":  1075,
    # Kamering:
    "Wiederschwing":  669,
    # Freibach:
    "Freibach":  721.5,
    "Drau":  339.01,
    # Forstsee:
    "Forstsee": 600,
    "Woerthersee": 439.01,
    # Bernegger
    "Bernegger_upper": 630,
    "Bernegger_lower": 30,
    "RSV1": 92,
    "RSV2": 43
    }

    # update default start levels:
    for i in updated_start_level.keys():
        start_level[i] = updated_start_level[i]

    list_of_reservoirs = shop.model.reservoir.get_object_names()

    for res in list_of_reservoirs:
        shop.model.reservoir[res].start_head.set(start_level[res])

    return shop