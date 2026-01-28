from Topologies import *
from save_results import *
from Availability import *
from pyshop import ShopSession
from price_comparison import *
from special_conditions import *
from Inflow import *

########################################################################################################################
# Longterm
########################################################################################################################
topology = "Fragant"

today = pd.Timestamp.today().floor('D')

starttime = pd.Timestamp(2023,1,1)
endtime = pd.Timestamp(2024,1,1)

time_unit = "hour"
time_resolution = {"Fragant": 1}

iterations = {"Fragant":  {"full": 3,
                           "iter": 2}}

mip_gap = {"Fragant":  0.01}

LT_start = time.time()
use_montel = False

for case in [0]:

    file_path_root, file_path_detail = set_path("/Bewertung/Test_hourly_inflow/Case " + str(case) )

    current_time_resolution = time_resolution[topology]

    shop = ShopSession(license_path='C:/pySHOP/License')
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=time_unit,
                             timeresolution=pd.Series(index=[starttime],data=[current_time_resolution]))

    print("Longterm Optimization: ".ljust(30) + topology.rjust(30))
    print("Start date:".ljust(30) + str(starttime).rjust(30))
    print("End date:".ljust(30) + str(endtime).rjust(30))

    shop = load_topology(shop,topology,use_tactical_limits=True,MIP=True)
    shop = set_res_start_level(shop,updated_start_level={})
    #shop = load_inflow(shop, ignore=[])
    shop = load_inflow_hourly(shop, sheet_name="2023")

    price_curve = "Preis_AT_2023_Ist.xlsx"
    shop = load_market_data(shop, file=price_curve)

    #shop = load_revisions(shop)

    shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")

    shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

    print("Start optimization")
    run_opt(shop, run_start=time.time(), save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                                   n_iterations2=iterations[topology]["iter"])

    shop.dump_yaml(file_path_root+"results.yaml")
    save_results(shop, file_path_root, file_path_detail,topology)

    plot_price_comparison()
    runtime = (time.time() - LT_start)/60
    print("Total runtime: " + "{:.2f}".format(runtime) + " min\n")




