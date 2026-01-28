from Topologies import *
from save_results import *
from Availability import *
from heatmaps import *
from pyshop import ShopSession
from price_comparison import *

iterations = {  "Freibach": {   "full": 5,
                                "iter": 3},
                "Kamering":  {   "full": 5,
                                "iter": 3},
                "Koralpe":  {   "full": 5,
                                "iter": 3},
                "Malta":  {   "full": 5,
                                "iter": 3},
                "Fragant":  {   "full": 5,
                                "iter": 3}}

mip_gap = { "Freibach": 0.018,
            "Kamering": 0.0001,
            "Koralpe":  0.0005,
            "Malta":    0.002,
            "Fragant":  0.001}

########################################################################################################################
# Shortterm
########################################################################################################################

today = pd.Timestamp.today().floor('D')
starttime = today + pd.Timedelta(1,unit='D')
endtime = starttime + pd.Timedelta(7,unit="D")# + pd.Timedelta(1,unit="H")

use_montel = True
n_exaa = 1

ST_start = time.time()

for topology in ["Fragant","Freibach","Kamering","Koralpe","Malta"]:#]:

    file_path_root, file_path_detail = set_path("/ST/" + create_date_string(starttime) + "/" + topology)

    shop = ShopSession(license_path='C:/pySHOP/License')
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit="hour",
                             timeresolution=pd.Series(index=[starttime],data=[1]))

    print("Shortterm Optimization: ".ljust(30) + topology.rjust(30))
    print("Start date:".ljust(30) + str(starttime).rjust(30))
    print("End date:".ljust(30) + str(endtime).rjust(30))

    shop = load_topology(shop,topology,use_tactical_limits=True,MIP=True)
    shop = get_res_start_levels(shop)
    shop = get_inflow(shop,Short_Term=True)
    shop = load_price_data(shop, montel=use_montel,n_exaa=n_exaa)
    shop = set_res_window(shop,file_path_root, topology)
    shop = load_revisions(shop)

    shop = read_command_file(shop, "C:/Users/baumga1/Desktop/ASCII LT/powelsrv_cmd.txt")
    #shop.model.global_settings.global_settings.solver_algorithm.set("primal")

    if topology in ["Freibach", "Kamering", "Korlape", "Fragant"]:
        shop.model.global_settings.global_settings.universal_mip.set(1)
    else:
        shop.model.global_settings.global_settings.universal_mip.set(0)

    shop.model.global_settings.global_settings.mipgap_rel.set(mip_gap[topology])

    shop.model.global_settings.global_settings.ramp_code.set(1)
    shop.model.global_settings.global_settings.bypass_loss.set(1)
    shop.model.global_settings.global_settings.time_delay_unit.set("MINUTE")

    #shop.dump_pyshop(file_path_root + "code.py")

    run_start = time.time()
    run_opt(shop, run_start=run_start, save_path=file_path_root, n_iterations1=iterations[topology]["full"],
                                                                 n_iterations2=iterations[topology]["iter"])

    shop.dump_yaml(file_path_root+"results.yaml")
    save_results(shop, file_path_root, file_path_detail,topology,Short_Term=True)

for PP in ["KOR","FRE","KAM","DMH","DRP","FE"]:
    create_heatmap(PP,n_exaa=n_exaa)

plot_price_comparison(n_exaa=n_exaa)
runtime = (time.time() - ST_start)/60
print("Total runtime: " + "{:.2f}".format(runtime) + " min\n")


