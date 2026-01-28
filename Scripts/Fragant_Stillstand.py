from Topologies import *
from save_results import *
from Availability import *
from pyshop import ShopSession
from price_comparison import *
from special_conditions import *
from Inflow import load_inflow

########################################################################################################################
# Longterm
########################################################################################################################
topology = "Fragant"

today = pd.Timestamp.today().floor('D')

starttime = today + pd.Timedelta(1,unit='D')
endtime = pd.Timestamp(today.year+1,1,1)

time_unit = "hour"
time_resolution = {"Fragant": 1}

iterations = {"Fragant":  {"full": 3,
                           "iter": 2}}

mip_gap = {"Fragant":  0.01}


# Update initial starting levels and revisions
if False:
    print("Updating revision data")
    update_revisions()
    #Longterm revision overview
    revision_overview(starttime,endtime,Short_Term=False)
    #Shortterm revision overview
    revision_overview(starttime,starttime + pd.Timedelta(7,unit="D") + pd.Timedelta(1,unit="H"),Short_Term=True)

    correct_reservoir_start_level_file()

LT_start = time.time()
use_montel = False

for case in [6]:

    file_path_root, file_path_detail = set_path("/Bewertung/Ausfall_O3/Case " + str(case) )

    current_time_resolution = time_resolution[topology]

    shop = ShopSession(license_path='C:/pySHOP/License')
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=time_unit,
                             timeresolution=pd.Series(index=[starttime],data=[current_time_resolution]))

    print("Longterm Optimization: ".ljust(30) + topology.rjust(30))
    print("Start date:".ljust(30) + str(starttime).rjust(30))
    print("End date:".ljust(30) + str(endtime).rjust(30))

    shop = load_topology(shop,topology,use_tactical_limits=True,MIP=True)
    #shop = get_res_start_levels(shop)
    shop = load_inflow(shop)
    shop = load_price_data(shop,montel=use_montel)
    #shop = load_revisions(shop)

    shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")

    shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

    shop.model.reservoir.Grosssee.start_head.set(2409.07)
    shop.model.reservoir.Feldsee.start_head.set(2216.10)
    shop.model.reservoir.Wurten.start_head.set(1687.57)
    shop.model.reservoir.Oschenik.start_head.set(2374.40)
    shop.model.reservoir.Innerfragant.start_head.set(1197.18)
    shop.model.reservoir.Haselstein.start_head.set(1466.67)
    shop.model.reservoir.Woella.start_head.set(1537.77)
    shop.model.reservoir.Goessnitz.start_head.set(745.60)
    shop.model.reservoir.Moell.start_head.set(339)

    if case == 1:
        start_outage = pd.Timestamp(2023,8,29,0,0,1)
        end_outage = pd.Timestamp(2023,9,4)

    if case == 2:
        start_outage = pd.Timestamp(2023,9,4)
        end_outage = pd.Timestamp(2023,9,11)

    if case == 3:
        start_outage = pd.Timestamp(2023,9,11)
        end_outage = pd.Timestamp(2023,9,18)

    if case == 4:
        start_outage = pd.Timestamp(2023,9,18)
        end_outage = pd.Timestamp(2023,9,25)

    if case == 5:
        start_outage = pd.Timestamp(2023,9,25)
        end_outage = pd.Timestamp(2023,10,2)

    if case == 6:
        start_outage = pd.Timestamp(2023,10,2)
        end_outage = pd.Timestamp(2023,10,9)

    if case != 0:
        shop.model.generator.OS_G3.maintenance_flag.set(pd.Series([0,1,0], index=(starttime,start_outage,end_outage)))
        shop.model.pump.OS_P3.maintenance_flag.set(pd.Series([0,1,0], index=(starttime,start_outage,end_outage)))

    print("Start optimization")
    run_opt(shop, run_start=time.time(), save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                                   n_iterations2=iterations[topology]["iter"])

    shop.dump_yaml(file_path_root+"results.yaml")
    save_results(shop, file_path_root, file_path_detail,topology)

    plot_price_comparison()
    runtime = (time.time() - LT_start)/60
    print("Total runtime: " + "{:.2f}".format(runtime) + " min\n")




