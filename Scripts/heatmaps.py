import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from LT_ST_tools import get_price_data, look_for_latest_file, create_date_string
import os
from matplotlib.backends.backend_pdf import PdfPages

weekdays = {0: "Montag",
            1: "Dienstag",
            2:  "Mittwoch",
            3:  "Donnerstag",
            4:  "Freitag",
            5:  "Samstag",
            6:  "Sonntag"}

def get_day_of_week(date):
    return weekdays[date.dayofweek]

def date_for_heatmaps(date_list):

    new_date_list = []

    for d in date_list:
        new_date_list.append(get_day_of_week(d) + "\n" + str(d.day) + "." + str(d.month) + "." + str(d.year))

    return new_date_list

def get_vmin_vmax(data):
    vmin = 0
    vmax = 0

    if np.nanmin(data) != 0:
        vmin = np.nanmin(data)
    if np.nanmax(data) != 0:
        vmax = np.nanmax(data)

    if vmin == 0 and vmax != 0:
        vmin = -vmax
    if vmax == 0 and vmin != 0:
        vmax = -vmin

    return vmin, vmax



def price_heatmap_array(starttime,n_exaa=1):

    dates, price = get_price_data(montel=True,verbose=False,n_exaa=n_exaa)

    price_array = np.zeros((24,7))

    offset = np.where(dates == starttime)[0][0]

    for x in np.arange(0,7):
        price_array[:,x] = price[(x)*24+offset:(x+1)*24+offset]                 # start with (x+1) to skip current day in price data

    return price_array


def prod_heatmap_array(PP):

    today = pd.Timestamp.today().floor('D')
    starttime = today + pd.Timedelta(1, unit='D')

    if PP in ["DMH", "DRP"]:
        topology="Malta"
    elif PP in ["FE"]:
        topology="Fragant"
    elif PP in ["KAM"]:
        topology = "Kamering"
    elif PP in ["KOR"]:
        topology = "Koralpe"
    elif PP in ["FRE"]:
        topology = "Freibach"

    file =  "C:/pySHOP/Results/ST/" + create_date_string(starttime) + "/" + topology + "/timeSeries_"+topology+"_"+create_date_string(starttime)+".xlsx"

    data = pd.read_excel(file)

    if PP in ["DMH"]:
        prod = data["KW_DMH Production [MW]"]
        cons = -data["KW_DMH Consumption [MW]"]
    elif PP in ["DRP"]:
        prod = data["KW_DRP Production [MW]"]
        cons = -data["KW_DRP Consumption [MW]"]
    elif PP in ["FE"]:
        prod = data["KW_Feldsee Production [MW]"]
        cons = -data["KW_Feldsee Consumption [MW]"]
    elif PP in ["KAM"]:
        prod = data["KW_Kamering Production [MW]"]
        cons =-data["KW_Kamering Consumption [MW]"]
    elif PP in ["KOR"]:
        prod = data["KW_Koralpe Production [MW]"]
        cons =-data["KW_Koralpe Consumption [MW]"]
    elif PP in ["FRE"]:
        prod = data["KW_Freibach Production [MW]"]
        cons =-data["KW_Freibach Consumption [MW]"]

    #sanity check
    sanity_check = np.logical_and(np.where(prod != 0,1,0),np.where(cons != 0,1,0))
    if np.sum(sanity_check) > 0:
        print("Warning "+PP+": Hydraulic short circuit")

    total = prod + cons

    prod_array = np.zeros((24,7))

    for x in np.arange(0,7):
        prod_array[:,x] = total[(x)*24:(x+1)*24]                 # start with (x+1) to skip current day in price data

    return prod_array


