from bs4 import BeautifulSoup
import glob
import matplotlib.pyplot as plt
from LT_ST_tools import *
from Misc import show_runtime
import pickle
import os

base_loc                    = "C:/pySHOP/Input/Revisions/"
ID_info_location            = base_loc + "ID_info.npy"
handled_files_location      = base_loc + "handled_files"
revision_location           = base_loc + "revisions"
availability_root           = "//kwoptbatch1/C$/Powel/IccData/import/Availability/Success/"



def load_revisions(shop):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    with open(revision_location, "rb") as fp:
        in_use = pickle.load(fp)

    date1 = np.where(in_use["timeline"] == starttime)[0][0]
    date2 = np.where(in_use["timeline"] == endtime)[0][0]

    for ob in shop.model.generator:

        timeline    = in_use["timeline"][date1:date2]
        status      =  1 - in_use[get_availablilty_obj_id(ob.get_name())][date1:date2] # substracting from 1 to invert bool. values

        shop.model.generator[ob.get_name()].maintenance_flag.set(pd.Series(status, index=timeline))

    for ob in shop.model.pump:

        timeline    = in_use["timeline"][date1:date2]
        status      = 1 -in_use[get_availablilty_obj_id(ob.get_name())][date1:date2] # substracting from 1 to invert bool. values

        shop.model.pump[ob.get_name()].maintenance_flag.set(pd.Series(status, index=timeline))

    return shop




def get_availablilty_obj_id(name):

    if name == "KOR_G1":
        return "KO_G1"
    elif name == "KOR_G2":
        return "KO_G2"
    elif name == "KOR_P1":
        return "KO_P2"                      # change in number is intentional
    elif name == "DMH_P2":
        return "DMH_PU2"
    elif name == "DMH_P3":
        return "DMH_PU3"
    elif name == "DRP_P1":
        return "PuDRP_P1"
    elif name == "DRP_P2":
        return "PuDRP_P2"
    elif name == "FS_G1":
        return "FE_G1"
    elif name == "FS_G2":
        return "FE_G2"
    elif name == "FS_P1":
        return "FE_P1"
    elif name == "FS_P2":
        return "FE_P2"
    elif name == "OS_G1":
        return "O123_G1"
    elif name == "OS_G2":
        return "O123_G2"
    elif name == "OS_G3":
        return "O123_G3"
    elif name == "GO_G1":
        return "GOE_G1"
    elif name == "GO_G2":
        return "GOE_G2"
    elif name == "OS_P1":
        return "PuO1_P1"
    elif name == "OS_P2":
        return "PuO23_P1"
    elif name == "OS_P3":
        return "PuO23_P2"
    elif name == "WO_G1":
        return "WOE_G1"
    else:
        return name


# 1 hour needs to be added to dates, because they are in UTC
# add_time_correction also checks for daylight saving time
def add_time_correction(date):
    return pd.Timedelta(1,unit='H') +pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=date.hour,
                                                  minute=date.minute, second=date.second, tz = 'Europe/Berlin').dst()


