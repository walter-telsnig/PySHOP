from save_results import *
from Topologies import *
from Availability import *
from pyshop import ShopSession
from price_comparison import *
from special_conditions import *
from Inflow import *

# Scenario for O3 + 5 MW
########################################################################################################################
# Longterm
########################################################################################################################
price_curve = ""

topology = "Fragant_O3_alt"
special_conditions = ""

price_curve = "HPFC_AT_2025-2028_26_02_2024.xlsx"

today = pd.Timestamp.today().floor('D')

starttime = pd.Timestamp(2025,1,1)
endtime = pd.Timestamp(2026,1,1)

time_unit = "hour"
time_resolution = {"Fragant_O3_alt": 1}

iterations = {"Fragant_O3_alt":  {"full": 3,
                           "iter": 2}}

mip_gap = {"Fragant_O3_alt":  0.01}

LT_start = time.time()


file_path_root, file_path_detail = set_path("/Bewertung/O3_plus_5MW/" + topology + "/" +create_date_string(starttime) + "/")

current_time_resolution = time_resolution[topology]

shop = ShopSession(license_path='C:/pySHOP/License')
shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=time_unit,
                         timeresolution=pd.Series(index=[starttime],data=[current_time_resolution]))

print("Longterm Optimization: ".ljust(30) + topology.rjust(30))
print("Start date:".ljust(30) + str(starttime).rjust(30))
print("End date:".ljust(30) + str(endtime).rjust(30))

shop = load_topology(shop,topology,use_tactical_limits=True,MIP=True)
shop = set_res_start_level(shop,updated_start_level={})
shop = load_inflow(shop, ignore=[])
shop = load_market_data(shop,file=price_curve)
#shop = load_revisions(shop)

shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")

shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

#shop = load_special_conditions(shop, special_conditions)

print("Start optimization")
run_opt(shop, run_start=time.time(), save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                               n_iterations2=iterations[topology]["iter"])

shop.dump_yaml(file_path_root+"results.yaml")
save_results(shop, file_path_root, file_path_detail,topology)

#plot_price_comparison()
runtime = (time.time() - LT_start)/60
print("Total runtime: " + "{:.2f}".format(runtime) + " min\n")

