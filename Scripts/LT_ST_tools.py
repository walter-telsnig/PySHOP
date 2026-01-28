import time
import stat
import re
from Misc import convert_vol_to_head, convert_head_to_vol
import pandas as pd
import numpy as np
import os

root = "//kwoptbatch1/C$/Powel/IccData/import/GS2/Excel/Success/"

def convert_date_to_string(date):
    return str(date.year) +"-"+str(date.month)+"-"+str(date.day)


def create_labels(start, end,Short_Term = True):
    labels = [convert_date_to_string(start)]
    labels_loc = [0]

    if Short_Term:
        labels.append("06:00")
        labels_loc.append(6)
        labels.append("12:00")
        labels_loc.append(12)
        labels.append("18:00")
        labels_loc.append(18)

    day = start + pd.Timedelta(1,"D")

    counter = 24
    while day <= end:
        if Short_Term or day.dayofweek == 0:
            labels.append(convert_date_to_string(day))
            labels_loc.append(counter)
        if Short_Term and day != (end-pd.Timedelta(1,unit="H")):
            labels.append("06:00")
            labels_loc.append(counter+6)
            labels.append("12:00")
            labels_loc.append(counter + 12)
            labels.append("18:00")
            labels_loc.append(counter + 18)

        counter += 24
        day = day + pd.Timedelta(1, "D")

    return labels_loc, labels

def look_for_latest_file(id, root, n_back = 1):
    day = pd.Timestamp.today() + pd.Timedelta(3, unit="D")

    looking_for_file = True
    counter = 0
    while looking_for_file:
        file = create_date_string(day) + "_" + id + ".txt"
        if os.path.isfile(root + file):
            counter += 1
        else:
            if day < pd.Timestamp(2020, 1, 1):
                print("No File found: " + id)
                break

        if counter == n_back:
            looking_for_file = False
            break

        day = day - pd.Timedelta(1, unit="D")

    return root + file


def count_lines(file):
    # open file in read mode
    with open(file, 'r') as f:
        for count, line in enumerate(f):
            pass
    return count + 1


def read_txt(file):
    n_lines = count_lines(file) - 2
    date = np.empty(n_lines, dtype='<M8[ns]')
    val = np.empty(n_lines, dtype=np.float64)

    f = open(file, "r")
    line = f.readline()  # skip id
    line = f.readline()  # skip units

    counter = 0
    for line in f.readlines():
        l = line.replace("\n", "")
        l_split = l.split(";")
        v = l_split[1].replace(",", ".")

        date[counter] = pd.Timestamp(l_split[0])
        val[counter] = float(v)
        counter += 1

    date = pd.to_datetime(date)

    f.close()

    return date, val


def create_date_string(timestamp):
    y = str(timestamp.year)
    m = str(timestamp.month)
    d = str(timestamp.day)

    if len(m) != 2:
        m = "0" + m

    if len(d) != 2:
        d = "0" + d

    return y + m + d


def extract_date(file):
    date = re.findall("\d{8}", file)
    y = int(date[0][0:4])
    m = int(date[0][4:6])
    d = int(date[0][6:])

    return pd.Timestamp(y,m,d).date()


def correct_reservoir_start_level_file():

    original_location = "J:/Kraftwerksoptimierung&Statistik/Powel/07_Zufluss/"
    target_location = root

    today = pd.Timestamp.today().floor(freq="D") + pd.Timedelta(1, unit="D")
    date_string = create_date_string(today)

    line = []

    file = look_for_latest_file("reservoir_start_levels", root)
    f = open(file,"r")
    line.append(f.readline())
    f.close()


    file = look_for_latest_file("reservoir_start_levels", original_location)

    f = open(file, "r")
    L = f.readlines()
    for i in np.arange(0, len(L)):
        L[i] = L[i].replace("\x00", "")
        L[i] = L[i].replace("ÿþ", "")
        L[i] = L[i].replace("\"", "")
    f.close()

    line.append(L[2])

    f = open(target_location + date_string + "_reservoir_start_levels.txt","w")
    f.write(line[0])
    f.write(line[1])
    f.close()



