from pyshop import ShopSession
from Topologies import *
from Inflow import *
from special_conditions import *
from save_results import *

time_resolution = { "Freibach": 1,
                    "Kamering": 1,
                    "Koralpe": 1,
                    "Malta": 2,
                    "Fragant": 4}

iterations = {  "Freibach": {   "full": 5,
                                "iter": 3},
                "Kamering":  {   "full": 5,
                                "iter": 3},
                "Koralpe":  {   "full": 5,
                                "iter": 3},
                "Malta":  {   "full": 3,
                                "iter": 2},
                "Fragant":  {   "full": 3,
                                "iter": 2},
                "Fragant_Haselstein": {"full": 3,
                            "iter": 2}
                }

mip_gap = { "Freibach": 0.0001,
            "Kamering": 0.001,      #0.0001
            "Koralpe":  0.0001,
            "Malta":    0.01,
            "Fragant":  0.01,
            "Fragant_Haselstein": 0.01}

########################################################################################################################
# Parameters
########################################################################################################################
# Available topologies
# Base topologies: "Koralpe","Freibach", "Kamering", "Malta", "Fragant", "Forstsee", "Forstsee_no_pump"
# Variants: "Koralpe_full", "Koralpe_ramp", "Fragant_Haselstein", Fragant_Haselstein_big", "Fragant_no_Haselstein", "Fragant_ramp"

topology = "Kamering"
special_condition = ""
                                                    # topology Koralpe_full  -> "Koralpe_23_24"
                                                    # topology Fragant  -> "empty_Fragant"

price_curve = "HPFC_AT_2026_Budget.xlsx"                    #"Spot_2019.xlsx"

add_to_title = "2025-07-15_WT-[668,5-676,17]_0,53"
if add_to_title != "":
    add_to_title = "_"+add_to_title

starttime = pd.Timestamp(2026,1,1)
endtime = pd.Timestamp(2027,1,1)

#title defined as "starttime_endtime"
title=create_dir_name(starttime, endtime)

# define time resolution
timeunit = "hour"
resolution = 1

MIP = True

log_gets=False

#flag for tactical limits
use_tactical_limits = True

########################################################################################################################
# Set up optimization
########################################################################################################################
file_path_root, file_path_detail = set_path("Misc" + "/" + topology+"/"+title+"_"+str(resolution)+timeunit+add_to_title)

# loading results from yaml file, e.g.
#shop = ShopSession(license_path='C:/Shop_input/License', log_file=file_path_root+"logfile.log", log_gets=log_gets)
#shop.load_yaml(file_path=file_path_root+"/results.yaml")

run_start = time.time()
shop = ShopSession(license_path='C:/pySHOP/License', log_file=file_path_root+"logfile.log", log_gets=log_gets)
shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=timeunit, timeresolution=pd.Series(index=[starttime],data=[resolution]))

#shop.model.global_settings.global_settings.universal_mip.set(1)
#shop.set_mipgap(['relative'],[0.01])

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
#shop = load_inflow(shop, ignore=["Haselstein","Innerfragant"])
shop = load_inflow_hourly(shop,"Inflow_TJAV", ignore=[])

# load market data
print("Loading market data")
shop = load_market_data(shop,file=price_curve)

# load special conditions
if not special_condition == "":
    shop = load_special_conditions(shop,special_condition)

if topology in ["Freibach","Kamering","Korlape","Koralpe_full","Fragant"]:
    shop.model.global_settings.global_settings.universal_mip.set(1)
else:
    shop.model.global_settings.global_settings.universal_mip.set(0)

shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])



########################################################################################################################
# Run optimization
########################################################################################################################
shop = read_command_file(shop,"C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt" )



print("Starting optimization")
#print(shop.model.global_settings.global_settings.solver_algorithm.get())
run_opt(shop, run_start=run_start, save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                             n_iterations2=iterations[topology]["iter"])
########################################################################################################################
# Save results
########################################################################################################################
shop.dump_yaml(file_path_root+"results.yaml")
save_results(shop, file_path_root, file_path_detail,topology)
#get_economics(shop,save_path=file_path_root)

shop.dump_pyshop(file_path_root+"code.py")



