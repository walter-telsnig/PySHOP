import pandas as pd

starttime           =   pd.Timestamp(2023,1,1)
endtime             =   pd.Timestamp(2024,1,1)

use_tactical_limits =   True

timeunit            = "hour"
resolution          = 1

price_curve = "HPFC_Budget_2023.xlsx"


########################################################################################################################
# Fragant Tests
########################################################################################################################

F1 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : True, \
           "add_to_title"         : "MIP_both_limits",
           "MIP"                  : True}

F2 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : True, \
           "add_to_title"         : "MIP_head",
           "MIP"                  : True}

F3 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : False, \
           "add_to_title"         : "MIP_tac",
           "MIP"                  : True}

F4 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : False, \
           "add_to_title"         : "MIP_no_limit",
           "MIP"                  : True}

F5 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : True, \
           "add_to_title"         : "both_limits",
           "MIP"                  : False}

F6 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : True, \
           "add_to_title"         : "head",
           "MIP"                  : False}

F7 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : False, \
           "add_to_title"         : "tac",
           "MIP"                  : False}

F8 = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : False, \
           "add_to_title"         : "no_limit",
           "MIP"                  : False}




########################################################################################################################
# Fragant (big Haselstein) Tests
########################################################################################################################

F1b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : True, \
           "add_to_title"         : "MIP_both_limits",
           "MIP"                  : True}

F2b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : True, \
           "add_to_title"         : "MIP_head",
           "MIP"                  : True}

F3b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : False, \
           "add_to_title"         : "MIP_tac",
           "MIP"                  : True}

F4b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : False, \
           "add_to_title"         : "MIP_no_limit",
           "MIP"                  : True}

F5b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : True, \
           "add_to_title"         : "both_limits",
           "MIP"                  : False}

F6b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : True, \
           "add_to_title"         : "head",
           "MIP"                  : False}

F7b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : True, \
           "use_head_constr"      : False, \
           "add_to_title"         : "tac",
           "MIP"                  : False}

F8b = {"topology"             : "Fragant_big", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : False, \
           "use_head_constr"      : False, \
           "add_to_title"         : "no_limit",
           "MIP"                  : False}


########################################################################################################################
# Forstsee: Pump Evaluation
########################################################################################################################

Forstsee_HPFC_2021 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2021,1,1), \
           "endtime"              : pd.Timestamp(2022,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "HPFC_AT_2021.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_HPFC_2021_nP = {"topology"             : "Forstsee_no_pump", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2021,1,1), \
           "endtime"              : pd.Timestamp(2022,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "HPFC_AT_2021.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_HPFC_2023 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_HPFC_2023_nP = {"topology"             : "Forstsee_no_pump", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_Budget_HPFC_2023 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "Budget",
           "MIP"                  : False}

Forstsee_Budget_HPFC_2023_nP = {"topology"             : "Forstsee_no_pump", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,1,1), \
           "endtime"              : pd.Timestamp(2024,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2023.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "Budget",
           "MIP"                  : False}

Forstsee_HPFC_2025 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2025,1,1), \
           "endtime"              : pd.Timestamp(2026,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "HPFC_AT_2025.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_HPFC_2025_nP = {"topology"             : "Forstsee_no_pump", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2025,1,1), \
           "endtime"              : pd.Timestamp(2026,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "HPFC_AT_2025.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_Budget_HPFC_2025 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2025,1,1), \
           "endtime"              : pd.Timestamp(2026,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2025.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "Budget",
           "MIP"                  : False}

Forstsee_Budget_HPFC_2025_nP = {"topology"             : "Forstsee_no_pump", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2025,1,1), \
           "endtime"              : pd.Timestamp(2026,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Budget_HPFC_AT_2025.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "Budget",
           "MIP"                  : False}

Forstsee_Brainpool_2027 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2027,1,1), \
           "endtime"              : pd.Timestamp(2028,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Brainpool_AT_2027.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee_Brainpool_2027_nP = {"topology"             : "Forstsee_no_pump", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2027,1,1), \
           "endtime"              : pd.Timestamp(2028,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Brainpool_AT_2027.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}


















Koralpe = {"topology"             : "Koralpe", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : endtime, \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Koralpe_long = {"topology"             : "Koralpe", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2023,5,1), \
           "endtime"              : pd.Timestamp(2025,8,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Freibach = {"topology"             : "Freibach", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : endtime, \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : endtime, \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Forstsee2 = {"topology"             : "Forstsee", \
           "special_condition"    : "", \
           "starttime"            : pd.Timestamp(2019,1,1), \
           "endtime"              : pd.Timestamp(2020,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : "Spot_2019.xlsx", \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Kamering = {"topology"             : "Kamering", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : endtime, \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Malta = {"topology"             : "Malta", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_H = {"topology"             : "Fragant", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_noH1 = {"topology"             : "Fragant_no_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : endtime, \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_noH2 = {"topology"             : "Fragant_no_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : endtime, \
           "timeunit"             : "minute", \
           "resolution"           : 10, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_H1 = {"topology"             : "Fragant_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 15, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_H2 = {"topology"             : "Fragant_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 10, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_H3 = {"topology"             : "Fragant_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 5, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}


Fragant_H4 = {"topology"             : "Fragant_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 1, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_H5 = {"topology"             : "Fragant_Haselstein", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_Hb1 = {"topology"             : "Fragant_Haselstein_big", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 15, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_Hb2 = {"topology"             : "Fragant_Haselstein_big", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 10, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_Hb3 = {"topology"             : "Fragant_Haselstein_big", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 5, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}


Fragant_Hb4 = {"topology"             : "Fragant_Haselstein_big", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : "minute", \
           "resolution"           : 1, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Fragant_Hb5 = {"topology"             : "Fragant_Haselstein_big", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,2,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Koralpe_full = {"topology"        : "Koralpe_full", \
           "special_condition"    : "Koralpe_23_24", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2025,1,1), \
           "timeunit"             : timeunit, \
           "resolution"           : resolution, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Malta_m1 = {"topology"             : "Malta", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,1,7), \
           "timeunit"             : "minute", \
           "resolution"           : 15, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Malta_m2 = {"topology"             : "Malta", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,1,7), \
           "timeunit"             : "minute", \
           "resolution"           : 10, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Malta_m3 = {"topology"             : "Malta", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,1,7), \
           "timeunit"             : "minute", \
           "resolution"           : 5, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}

Malta_m4 = {"topology"             : "Malta", \
           "special_condition"    : "", \
           "starttime"            : starttime, \
           "endtime"              : pd.Timestamp(2023,1,7), \
           "timeunit"             : "minute", \
           "resolution"           : 1, \
           "price_curve"          : price_curve, \
           "use_tactical_limits"  : use_tactical_limits, \
           "use_head_constr"      : use_head_constr, \
           "add_to_title"         : "",
           "MIP"                  : False}