def get_head_level(PP):
    today = pd.Timestamp.today().floor('D')
    starttime = today + pd.Timedelta(1, unit='D')

    if PP in ["DMH", "DRP"]:
        topology = "Malta"
    elif PP in ["FE"]:
        topology = "Fragant"
    elif PP in ["KAM"]:
        topology = "Kamering"
    elif PP in ["KOR"]:
        topology = "Koralpe"
    elif PP in ["FRE"]:
        topology = "Freibach"

    file = "C:/pySHOP/Results/ST/" + create_date_string(starttime) + "/" + topology + "/timeSeries_"+topology+"_"+create_date_string(starttime)+".xlsx"

    data = pd.read_excel(file)

    if PP in ["DMH"]:
        head = data["Galgenbichl level a.A. [m]"]
        title_string = "Galgenbichl"
        min_head =  np.nanmin(data["Galgenbichl tac. min [m]"])
        max_head =  np.nanmax(data["Galgenbichl tac. max [m]"])
    elif PP in ["DRP"]:
        head = data["Muehldorfersee level a.A. [m]"]
        title_string = "Muehldorfersee"
        min_head =  np.nanmin(data["Muehldorfersee tac. min [m]"])
        max_head =  np.nanmax(data["Muehldorfersee tac. max [m]"])
    elif PP in ["FE"]:
        head = data["Feldsee level a.A. [m]"]
        title_string = "Feldsee"
        min_head =  np.nanmin(data["Feldsee tac. min [m]"])
        max_head =  np.nanmax(data["Feldsee tac. max [m]"])
    elif PP in ["KAM"]:
        head = data["Wiederschwing level a.A. [m]"]
        title_string = "Wiederschwing"
        min_head =  np.nanmin(data["Wiederschwing tac. min [m]"])
        max_head =  np.nanmax(data["Wiederschwing tac. max [m]"])
    elif PP in ["KOR"]:
        head = data["Soboth level a.A. [m]"]
        title_string = "Soboth"
        min_head =  np.nanmin(data["Soboth tac. min [m]"])
        max_head =  np.nanmax(data["Soboth tac. max [m]"])
    elif PP in ["FRE"]:
        head = data["Freibach level a.A. [m]"]
        title_string = "Freibach"
        min_head =  np.nanmin(data["Freibach tac. min [m]"])
        max_head =  np.nanmax(data["Freibach tac. max [m]"])

    return head, title_string, min_head, max_head


