from TOP_LEVEL_as_function import *
from Tasks import *


#Tasks = [Fragant_noH2,
#         Fragant_H1,Fragant_H2,Fragant_H3,Fragant_H4,Fragant_H5,Fragant_Hb1,Fragant_Hb2,Fragant_Hb3,Fragant_Hb4,Fragant_Hb5,
#         Koralpe_full,Malta_m1,Malta_m2,Malta_m3,Malta_m4]

#Koralpe, Koralpe_long, Freibach,Forstsee,Forstsee2,Kamering,Malta,Fragant,Fragant_H,Fragant_noH1

#Tasks = [Forstsee_HPFC_2021,Forstsee_HPFC_2021_nP,Forstsee_HPFC_2023,Forstsee_HPFC_2023_nP,Forstsee_Budget_HPFC_2023,Forstsee_Budget_HPFC_2023_nP,
#         Forstsee_HPFC_2025,Forstsee_HPFC_2025_nP,Forstsee_Budget_HPFC_2025,Forstsee_Budget_HPFC_2025_nP,Forstsee_Brainpool_2027,Forstsee_Brainpool_2027_nP]

Tasks = [F1,F2,F3,F4,F5,F6,F7,F8]
#Tasks = [F1b,F2b,F3b,F4b,F5b,F6b,F7b,F8b]

total_run_start = time.time()

for d in Tasks:

    print("Current task:")
    print(d)

    run_optimization(d["topology"], d["special_condition"],d["starttime"],d["endtime"],d["timeunit"],d["resolution"],
                     d["price_curve"],d["use_tactical_limits"],d["add_to_title"],d["MIP"])

    runtime = (time.time() - total_run_start) / 60
    print("# Elapsed time: " + "{:.2f}".format(runtime) + " min")

runtime = (time.time() - total_run_start) / 60
print("# Finished after " + "{:.2f}".format(runtime) + " min")