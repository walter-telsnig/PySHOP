from Topologies import *
from save_results import *
from Availability import *
from pyshop import ShopSession
from price_comparison import *

########################################################################################################################
# Longterm
########################################################################################################################
today = pd.Timestamp.today().floor('D')

starttime = today + pd.Timedelta(1,unit='D')
endtime = pd.Timestamp(today.year+1,1,1)

time_unit = "hour"
time_resolution = { "Freibach": 1,
                    "Kamering": 1,
                    "Koralpe": 1,
                    "Malta": 1,
                    "Fragant": 1}

iterations = {  "Freibach": {   "full": 5,
                                "iter": 3},
                "Kamering":  {   "full": 5,
                                "iter": 3},
                "Koralpe":  {   "full": 5,
                                "iter": 3},
                "Malta":  {   "full": 3,
                                "iter": 2},
                "Fragant":  {   "full": 3,
                                "iter": 2}}

mip_gap = { "Freibach": 0.0001,
            "Kamering": 0.001,      #0.0001
            "Koralpe":  0.0001,
            "Malta":    0.01,
            "Fragant":  0.01}


if True:
    print("Updating revision data")
    update_revisions()
    #Longterm revision overview
    revision_overview(starttime,endtime,Short_Term=False)
    #Shortterm revision overview
    revision_overview(starttime,starttime + pd.Timedelta(7,unit="D") + pd.Timedelta(1,unit="H"),Short_Term=True)

LT_start = time.time()
use_montel = False

correct_reservoir_start_level_file()

for topology in ["Malta","Malta","Koralpe","Kamering","Freibach","Fragant"]:

    file_path_root, file_path_detail = set_path("/LT/" + create_date_string(starttime) + "/" + topology)

    current_time_resolution = time_resolution[topology]

    shop = ShopSession(license_path='C:/pySHOP/License')
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit=time_unit,
                             timeresolution=pd.Series(index=[starttime],data=[current_time_resolution]))

    print("Longterm Optimization: ".ljust(30) + topology.rjust(30))
    print("Start date:".ljust(30) + str(starttime).rjust(30))
    print("End date:".ljust(30) + str(endtime).rjust(30))

    shop = load_topology(shop,topology,use_tactical_limits=True,MIP=True)
    shop = get_res_start_levels(shop)
    shop = get_inflow(shop)
    shop = load_price_data(shop,montel=use_montel)
    shop = load_revisions(shop)


    shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")
    #shop.model.global_settings.global_settings.solver_algorithm.set("primal")

    #shop.model.global_settings.global_settings.ramp_code.set(1)
    #shop.model.global_settings.global_settings.bypass_loss.set(1)
    #shop.model.global_settings.global_settings.time_delay_unit.set("MINUTE")


    #if topology in ["Freibach","Kamering","Korlape","Fragant"]:
    #    shop.model.global_settings.global_settings.universal_mip.set(1)
    #else:
    #    shop.model.global_settings.global_settings.universal_mip.set(0)

    shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

    #shop.dump_pyshop(file_path_root + "code.py")

    run_opt(shop, run_start=time.time(), save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                                   n_iterations2=iterations[topology]["iter"])

    shop.dump_yaml(file_path_root+"results.yaml")
    save_results(shop, file_path_root, file_path_detail,topology)

plot_price_comparison()
runtime = (time.time() - LT_start)/60
print("Total runtime: " + "{:.2f}".format(runtime) + " min\n")