def create_heatmap(PP,n_exaa=1):

    today = pd.Timestamp.today().floor('D')
    starttime = today + pd.Timedelta(1, unit='D')

    file_path = "C:/pySHOP/Results/_Heatmaps/" + create_date_string(starttime) +"/"

    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    dates = [starttime + pd.Timedelta(i,unit="D") for i in np.arange(0,7)]

    prices = price_heatmap_array(starttime,n_exaa=n_exaa)
    dates = date_for_heatmaps(dates)

    interval = np.linspace(0.35, 0.65)
    c = plt.cm.seismic_r(interval)
    cmap = LinearSegmentedColormap.from_list('seismic_reduced', c)

    with PdfPages(file_path+PP+".pdf")as pdf:
        fig, ax = plt.subplots(2,1)
        fig.set_size_inches((8.27-1, 11.69-1))

        title_string = r'Heatmap {p1}'.format(p1=PP)
        fig.suptitle(title_string,size=15,fontweight="bold")

        vmin, vmax = get_vmin_vmax(prices)

        ax[0].set_title(r"$\bfPrice~[EUR/MWh]$")
        ax[0].pcolormesh(prices,cmap=cmap,vmin=vmin,vmax=vmax)
        ax[0].xaxis.set_ticks(np.arange(0,7)+0.5)
        ax[0].xaxis.set_ticklabels(dates)
        ax[0].xaxis.set_ticks_position("top")
        ax[0].yaxis.set_ticks(np.arange(0,24)+0.5)
        ax[0].yaxis.set_ticklabels(np.arange(1,25))
        ax[0].axhline(8,color='black')
        ax[0].axhline(20,color='black')
        ax[0].invert_yaxis()
        ax[0].tick_params(axis=u'both', which=u'both', length=0)

        for y in np.arange(0,24):
            for x in np.arange(0,7):
                ax[0].text(x+0.5,y+0.6,r"{:.2f}".format(prices[y,x]),ha='center', va='center')

        if os.path.isfile(file_path+"_"+PP+".xlsx"):
            df = pd.read_excel(file_path+"_"+PP+".xlsx")
            total = df["Prod"].values

            prod = np.zeros((24, 7))

            for x in np.arange(0, 7):
                prod[:, x] = total[(x) * 24:(x + 1) * 24]  # start with (x+1) to skip current day in price data
        else:
            prod = prod_heatmap_array(PP)
        vmin, vmax = get_vmin_vmax(prod)

        if vmin == vmax:
            vmin = vmin - 0.5
            vmax = vmax + 0.5

        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

        ax[1].set_title(r"$\bfGeneration~&~Pump~[MW]$")
        ax[1].pcolormesh(prod,cmap=cmap,norm=norm)
        ax[1].xaxis.set_ticks(np.arange(0,7)+0.5)
        ax[1].xaxis.set_ticklabels(dates)
        ax[1].xaxis.set_ticks_position("top")
        ax[1].yaxis.set_ticks(np.arange(0,24)+0.5)
        ax[1].yaxis.set_ticklabels(np.arange(1,25))
        ax[1].axhline(8,color='black')
        ax[1].axhline(20,color='black')
        ax[1].invert_yaxis()
        ax[1].tick_params(axis=u'both', which=u'both', length=0)

        for y in np.arange(0,24):
            for x in np.arange(0,7):
                ax[1].text(x+0.5,y+0.6,"{:.1f}".format(prod[y,x]),ha='center', va='center')

        ax[1].text(-1, 26, "min")
        ax[1].text(-1, 27, "max")
        ax[1].text(-1, 28, "Pumpe",fontweight="bold",color="red")

        for x in np.arange(0,7):
            pump_mask = np.where(prod[:,x] < 0)
            if len(pump_mask[0]) > 0:
                min_pump = np.min(prices[:,x][pump_mask])
                max_pump = np.max(prices[:,x][pump_mask])

                ax[1].text(x+0.95,26,"{:.2f}".format(min_pump),ha='right', va='center')
                ax[1].text(x+0.95,27,"{:.2f}".format(max_pump),ha='right', va='center')
                ax[1].text(x+0.95,28,"{:.2f}".format(np.ceil(max_pump)),ha='right', va='center')
            else:
                ax[1].text(x + 0.95, 26, "-", ha='right', va='center')
                ax[1].text(x + 0.95, 27, "-", ha='right', va='center')
                ax[1].text(x + 0.95, 28, "-", ha='right', va='center')
        ax[1].text(-1, 30, "min")
        ax[1].text(-1, 31, "max")
        ax[1].text(-1, 32, "Turbine",fontweight="bold",color="blue")

        for x in np.arange(0,7):
            prod_mask = np.where(prod[:,x] > 0)
            if len(prod_mask[0]) > 0:
                min_prod = np.min(prices[:,x][prod_mask])
                max_prod = np.max(prices[:,x][prod_mask])

                ax[1].text(x+0.95,30,"{:.2f}".format(min_prod),ha='right', va='center')
                ax[1].text(x+0.95,31,"{:.2f}".format(max_prod),ha='right', va='center')
                ax[1].text(x+0.95,32,"{:.2f}".format(np.floor(min_prod)),ha='right', va='center')
            else:
                ax[1].text(x + 0.95, 30, "-", ha='right', va='center')
                ax[1].text(x + 0.95, 31, "-", ha='right', va='center')
                ax[1].text(x + 0.95, 32, "-", ha='right', va='center')

        pdf.savefig(bbox_inches='tight')
        #plt.savefig(file_path+PP+".pdf",bbox_inches='tight')
        plt.close()

        prices = prices.flatten(order="F")
        prod = prod.flatten(order="F")
        time = [starttime + pd.Timedelta(i, unit="H") for i in np.arange(0, 168)]

        data = {"Date": time, "Prices": prices, "Prod": prod}
        df = pd.DataFrame(data)
        df.to_excel(file_path + "_" + PP + ".xlsx")



        fig, ax = plt.subplots(1,1)
        fig.set_size_inches((9, 4))

        head, title_string, min_head, max_head = get_head_level(PP)

        ax.set_title(title_string)
        ax.fill_between(np.arange(0,len(head)), head, 0, color='blue', label='Storage')
        ax.set_ylabel("m.ü.A.")
        ax.set_ylim(min_head,max_head)
        ax.set_xlim(0,167)

        ax.xaxis.set_ticks(np.arange(12,168,24)+0.5)
        ax.xaxis.set_ticklabels(dates)
        for i in np.arange(1,7):
            ax.axvline(24*i,color='black',linestyle='--',alpha=0.25)

        ax_twin = ax.twinx()
        ax_twin.plot(np.arange(0,len(head)), prices, color='black', label='Inflow')
        ax_twin.set_ylabel(r'€/MWh')
        ax_twin.set_xlim(0,167)

        for i in ax_twin.yaxis.get_ticklocs():
            ax_twin.axhline(i,color='black',alpha=0.1)

        pdf.savefig(bbox_inches='tight')
        #plt.savefig(file_path+PP+".pdf",bbox_inches='tight')
        plt.close()