def get_res_start_levels(shop):

    file = look_for_latest_file("reservoir_start_levels", root)
    df = pd.read_csv(file, sep=";", decimal=",")

    print("Reservoir Start Levels".ljust(30) + str(extract_date(file)).rjust(30))

    file_stats = os.stat(file)
    modification_time = pd.Timestamp(time.ctime(file_stats[stat.ST_MTIME])).floor('D')

    if modification_time != pd.Timestamp.today().floor('D'):
        print("WARNING: Reservoir start levels are outdated.")
        print("Latest update: " + str(modification_time))

    for res in shop.model.reservoir:
        if res.get_name() in ["Moell", "Drau", "Woerthersee"]:
            if res.get_name() == "Moell":
                res.start_head.set(339.01)
            elif res.get_name() == "Drau":
                res.start_head.set(339.01)
            elif res.get_name() == "Woerthersee":
                res.start_head.set(439.01)
        elif res.get_name() == "Wiederschwing":
            res.start_head.set(check_start_head(df["Kamering"][0],res))
        elif res.get_name() == "Grosssee":
            res.start_head.set(check_start_head(df["Grossee Hochwurten"][0],res))
        elif res.get_name() == "Woella":
            res.start_head.set(check_start_head(df["Wölla"][0],res))
        elif res.get_name() == "Muehldorfersee":
            res.start_head.set(check_start_head(df["Großer Mühldorfersee"][0],res))
        elif res.get_name() == "Koelnbrein":
            res.start_head.set(check_start_head(df["Kölnbrein"][0],res))
        else:
            name = res.get_name()
            res.start_head.set(df[name])

    return shop


def check_start_head(val, res):
    min_limit = convert_vol_to_head([res.tactical_limit_min.get().values[0]],res.get_name())[0]
    max_limit = convert_vol_to_head([res.tactical_limit_max.get().values[0]],res.get_name())[0]

    if val > max_limit:
        print("WARNING " + res.get_name() + ": Starthead of " + str(val) + " above max. tact. limit of "
              + str(max_limit) + "." )
        val = max_limit

    if val < min_limit:
        print("WARNING " + res.get_name() + ": Starthead of " + str(val) + " below min. tact. limit of "
              + str(min_limit) + ".")
        val = min_limit

    return val

def update_price_curve(base_date, base_val, update_date, update_val):
    for i in np.arange(0, len(update_date)):
        loc = np.where(base_date == update_date[i])
        if len(loc[0]) != 0:
            loc = loc[0][0]
            base_val[loc] = update_val[i]

    return base_val

def update_inflow(base_date, base_val, update_date, update_val):
    for i in np.arange(0, len(update_date)):
        loc = np.where(base_date == update_date[i])[0]
        base_val[loc] = update_val[i]

    return base_val

def get_inflow(shop, Short_Term=False):

    for res in shop.model.reservoir:
        if res.get_name() in ["Moell","Drau","Woerthersee","Muehldorfersee"]:
            starttime = shop.get_time_resolution()['timeresolution'].index[0]
            res.inflow.set(pd.Series([0],index=[starttime]))
        else:
            file_LT = look_for_latest_file(res.get_name() + "_inflow_fcast_LT", root)
            print(("LT Inflow " + res.get_name()).ljust(30) + str(extract_date(file_LT)).rjust(30))
            dates_LT, inflow_LT = read_txt(file_LT)

            if res.get_name() in ['Koelnbrein', 'Muehldorfersee', 'Galgenbichl', 'Goesskar', 'Rottau']:
                inflow_LT = inflow_LT * 0.24

            if Short_Term:
                file_ST = look_for_latest_file(res.get_name() + "_inflow_fcast_01h", root)
                print(("ST Inflow " + res.get_name()).ljust(30) + str(extract_date(file_ST)).rjust(30))
                dates_ST, inflow_ST = read_txt(file_ST)

                if res.get_name() in ['Koelnbrein', 'Muehldorfersee', 'Galgenbichl', 'Goesskar', 'Rottau']:
                    inflow_ST = inflow_ST * 0.24

                inflow_LT = update_inflow(dates_LT, inflow_LT, dates_ST, inflow_ST)

            res.inflow.set(pd.Series(inflow_LT, index=dates_LT))

    return shop