def update_revisions():

    starttime = pd.Timestamp(2020,1,1)
    endtime = pd.Timestamp(pd.Timestamp.today().year + 5,1,1)
    timeline = pd.date_range(starttime,endtime,freq="1h")

    if os.path.isfile(ID_info_location):
        with open(ID_info_location, "rb") as fp:
            ID_info = pickle.load(fp)
    else:
        ID_info = {
        "ZN_G1": {},
        "ZN_G2": {},
        "FE_G1": {},
        "FE_G2": {},
        "FE_P1": {},
        "FE_P2": {},
        "WU_G1": {},
        "WU_G2": {},
        "WOE_G1": {},
        "HA_G1": {},
        "HA_P1": {},
        "AF_G1": {},
        "AF_G2": {},
        "AF_G3": {},
        "O123_G1": {},
        "O123_G2": {},
        "O123_G3": {},
        "PuO1_P1": {},
        "PuO23_P1": {},
        "PuO23_P2": {},
        "KO_G1": {},
        "KO_G2": {},
        "KO_P2": {},
        "KA_G1": {},
        "FB_G1": {},
        "FB_P2": {},
        "DMO_G1": {},
        "DMO_G2": {},
        "DMO_P1": {},
        "DMO_P2": {},
        "DRP_G1": {},
        "DRP_G2": {},
        "PuDRP_P1": {},
        "PuDRP_P2": {},
        "DMH_G1": {},
        "DMH_G2": {},
        "DMH_G3": {},
        "DMH_G4": {},
        "DMH_PU2": {},
        "DMH_PU3": {},
        "DMU_G1": {},
        "DMU_G2": {},
        "GOE_G1": {},
        "GOE_G2": {}
        }



    list_of_files = filter(os.path.isfile,glob.glob(availability_root+'*'))
    list_of_files = sorted(list_of_files, key = os.path.getmtime)

    if os.path.isfile(handled_files_location):
        with open(handled_files_location, "rb") as fp:
            handled_files = pickle.load(fp)
    else:
        handled_files = []


    for current_file in list_of_files:

        if current_file in handled_files:             # or pd.Timestamp(time.ctime(os.path.getmtime(current_file))) < pd.Timestamp(2021,1,1):
            continue

        with open(current_file,"r") as f:
            file = f.read()

        soup = BeautifulSoup(file, "xml")

        revisions = soup.find_all('revision')

        for entry in revisions:
            objectName = entry.find_all('objectName')[0].text
            jobID = entry.find_all('jobID')[0].text
            fT = pd.Timestamp(entry.find_all('fromTime')[0].text)           #fromTime
            fT = fT + add_time_correction(fT)
            fT = fT.round(freq="H")
            tT = pd.Timestamp(entry.find_all('toTime')[0].text)             #toTime
            tT = tT + add_time_correction(tT)
            tT = tT.round(freq="H")
            ID_info[objectName][jobID] = {"fromTime": fT, "toTime": tT}

        removeEntries = soup.find_all('removeEntry')

        for entry in removeEntries:
            objectName = entry.find_all('objectName')[0].text
            jobID = entry.find_all('jobID')[0].text

            ID_info[objectName].pop(jobID)

        handled_files.append(current_file)

    with open(handled_files_location, "wb") as fp:
        pickle.dump(handled_files,fp)

    with open(ID_info_location, "wb") as fp:
        pickle.dump(ID_info,fp)


    in_use = {
    "timeline": timeline,
    "ZN_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "ZN_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "FE_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "FE_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "FE_P1": np.array(np.ones(len(timeline)),dtype=bool),
    "FE_P2": np.array(np.ones(len(timeline)),dtype=bool),
    "WU_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "WU_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "WOE_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "HA_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "HA_P1": np.array(np.ones(len(timeline)),dtype=bool),
    "AF_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "AF_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "AF_G3": np.array(np.ones(len(timeline)),dtype=bool),
    "O123_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "O123_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "O123_G3": np.array(np.ones(len(timeline)),dtype=bool),
    "PuO1_P1": np.array(np.ones(len(timeline)),dtype=bool),
    "PuO23_P1": np.array(np.ones(len(timeline)),dtype=bool),
    "PuO23_P2": np.array(np.ones(len(timeline)),dtype=bool),
    "KO_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "KO_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "KO_P2": np.array(np.ones(len(timeline)),dtype=bool),
    "KA_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "FB_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "FB_P2": np.array(np.ones(len(timeline)),dtype=bool),
    "DMO_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "DMO_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "DMO_P1": np.array(np.ones(len(timeline)),dtype=bool),
    "DMO_P2": np.array(np.ones(len(timeline)),dtype=bool),
    "DRP_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "DRP_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "PuDRP_P1": np.array(np.ones(len(timeline)),dtype=bool),
    "PuDRP_P2": np.array(np.ones(len(timeline)),dtype=bool),
    "DMH_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "DMH_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "DMH_G3": np.array(np.ones(len(timeline)),dtype=bool),
    "DMH_G4": np.array(np.ones(len(timeline)),dtype=bool),
    "DMH_PU2": np.array(np.ones(len(timeline)),dtype=bool),
    "DMH_PU3": np.array(np.ones(len(timeline)),dtype=bool),
    "DMU_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "DMU_G2": np.array(np.ones(len(timeline)),dtype=bool),
    "GOE_G1": np.array(np.ones(len(timeline)),dtype=bool),
    "GOE_G2": np.array(np.ones(len(timeline)),dtype=bool)
    }

    for ob in ID_info:
        for id in ID_info[ob]:

            fT = ID_info[ob][id]["fromTime"]
            tT = ID_info[ob][id]["toTime"]

            date1 = np.where(in_use["timeline"] == pd.Timestamp(fT.year, fT.month, fT.day, fT.hour))[0][0]
            date2 = np.where(in_use["timeline"] == pd.Timestamp(tT.year, tT.month, tT.day, tT.hour))[0][0]

            in_use[ob][date1:date2] = False

    with open(revision_location, "wb") as fp:
        pickle.dump(in_use,fp)



