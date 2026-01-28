from heatmaps import *
from LT_ST_tools import *

def get_phelix(daydelta=1):
    path = "J:/BGV/Prognose/Speicheroptimierung/"
    reference_day = pd.Timestamp.today().floor('D')+pd.Timedelta(daydelta,unit="D")
    year = str(reference_day.year)
    month = str(reference_day.month)
    if len(month) == 1:
        month = "0" + month

    file = path + year + month + "_Speicheroptimierung.xlsm"

    if not os.path.isfile(file):
        month = str(reference_day.month - 1)
        if len(month) == 1:
            month = "0" + month

        file = path + year + month + "_Speicheroptimierung.xlsm"

    df = pd.read_excel(file, sheet_name='Börsenpreise_h',header=0,skiprows=1,nrows=24)

    return df[reference_day].values

def plot_price_comparison(n_exaa=1):

    today = pd.Timestamp.today().floor('D')
    starttime = today + pd.Timedelta(1, unit='D')
    endtime = starttime + pd.Timedelta(7, unit="D") - pd.Timedelta(1,unit="H")

    dates = [starttime + pd.Timedelta(i, unit="D") for i in np.arange(0, 7)]
    dates = date_for_heatmaps(dates)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches((9, 4))
    plt.xlim(starttime,endtime)
    ax.xaxis.set_ticks([starttime + pd.Timedelta(12,unit = "H") + pd.Timedelta(x,unit="D") for x in np.arange(0, 7)])
    ax.xaxis.set_ticklabels(dates)
    ax.set_ylabel("Preis [€/MWh]")

    file_hpfc = look_for_latest_file("LT", root)
    date_hpfc, price_hpfc = read_txt(file_hpfc)


    date_range = np.where(np.logical_and(date_hpfc >= starttime, date_hpfc <= endtime))
    ax.plot(date_hpfc[date_range],price_hpfc[date_range],color="lightgreen",label="HPFC")
    price_collection = np.array(price_hpfc[date_range])

    file_montel = look_for_latest_file("MarketData_Epex_Spot_AT_fcst_01h", root)
    if create_date_string(starttime) in file_montel:
        date_montel, price_montel = read_txt(file_montel)
        ax.plot(date_montel, price_montel, color="blue", label="Montel")
        price_collection = np.concatenate((price_collection,np.array(price_montel)))


    for i in np.arange(1,n_exaa+1):
        file_exaa = look_for_latest_file("EXAA", root,n_back=i)
        if create_date_string(starttime+pd.Timedelta(i-1,unit="D")) in file_exaa:
            date_exaa, price_exaa = read_txt(file_exaa)
            ax.plot(date_exaa, price_exaa, color="purple", label="EXAA")
            price_collection = np.concatenate((price_collection,np.array(price_exaa)))

    price_phelix = get_phelix()
    if not np.isnan(price_phelix[0]):
        ax.plot(date_exaa, price_phelix, color="red", label="PHELIX AT")
        price_collection = np.concatenate((price_collection, np.array(price_phelix)))

    for l in ax.axes.get_yticks():
        plt.axhline(l,alpha=0.1,color='black',zorder=-1,linewidth=1)
    for i in np.arange(1, 7):
        ax.axvline(starttime + pd.Timedelta(i,unit='D'), color='black', linestyle='--', alpha=0.1,linewidth=1)

    plt.legend(facecolor="white")

    labels = ["00:00","06:00","12:00","18:00"] * 7 + ["00:00"]
    labels_loc = [starttime + pd.Timedelta(6*i,unit="H") for i in np.arange(29)]

    ax2 = ax.twiny()
    ax2.xaxis.set_ticks_position('top')
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.set_ticks(labels_loc)
    ax2.xaxis.set_ticklabels(labels, rotation=45, rotation_mode="anchor",ha="left")
    ax2.set_xlim(starttime, endtime)

    min_val = np.nanmin(price_collection)-10
    max_val = np.nanmax(price_collection)+10
    plt.ylim(min_val,max_val)



    title_string = "Vergleich Week-Ahead-Preise"

    ax.set_title(title_string)

    plt.tight_layout()

    file_path = "C:/pySHOP/Results/Price_Comparison/"+create_date_string(starttime) +"/"

    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    plt.savefig(file_path +"price_comparison_"+create_date_string(starttime)+".pdf")
    plt.savefig(file_path +"price_comparison_"+create_date_string(starttime)+".jpeg")
    plt.savefig(file_path +"price_comparison_"+create_date_string(starttime)+".png")
    plt.close()

    date_range = np.where(date_hpfc >= starttime)
    date_hpfc = date_hpfc[date_range]
    price_hpfc = price_hpfc[date_range]

    f = open(file_path + "price_comparison_"+create_date_string(starttime)+".txt", "w")
    f.write("Date".ljust(25) + "HPFC AT".ljust(15) + "Montel".ljust(15) + "EXAA".ljust(15) + "PHELIX AT".ljust(15) + "\n")
    for i in np.arange(0,len(date_hpfc)):
        d = str(date_hpfc[i])
        hpfc = str(price_hpfc[i])
        try:
            montel = str(price_montel[i])
        except:
            montel = ""
        try:
            exaa = str(price_exaa[i])
        except:
            exaa = ""
        try:
            phelix = str(price_phelix[i])
        except:
            phelix = ""

        f.write(d.ljust(25) + hpfc.ljust(15) + montel.ljust(15) + exaa.ljust(15) + phelix.ljust(15) + "\n")

    f.close()