def get_price_data(montel = False,verbose=True,n_exaa=1):

    file_hpfc = look_for_latest_file("LT", root)
    if verbose:
        print("HPFC  Price Curve".ljust(30) + str(extract_date(file_hpfc)).rjust(30))
    date_hpfc, price = read_txt(file_hpfc)

    if montel:
        file_montel = look_for_latest_file("MarketData_Epex_Spot_AT_fcst_01h", root)
        if verbose:
            print("Montel Price Curve".ljust(30) + str(extract_date(file_montel)).rjust(30))
        date_montel, price_montel = read_txt(file_montel)

        price = update_price_curve(date_hpfc, price, date_montel, price_montel)

    if n_exaa:
        for i in np.arange(1,n_exaa+1):
            file_exaa = look_for_latest_file("EXAA", root,n_back=i)
            if verbose:
                print("EXAA  Price Curve".ljust(30) + str(extract_date(file_exaa)).rjust(30))
            date_exaa, price_exaa = read_txt(file_exaa)

            price = update_price_curve(date_hpfc, price, date_exaa, price_exaa)

    return date_hpfc, price

def load_price_data(shop, montel=False,n_exaa=0):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]

    dates, price = get_price_data(montel=montel,n_exaa=n_exaa)

    shop.model.market.add_object('price_curve')
    price_curve = shop.model.market.price_curve
    price_curve.sale_price.set(pd.DataFrame(price, index=dates))

    price_curve.buy_price.set(price_curve.sale_price.get())
    price_curve.max_buy.set(pd.Series([5000], [starttime]))
    price_curve.max_sale.set(pd.Series([5000], [starttime]))
    price_curve.load.set(pd.Series([0], [starttime]))  # fixed amount that must be delivered to this market

    return shop


def set_res_window(shop, file_path_root, topology):
    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    sd = shop.get_time_resolution()['timeresolution'].index[0]
    ds = create_date_string(sd)

    result_file = file_path_root.replace("ST", "LT") + "timeSeries_"+topology+"_"+ds+".xlsx"

    df = pd.read_excel(result_file)
    dates = []
    for d in df["Unnamed: 0"].values:
        dates.append(pd.Timestamp(d))

    dates = np.array(dates)

    for res in shop.model.reservoir:
        if res.get_name() not in ["Drau", "Moell", "Woerthersee"]:
            ref_head = df[res.get_name() + " level a.A. [m]"]

            ref_date_index = np.where(dates == endtime)[0][0]
            ref_head = convert_head_to_vol(res.get_name(),ref_head[ref_date_index])

            res.schedule.set(pd.Series([ref_head], index=[starttime]))
            res.schedule_flag.set(1)

            res.upper_slack.set(ref_head+0.01)
            res.lower_slack.set(ref_head-0.01)

    return shop


# old version setting res. windows via head constraints

#def set_res_window(shop, file_path_root, head_window=0.05):
#    starttime = shop.get_time_resolution()['timeresolution'].index[0]
#    endtime = shop.get_time_resolution()['timeresolution'].index[-1]
#
#    result_file = file_path_root.replace("ST", "LT") + "timeSeries.xlsx"
#
#    df = pd.read_excel(result_file)
#    dates = []
#    for d in df["Unnamed: 0"].values:
#        dates.append(pd.Timestamp(d))
#
#    dates = np.array(dates)
#
#    for res in shop.model.reservoir:
#        if res.min_head_constr.get() is None:
#            res.min_head_constr.set(pd.Series([res.lrl.get()], index=[starttime]))
#        if res.max_head_constr.get() is None:
#            res.max_head_constr.set(pd.Series([res.hrl.get()], index=[starttime]))
#
#        ref_head = df[res.get_name() + " level a.A. [m]"]
#
#        ref_date_index = np.where(dates == endtime)[0][0]
#        ref_head = ref_head[ref_date_index]
#
#        min_head_date = res.min_head_constr.get().index
#        min_head_val = res.min_head_constr.get().values
#        min_head_val[-1] = ref_head - head_window
#        res.min_head_constr.set(pd.Series(min_head_val, index=min_head_date))
#
#        max_head_date = res.max_head_constr.get().index
#        max_head_val = res.max_head_constr.get().values
#        max_head_val[-1] = ref_head + head_window
#        res.max_head_constr.set(pd.Series(max_head_val, index=max_head_date))

#    return shop





