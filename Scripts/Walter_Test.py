from pyshop import ShopSession
from Topologies import *
from Inflow import *
from special_conditions import *
from save_results import *

########################################################################################################################
# Parameters
########################################################################################################################

#topology = "PSKW_Grosssee"
#topology = "Kegele_Brettsee_Zirmsee_4"
#topology = "SHOP_pump_example"
#topology = "Malta_Kolbnitz"
#topology = "Malta_Kolbnitz"
#topology = "Fragant_750MW"
#topology = "Malta"
#topology = "Koralpe"
#topology = "Fragant_small_and_ramp"
#topology = "Kolbnitz"
topology = "Kamering"


# HPFC AT Budget 2026
price_curve = "HPFC_AT_2026_Budget.xlsx"

# EXAA 2024 (quarterhourly)
# eVenture_2035 (prices 2035 but pasted into 2024)
#price_curve = "EXAA_2024_hourly.xlsx"
#price_curve = "EXAA_2024_quarterhourly.xlsx"
#price_curve = "eVenture_2035_quarterhourly.xlsx"

add_to_title = "Walter_Test_2025702_HPFC_2026"
if add_to_title != "":
    add_to_title = "_"+add_to_title

starttime = pd.Timestamp(2026,1,1)
endtime = pd.Timestamp(2027,1,1)

#title defined as "starttime_endtime"
title=create_dir_name(starttime, endtime)

# define time resolution
timeunit = "hour"
resolution = 1

MIP = False

log_gets=False

#flag for tactical limits
use_tactical_limits = False


for condition in ["default"]: #["default',"orig", "simple", "2035", "2035_small"]:
    title = create_dir_name(starttime, endtime)

    # working 2024-01-08
    #special_condition = "Koralpe_26_" + condition
    # special_condition ="Goessnitz_" + condition
    special_condition = "Kamering_" + condition

    #special_conditions = "SHOP_" + condition

    #special_condition = "Kegele_" + condition
    title = title + "_" + condition

    ########################################################################################################################
    # Set up optimization
    ########################################################################################################################
    file_path_root, file_path_detail = set_path("Misc/" + topology+"/"+title+"_"+str(resolution)+timeunit+add_to_title)

    # loading results from yaml file, e.g.
    #shop = ShopSession(license_path='C:/Shop_input/License', log_file=file_path_root+"logfile.log", log_gets=log_gets)
    #shop.load_yaml(file_path=file_path_root+"/results.yaml")

    run_start = time.time()
    shop = ShopSession(license_path='C:/pySHOP/License', log_file=file_path_root+"logfile.log", log_gets=log_gets)
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=timeunit, timeresolution=pd.Series(index=[starttime],data=[resolution]))

    print("Shop version: " + shop.get_shop_version()+"\n")

    print("Optimization start date:\t" + str(starttime))
    print("Optimization end date:\t\t" + str(endtime))

    # load topology
    print("Loading topology: " + topology)
    shop = load_topology(shop,topology,use_tactical_limits=use_tactical_limits,MIP=MIP)

    # set reservoir start levels
    print("Loading reservoir start levels")
    shop = set_res_start_level(shop,updated_start_level={})
    # set inflow

    print("Loading inflow")
    # Rampe
    shop = load_inflow_hourly(shop,"Inflow_TJAV", ignore=[])

    # Regulär
    #shop = load_inflow(shop, ignore=[])

    # load market data
    print("Loading market data")
    shop = load_market_data(shop,file=price_curve)

    # load special conditions
    if not special_condition == "":
        shop = load_special_conditions(shop,special_condition)

    #shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")
    shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")
    #shop = read_command_file(shop, "C:/pySHOP/Input/Commands/powelsrv_cmd.txt")
    #shop.model.global_settings.global_settings.universal_mip.set(1)
    #shop.model.global_settings.global_settings.mipgap_rel.set(0.0001)
    shop.dump_pyshop(file_path_root+"code.py")

    ########################################################################################################################
    # Run optimization
    ########################################################################################################################
    print("Starting optimization")
    run_opt(shop, run_start=run_start, save_path=file_path_root, n_iterations1=3, n_iterations2=3)

    ########################################################################################################################
    # Save results
    ########################################################################################################################
    shop.dump_yaml(file_path_root+"results.yaml")
    save_results(shop, file_path_root, file_path_detail, topology)
    get_economics(shop,save_path=file_path_root)