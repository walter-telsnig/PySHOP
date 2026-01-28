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
special_conditions = "Fragant_Stillstand_2024"#"Fragant_Normal_2024"#  #

today = pd.Timestamp.today().floor('D')

starttime = pd.Timestamp(2024,1,1)
endtime = pd.Timestamp(2025,1,1)

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

file_path_root, file_path_detail = set_path("/Bewertung/Stillstand_Fragant/"+special_conditions+"/"+ create_date_string(starttime) + "/" + topology)

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
#shop = get_res_start_levels(shop)
#shop = get_inflow(shop)
shop = load_price_data(shop,montel=use_montel)
shop = load_revisions(shop)

shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")

shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

shop = load_special_conditions(shop, special_conditions)

print("Start optimization")
run_opt(shop, run_start=time.time(), save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                               n_iterations2=iterations[topology]["iter"])

shop.dump_yaml(file_path_root+"results.yaml")
save_results(shop, file_path_root, file_path_detail,topology)

plot_price_comparison()
runtime = (time.time() - LT_start)/60
print("Total runtime: " + "{:.2f}".format(runtime) + " min\n")

