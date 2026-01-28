import pandas as pd
import numpy as np

file = "C:/pySHOP/Input/PowerPlants.xlsx"

def get_Forstsee_generator(i):
    df = pd.read_excel(file, sheet_name="FOR_G"+str(i))
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Forstsee_turbine(i):

    df = pd.read_excel(file, sheet_name="FOR_T"+str(i))
    flow = df["Flow"].values
    E1 = df[165].values

    return flow, E1

def get_Forstsee_generator_alt():

    df = pd.read_excel(file, sheet_name="FOR_G2_alt")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Forstsee_turbine_alt():

    df = pd.read_excel(file, sheet_name="FOR_T2_alt")
    flow = df["Flow"].values
    E1 = df[165.60].values
    E2 = df[160.47].values
    E3 = df[155.33].values
    E4 = df[150.19].values
    E5 = df[145.02].values

    return flow, E1, E2, E3, E4, E5

def get_Haselstein_generator():
    df = pd.read_excel(file, sheet_name="HA_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Haselstein_turbine():

    df = pd.read_excel(file, sheet_name="HA_T")
    flow = df["Flow"].values
    E1 = df[260].values

    return flow, E1


def get_DMU_generator():

    df = pd.read_excel(file, sheet_name="DMU_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_DMU_turbine():

    df = pd.read_excel(file, sheet_name="DMU_T")
    flow = df["Flow"].values
    E1 = df[41].values
    E2 = df[44.7].values
    E3 = df[46].values

    return flow, E1, E2, E3

def get_DMH_generator():

    df = pd.read_excel(file, sheet_name="DMH_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_DMH_turbine():

    df = pd.read_excel(file, sheet_name="DMH_T")
    flow = df["Flow"].values
    E1 = df[1030].values
    E2 = df[1105].values

    return flow, E1, E2

def get_DRP_generator():

    df = pd.read_excel(file, sheet_name="DRP_G1")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_DRP_turbine():

    df = pd.read_excel(file, sheet_name="DRP_T1")
    flow = df["Flow"].values
    E1 = df[600].values

    return flow, E1

def get_DMO_generator():

    df = pd.read_excel(file, sheet_name="DMO_G1")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_KOLB_turbine():

    df = pd.read_excel(file, sheet_name="KOLB_T")
    flow = df["Flow"].values
    E1 = df[105].values

    return flow, E1

def get_KOLB_generator():

    df = pd.read_excel(file, sheet_name="KOLB_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_DMO_turbine():

    df = pd.read_excel(file, sheet_name="DMO_T1")
    flow = df["Flow"].values
    E1 = df[53].values
    E2 = df[61.45].values
    E3 = df[69.9].values
    E4 = df[78.35].values
    E5 = df[86.8].values
    E6 = df[95.25].values
    E7 = df[103.7].values
    E8 = df[112.15].values
    E9 = df[120.6].values
    E10 = df[129.05].values
    E11 = df[137.5].values
    E12 = df[145.95].values
    E13 = df[154.4].values
    E14 = df[162.85].values
    E15 = df[171.3].values
    E16 = df[179.75].values
    E17 = df[188.2].values
    E18 = df[196.65].values
    E19 = df[205.1].values
    E20 = df[213.55].values
    E21 = df[222].values

    return flow, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21

def get_Kamering_generator():

    df = pd.read_excel(file, sheet_name="KA_G1")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Kamering_turbine():

    df = pd.read_excel(file, sheet_name="KA_T1")
    flow = df["Flow"].values
    E1 = df[155].values

    return flow, E1

def get_Freibach_generator():

    df = pd.read_excel(file, sheet_name="FB_G1")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Freibach_turbine():

    df = pd.read_excel(file, sheet_name="FB_T1")
    flow = df["Flow"].values
    E1 = df[324].values

    return flow, E1


def get_Koralpe_generator(num):

    df = pd.read_excel(file, sheet_name="KO_G"+str(num))
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Koralpe_turbine(num):

    df = pd.read_excel(file, sheet_name="KO_T"+str(num))
    flow = df["Flow"].values
    if num == 1:
        E1 = df[660].values
        E2 = df[700].values
        E3 = df[735.5].values

        return flow, E1, E2, E3
    elif num == 2:
        E = df[731].values
        return flow, E
    else:
        print("get_Koralpe_turbine(num) ... num not defined.")


def get_Zirknitz_generator():

    df = pd.read_excel(file, sheet_name="ZN_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Zirknitz_turbine():

    df = pd.read_excel(file, sheet_name="ZN_T")
    flow = df["Flow"].values
    E1 = df[605].values
    E2 = df[660].values
    E3 = df[688].values

    return flow, E1, E2, E3

def get_Feldsee_generator():

    df = pd.read_excel(file, sheet_name="FS_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Feldsee_turbine():

    df = pd.read_excel(file, sheet_name="FS_T")
    flow = df["Flow"].values
    E1 = df[501].values
    E2 = df[526].values
    E3 = df[546].values

    return flow, E1, E2, E3

def get_Wurten_generator(num):

    df = pd.read_excel(file, sheet_name="WU_G"+str(num))
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Wurten_turbine(num):

    df = pd.read_excel(file, sheet_name="WU_T"+str(num))
    flow = df["Flow"].values
    E1 = df[469].values


    return flow, E1

def get_Woella_generator():

    df = pd.read_excel(file, sheet_name="WO_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Woella_turbine():

    df = pd.read_excel(file, sheet_name="WO_T")
    flow = df["Flow"].values
    E1 = df[311].values

    return flow, E1

def get_AF_generator(num):

    df = pd.read_excel(file, sheet_name="AF_G"+str(num))
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_AF_turbine(num):

    df = pd.read_excel(file, sheet_name="AF_T"+str(num))
    flow = df["Flow"].values
    E1 = df[475].values
    E2 = df[480].values
    E3 = df[485].values

    return flow, E1, E2, E3

def get_Oschenik_generator(num):

    df = pd.read_excel(file, sheet_name="OS_G"+str(num))
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Oschenik_generator_alt(num):

    df = pd.read_excel(file, sheet_name="OS_G"+str(num)+"_alt")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Oschenik_turbine(num):

    df = pd.read_excel(file, sheet_name="OS_T"+str(num))
    flow = df["Flow"].values
    E1 = df[1100].values
    E2 = df[1105].values
    E3 = df[1110].values

    return flow, E1, E2, E3

def get_Oschenik_turbine1():

    df = pd.read_excel(file, sheet_name="OS_T1")
    flow = df["Flow"].values
    E1 = df[1044].values
    E2 = df[1045].values
    E3 = df[1100].values
    E4 = df[1105].values
    E5 = df[1110].values

    mask1 = np.where(~np.isnan(E1))
    mask2 = np.where(~np.isnan(E2))
    mask3 = np.where(~np.isnan(E3))
    mask4 = np.where(~np.isnan(E4))
    mask5 = np.where(~np.isnan(E5))

    F1 = flow[mask1]
    F2 = flow[mask2]
    F3 = flow[mask3]
    F4 = flow[mask4]
    F5 = flow[mask5]

    E1 = E1[mask1]
    E2 = E2[mask2]
    E3 = E3[mask3]
    E4 = E4[mask4]
    E5 = E5[mask5]

    return F1, F2, F3, F4, F5, E1, E2, E3, E4, E5

# new generator and turbine PSKW Grosssee - Stufe Brettsee
def get_Brettsee_generator():

    df = pd.read_excel(file, sheet_name="BS_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Brettsee_turbine():

    df = pd.read_excel(file, sheet_name="BS_T")
    flow = df["Flow"].values
    E1 = df[340].values
    E2 = df[345].values
    E3 = df[349].values

    return flow, E1, E2, E3

def get_Kegelesee_generator():

    df = pd.read_excel(file, sheet_name="KS_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Kegelesee_turbine():

    df = pd.read_excel(file, sheet_name="KS_T")
    flow = df["Flow"].values
    E1 = df[215].values
    E2 = df[220].values
    E3 = df[225].values

    return flow, E1, E2, E3

def get_Bernegger_generator():

    df = pd.read_excel(file, sheet_name="BN_G")
    g_eff = df["Efficiency"].values
    g_MW = df["MW"].values

    return g_eff, g_MW

def get_Bernegger_turbine():

    df = pd.read_excel(file, sheet_name="BN_T")
    flow = df["Flow"].values
    E1 = df[600].values
    E2 = df[630].values
    E3 = df[660].values

    return flow, E1, E2, E3