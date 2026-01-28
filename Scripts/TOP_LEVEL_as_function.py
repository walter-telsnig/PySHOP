from pyshop import ShopSession
from Topologies import *
from Inflow import *
from special_conditions import *
from save_results import *

log_gets=False

def run_optimization(topology,special_condition,starttime,endtime,timeunit,resolution,price_curve,
                     use_tactical_limits,add_to_title,MIP=False):

    if add_to_title != "":
        add_to_title = "_" + add_to_title

    title = create_dir_name(starttime, endtime)

    print("Optimization start date:\t" + str(starttime))
    print("Optimization end date:\t\t" + str(endtime))

    file_path_root, file_path_detail = set_path("Misc/" + topology+"/"+title+"_"+str(resolution)+timeunit+add_to_title)

    run_start = time.time()
    shop = ShopSession(license_path='C:/pySHOP/License', log_file=file_path_root + "logfile.log", log_gets=log_gets)
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=timeunit,
                             timeresolution=pd.Series(index=[starttime], data=[resolution]))

    ########################################################################################################################
    # Set up optimization
    ########################################################################################################################
    # load topology
    print("Loading topology: " + topology)
    shop = load_topology(shop, topology, use_tactical_limits=use_tactical_limits,MIP=MIP)

    # set reservoir start levels
    print("Loading reservoir start levels")
    shop = set_res_start_level(shop, updated_start_level={})
    # set inflow
    print("Loading inflow")
    shop = load_inflow(shop, ignore=[])

    # load market data
    print("Loading market data")
    shop = load_market_data(shop, file=price_curve)

    # load special conditions
    if not special_condition == "":
        shop = load_special_conditions(shop, special_condition)

    ########################################################################################################################
    # Run optimization
    ########################################################################################################################
    print("Starting optimization")
    run_opt(shop, run_start, save_path=file_path_root)

    ########################################################################################################################
    # Save results
    ########################################################################################################################
    shop.dump_yaml(file_path_root + "results.yaml")
    save_results(shop, file_path_root, file_path_detail)
    get_economics(shop, save_path=file_path_root)