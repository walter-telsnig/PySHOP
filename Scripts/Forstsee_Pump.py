from pyshop import ShopSession
from Topologies import *
from Inflow import *
from special_conditions import *
from save_results import *

time_resolution = { "Forstsee": 1}
iterations = {  "Forstsee": {   "full": 5,
                                "iter": 3}}
mip_gap = { "Forstsee": 0.0001}


timeframe = {"EPEX_PHELIX_AT_2021.xlsx": [pd.Timestamp(2021,1,1),pd.Timestamp(2022,1,1)],
             "EPEX_PHELIX_AT_2019.xlsx": [pd.Timestamp(2019,1,1),pd.Timestamp(2020,1,1)],
             "HPFC_Budget_2024.xlsx": [pd.Timestamp(2024,1,1),pd.Timestamp(2025,1,1)],
             "HPFC_Budget_2025.xlsx": [pd.Timestamp(2025,1,1),pd.Timestamp(2026,1,1)],
             "HPFC_Budget_2026.xlsx": [pd.Timestamp(2026,1,1),pd.Timestamp(2027,1,1)]}

########################################################################################################################
# Parameters
########################################################################################################################
topology = "Forstsee"
special_condition = ""




for price_curve in ["EPEX_PHELIX_AT_2019.xlsx","EPEX_PHELIX_AT_2021.xlsx",
                     "HPFC_Budget_2024.xlsx","HPFC_Budget_2025.xlsx","HPFC_Budget_2026.xlsx"]:

    add_to_title = price_curve.replace(".xlsx","")+"_pump_as_turbine_no_pump"
    if add_to_title != "":
        add_to_title = "_"+add_to_title


    starttime = timeframe[price_curve][0]
    endtime = timeframe[price_curve][1]

    timeunit = "hour"
    resolution = 1

    MIP = True

    log_gets=False

    use_tactical_limits = True

    ########################################################################################################################
    # Set up optimization
    ########################################################################################################################
    title=create_dir_name(starttime, endtime)
    file_path_root, file_path_detail = set_path("Misc" + "/" + topology+"/"+title+"_"+str(resolution)+timeunit+add_to_title)

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
    shop = load_inflow(shop)

    # load market data
    print("Loading market data")
    shop = load_market_data(shop,file=price_curve)

    # load special conditions
    if not special_condition == "":
        shop = load_special_conditions(shop,special_condition)

    shop.model.global_settings.global_settings.universal_mip.set(1)
    shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

    ########################################################################################################################
    # Run optimization
    ########################################################################################################################
    shop = read_command_file(shop,"C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt" )

    print("Starting optimization")
    run_opt(shop, run_start=run_start, save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                                 n_iterations2=iterations[topology]["iter"])
    ########################################################################################################################
    # Save results
    ########################################################################################################################
    #shop.dump_yaml(file_path_root+"results.yaml")
    save_results(shop, file_path_root, file_path_detail,topology)

    shop.dump_pyshop(file_path_root+"code.py")