from pyshop import ShopSession
from Topologies import *
from Inflow import *
from special_conditions import *
from save_results import *
from Misc import *

run_start = time.time()

path = 'C:/Users/baumga1/Desktop/ASCII LT/'


case = "MALLT"
#for case in ["FRALT","MALLT","KORLT","FRELT","KAMLT"]:

shop = ShopSession(license_path='C:/pySHOP/License')

f1 = "powelsrv_"+case+".ascii"
shop.read_ascii_file(path + f1)



if not case == "KAMLT":
    f2 = case+"_extra_data.ascii"
    shop.read_ascii_file(path + f2)

shop =read_command_file(shop,path + "powelsrv_cmd.txt" )

discharge_group_GOE_out = shop.model.discharge_group.add_object("Out_of_Goesskar")
discharge_group_GOE_out.connect_to(shop.model.plant["DMH(4701)"])
discharge_group_GOE_out.connect_to(shop.model.plant["PuDRP(796)"])

discharge_group_GOE_in = shop.model.discharge_group.add_object("In_to_Goesskar")
discharge_group_GOE_in.connect_to(shop.model.plant["PuDMH(6581)"])
discharge_group_GOE_in.connect_to(shop.model.plant["DRP(4697)"])


shop.model.discharge_group.Out_of_Goesskar.max_discharge_m3s.set(80)
shop.model.discharge_group.In_to_Goesskar.max_discharge_m3s.set(80)



shop.dump_pyshop(path + "python_" + case +".py")


#convert_vol_to_head([0.712037],"Galgenbichl")

########################################################################################################################
print("Starting optimization")
run_opt(shop,run_start,save_path=path,n_iterations1=3,n_iterations2=2)
save_results(shop, path, path + "/Detail/")