def revision_overview(starttime,endtime,Short_Term=False):
    with open(revision_location, "rb") as fp:
        in_use = pickle.load(fp)

    date1 = np.where(in_use["timeline"] == starttime)[0][0]
    date2 = np.where(in_use["timeline"] == endtime)[0][0]

    length = date2-date1

    # Fragant
    Fragant = np.zeros((22,length))

    Fragant[0] = in_use["ZN_G1"][date1:date2]
    Fragant[1] = in_use["ZN_G2"][date1:date2]
    Fragant[2] = in_use["FE_G1"][date1:date2]
    Fragant[3] = in_use["FE_G2"][date1:date2]
    Fragant[4] = in_use["FE_P1"][date1:date2]
    Fragant[5] = in_use["FE_P2"][date1:date2]
    Fragant[6] = in_use["WU_G1"][date1:date2]
    Fragant[7] = in_use["WU_G2"][date1:date2]
    Fragant[8] = in_use["O123_G1"][date1:date2]
    Fragant[9] = in_use["O123_G2"][date1:date2]
    Fragant[10] = in_use["O123_G3"][date1:date2]
    Fragant[11] = in_use["PuO1_P1"][date1:date2]
    Fragant[12] = in_use["PuO23_P1"][date1:date2]
    Fragant[13] = in_use["PuO23_P2"][date1:date2]
    Fragant[14] = in_use["HA_G1"][date1:date2]
    Fragant[15] = in_use["HA_P1"][date1:date2]
    Fragant[16] = in_use["AF_G1"][date1:date2]
    Fragant[17] = in_use["AF_G2"][date1:date2]
    Fragant[18] = in_use["AF_G3"][date1:date2]
    Fragant[19] = in_use["WOE_G1"][date1:date2]
    Fragant[20] = in_use["GOE_G1"][date1:date2]
    Fragant[21] = in_use["GOE_G2"][date1:date2]



    # Malta
    Malta = np.zeros((16,length))

    Malta[0] = in_use["DRP_G1"][date1:date2]
    Malta[1] = in_use["DRP_G2"][date1:date2]
    Malta[2] = in_use["PuDRP_P1"][date1:date2]
    Malta[3] = in_use["PuDRP_P2"][date1:date2]
    Malta[4] = in_use["DMO_G1"][date1:date2]
    Malta[5] = in_use["DMO_G2"][date1:date2]
    Malta[6] = in_use["DMO_P1"][date1:date2]
    Malta[7] = in_use["DMO_P2"][date1:date2]
    Malta[8] = in_use["DMH_G1"][date1:date2]
    Malta[9] = in_use["DMH_G2"][date1:date2]
    Malta[10] = in_use["DMH_G3"][date1:date2]
    Malta[11] = in_use["DMH_G4"][date1:date2]
    Malta[12] = in_use["DMH_PU2"][date1:date2]
    Malta[13] = in_use["DMH_PU3"][date1:date2]
    Malta[14] = in_use["DMU_G1"][date1:date2]
    Malta[15] = in_use["DMU_G2"][date1:date2]


    # Freibach, Koralpe, Kamering
    Others = np.zeros((6,length))

    Others[0] = in_use["KO_G1"][date1:date2]
    Others[1] = in_use["KO_G2"][date1:date2]
    Others[2] = in_use["KO_P2"][date1:date2]
    Others[3] = in_use["KA_G1"][date1:date2]
    Others[4] = in_use["FB_G1"][date1:date2]
    Others[5] = in_use["FB_P2"][date1:date2]

    if Short_Term:
        timeframe = "ST"
    else:
        timeframe = "LT"

    save_loc = base_loc + create_date_string(pd.Timestamp.today()) + "/" + timeframe + "/"

    if not os.path.isdir(save_loc):
        os.makedirs(save_loc)

    Fragant_names = ["ZN_G1","ZN_G2", "FE_G1", "FE_G2", "FE_P1", "FE_P2", "WU_G1", "WU_G2", "O123_G1","O123_G2",
                     "O123_G3","PuO1_P1", "PuO23_P1","PuO23_P2","HA_G1","HA_P1","AF_G1","AF_G2","AF_G3","WOE_G1",
                     "GOE_G1","GOE_G2"]
    Malta_names = ["DRP_G1","DRP_G2","PuDRP_P1","PuDRP_P2","DMO_G1","DMO_G2","DMO_P1","DMO_P2","DMH_G1","DMH_G2",
                   "DMH_G3","DMH_G4","DMH_PU2","DMH_PU3","DMU_G1","DMU_G2"]
    Others_names = ["KO_G1","KO_G2","KO_P2","KA_G1","FB_G1","FB_P2"]

    labels_loc,labels = create_labels(starttime, endtime,Short_Term=Short_Term)

    #Fragant
    fig = plt.figure()
    fig.set_figwidth(18)
    fig.set_figheight(8)
    plt.xticks(rotation=90)
    ax = plt.gca()
    if Short_Term:
        ax.pcolormesh(Fragant,cmap='Paired_r',edgecolors='w',vmin=0,vmax=1)
        for vline in labels_loc[4::4]:
            ax.axvline(vline, linestyle='--', color='black')
        for vline in labels_loc[2::4]:
            ax.axvline(vline, linestyle='dotted', color='black', alpha=0.25)
    else:
        ax.pcolormesh(Fragant, cmap='Paired_r', edgecolors='w', vmin=0, vmax=1,lw=0)
    ax.xaxis.set_ticks(labels_loc)
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticks(np.arange(0,22)+0.5)
    ax.yaxis.set_ticklabels(Fragant_names)
    plt.tight_layout()
    plt.savefig(save_loc + "Fragant_revisions.pdf")
    plt.close()


    #Malta
    fig = plt.figure()
    fig.set_figwidth(18)
    fig.set_figheight(8)
    plt.xticks(rotation=90)
    ax = plt.gca()
    if Short_Term:
        ax.pcolormesh(Malta,cmap='Paired_r',edgecolors='w',vmin=0,vmax=1)
        for vline in labels_loc[4::4]:
            ax.axvline(vline, linestyle='--', color='black')
        for vline in labels_loc[2::4]:
            ax.axvline(vline, linestyle='dotted', color='black', alpha=0.25)
    else:
        ax.pcolormesh(Malta, cmap='Paired_r', edgecolors='w', vmin=0, vmax=1,lw=0)
    ax.xaxis.set_ticks(labels_loc)
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticks(np.arange(0,16)+0.5)
    ax.yaxis.set_ticklabels(Malta_names)

    plt.tight_layout()
    plt.savefig(save_loc + "Malta_revisions.pdf")
    plt.close()

    #Others
    fig = plt.figure()
    fig.set_figwidth(18)
    fig.set_figheight(8)
    plt.xticks(rotation=90)
    ax = plt.gca()
    if Short_Term:
        ax.pcolormesh(Others,cmap='Paired_r',edgecolors='w',vmin=0,vmax=1)
        for vline in labels_loc[4::4]:
            ax.axvline(vline, linestyle='--', color='black')
        for vline in labels_loc[2::4]:
            ax.axvline(vline, linestyle='dotted', color='black', alpha=0.25)
    else:
        ax.pcolormesh(Others, cmap='Paired_r', edgecolors='w', vmin=0, vmax=1,lw=0)
    ax.xaxis.set_ticks(labels_loc)
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticks(np.arange(0,6)+0.5)
    ax.yaxis.set_ticklabels(Others_names)
    plt.tight_layout()
    plt.savefig(save_loc + "Other_revisions.pdf")
    plt.close()


    #creating revision overview as txt files

    with open(ID_info_location, "rb") as fp:
        ID_info = pickle.load(fp)

    f = open(save_loc + "Revisions.txt", "w")

    f.write("Revision Overview\n")
    f.write("Start Date:".ljust(45) + str(starttime).ljust(25) + "\n")
    f.write("End Date:".ljust(45) + str(endtime).ljust(25) +"\n")
    f.write("\n")

    f.write("Fragant" + "\n")
    f.write("Object".ljust(10) + "ID".ljust(10) + "From".ljust(25) + "To".ljust(25) + "\n")
    for ob in Fragant_names:
        for id in ID_info[ob]:

            fT = ID_info[ob][id]["fromTime"]
            fT = pd.Timestamp(fT.year,fT.month,fT.day,fT.hour,fT.minute)
            tT = ID_info[ob][id]["toTime"]
            tT = pd.Timestamp(tT.year,tT.month,tT.day,tT.hour,tT.minute)

            if (fT >= starttime and fT <= endtime) or (tT >= starttime and tT <= endtime) or \
                (starttime >= fT and starttime <= tT):
                f.write(ob.ljust(10) + str(id).ljust(10) + str(fT).ljust(25) + str(tT).ljust(25) + "\n")

    f.write("\n")

    f.write("Malta" + "\n")
    f.write("Object".ljust(10) + "ID".ljust(10) + "From".ljust(25) + "To".ljust(25) + "\n")
    for ob in Malta_names:
        for id in ID_info[ob]:

            fT = ID_info[ob][id]["fromTime"]
            fT = pd.Timestamp(fT.year,fT.month,fT.day,fT.hour,fT.minute)
            tT = ID_info[ob][id]["toTime"]
            tT = pd.Timestamp(tT.year,tT.month,tT.day,tT.hour,tT.minute)

            if (fT >= starttime and fT <= endtime) or (tT >= starttime and tT <= endtime) or \
                (starttime >= fT and starttime <= tT):
                f.write(ob.ljust(10) + str(id).ljust(10) + str(fT).ljust(25) + str(tT).ljust(25) + "\n")

    f.write("\n")

    f.write("Others" + "\n")
    f.write("Object".ljust(10) + "ID".ljust(10) + "From".ljust(25) + "To".ljust(25) + "\n")
    for ob in Others_names:
        for id in ID_info[ob]:

            fT = ID_info[ob][id]["fromTime"]
            fT = pd.Timestamp(fT.year,fT.month,fT.day,fT.hour,fT.minute)
            tT = ID_info[ob][id]["toTime"]
            tT = pd.Timestamp(tT.year,tT.month,tT.day,tT.hour,tT.minute)

            if (fT >= starttime and fT <= endtime) or (tT >= starttime and tT <= endtime) or \
                (starttime >= fT and starttime <= tT):
                f.write(ob.ljust(10) + str(id).ljust(10) + str(fT).ljust(25) + str(tT).ljust(25) + "\n")
    f.close()




