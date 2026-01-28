import pandas as pd

from PowerPlants import *
from Reservoirs import *
#from Outdated.Plots_old import *

def load_topology(shop,topology,use_tactical_limits=True,ramp_penalty=1e20, ramp_value=4,MIP=False):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    if topology == "Fragant":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Grosssee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Feldsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woella(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        shop = add_bypass_gate_Haselstein(shop)
        shop = add_bypass_gate_Woella(shop)
        #shop = add_bypass_gate_Goessnitz(shop)

        #shop = add_bypass_gate_Grosssee(shop)
        #shop = add_bypass_gate_Feldsee(shop)
        #shop = add_bypass_gate_Wurten(shop)
        #shop = add_bypass_gate_Oschenik(shop)
        #shop = add_bypass_gate_Innerfragant(shop)

        Gate_Haselstein = shop.model.gate.Gate_Haselstein
        Gate_Woella = shop.model.gate.Gate_Woella
        #Gate_Goessnitz = shop.model.gate.Gate_Goessnitz

        #Gate_Grosssee = shop.model.gate.Gate_Grosssee
        #Gate_Feldsee = shop.model.gate.Gate_Feldsee
        #Gate_Wurten = shop.model.gate.Gate_Wurten
        #Gate_Oschenik = shop.model.gate.Gate_Oschenik
        #Gate_Innerfragant = shop.model.gate.Gate_Innerfragant

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Feldsee(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Haselstein(shop)
        shop = add_PP_Oschenik(shop)
        shop = add_PP_Oschenik_P1(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Woella(shop)
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Feldsee = shop.model.plant.Feldsee
        KW_Wurten = shop.model.plant.Wurten
        KW_Haselstein = shop.model.plant.Haselstein
        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P1 = shop.model.plant.Oschenik_P1
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Woella = shop.model.plant.Woella
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz

        KW_Oschenik_P1.maintenance_flag.set(1)

        if MIP:
            shop.model.plant.Oschenik_P1.mip_flag.set(1)
            shop.model.plant.Oschenik_P23.mip_flag.set(1)
            shop.model.plant.Haselstein.mip_flag.set(1)
            #shop.model.global_settings.global_settings.universal_mip.get()

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten)

        Feldsee.connect_to(KW_Feldsee)
        KW_Feldsee.connect_to(Wurten)

        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P1)
        KW_Oschenik_P1.connect_to(Haselstein)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten)

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        Woella.connect_to(KW_Woella)
        KW_Woella.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        #Goessnitz.connect_to(KW_Goessnitz)
        #KW_Goessnitz.connect_to(Moell)


        Haselstein.connect_to(Gate_Haselstein,connection_type='bypass')
        Gate_Haselstein.connect_to(Innerfragant)
        Woella.connect_to(Gate_Woella,connection_type='bypass')
        Gate_Woella.connect_to(Innerfragant)
        #Goessnitz.connect_to(Gate_Goessnitz,connection_type='bypass')
        #Gate_Goessnitz.connect_to(Moell)

        #Grosssee.connect_to(Gate_Grosssee,connection_type='bypass')
        #Gate_Grosssee.connect_to(Wurten)
        #Gate_Grosssee.connect_to(Moell)
        #Feldsee.connect_to(Gate_Feldsee,connection_type='bypass')
        #Gate_Feldsee.connect_to(Wurten)
        #Gate_Feldsee.connect_to(Moell)
        #Wurten.connect_to(Gate_Wurten,connection_type='bypass')
        #Gate_Wurten.connect_to(Innerfragant)
        #Gate_Wurten.connect_to(Moell)
        #Innerfragant.connect_to(Gate_Innerfragant,connection_type='bypass')
        #Gate_Innerfragant.connect_to(Moell)
        #Oschenik.connect_to(Gate_Oschenik,connection_type='bypass')
        #Gate_Oschenik.connect_to(Innerfragant)
        #Gate_Oschenik.connect_to(Moell)

        #grid_restriction_group = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP')
        #grid_restriction_group.max_p_limit.set(240)

        #grid_restriction_group.connect_to(KW_Oschenik)
        #grid_restriction_group.connect_to(KW_Oschenik_P1)
        #grid_restriction_group.connect_to(KW_Oschenik_P23)
        #grid_restriction_group.connect_to(KW_Wurten)
        #grid_restriction_group.connect_to(KW_Feldsee)
        #grid_restriction_group.connect_to(KW_Haselstein)


        #default = 9999
        #grid_restriction_group_all = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP_ALL')
        #grid_restriction_group_all.max_p_limit.set(pd.Series([default,280,default],
                                                   #index=[pd.Timestamp(2023,1,1),pd.Timestamp(2023,5,3,9), pd.Timestamp(2023,5,3,15)]))

        #grid_restriction_group_all.connect_to(KW_Zirknitz)
        #grid_restriction_group_all.connect_to(KW_Oschenik)
        #grid_restriction_group_all.connect_to(KW_Wurten)
        #grid_restriction_group_all.connect_to(KW_Feldsee)
        #grid_restriction_group_all.connect_to(KW_Haselstein)
        #grid_restriction_group_all.connect_to(KW_Auszerfragant)
        #grid_restriction_group_all.connect_to(KW_Woella)
        #grid_restriction_group_all.connect_to(KW_Goessnitz)

        return shop

    if topology == "Fragant_big":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Grosssee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Feldsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein_big(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woella(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein_big
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Feldsee(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Haselstein(shop)
        shop = add_PP_Oschenik(shop)
        shop = add_PP_Oschenik_P1(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Woella(shop)
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Feldsee = shop.model.plant.Feldsee
        KW_Wurten = shop.model.plant.Wurten
        KW_Haselstein = shop.model.plant.Haselstein
        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P1 = shop.model.plant.Oschenik_P1
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Woella = shop.model.plant.Woella
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz

        #KW_Oschenik_P1.maintenance_flag.set(1)

        #### MAINTANANCE FLAG
        KW_Zirknitz.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 3, 24), pd.Timestamp(2025, 4, 4)], name=0))
        KW_Wurten.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 3, 24), pd.Timestamp(2025, 4, 4)], name=0))
        KW_Oschenik_P23.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 3, 24), pd.Timestamp(2025, 4, 4)], name=0))

        KW_Oschenik_P23.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 3, 7), pd.Timestamp(2025, 10, 31)], name=0))
        KW_Feldsee.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 3, 24), pd.Timestamp(2025, 10, 23)], name=0))


        if MIP:
            shop.model.plant.Oschenik_P1.mip_flag.set(1)
            shop.model.plant.Oschenik_P23.mip_flag.set(1)
            shop.model.plant.Haselstein.mip_flag.set(1)
            #shop.model.global_settings.global_settings.universal_mip.get()

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten)

        Feldsee.connect_to(KW_Feldsee)
        KW_Feldsee.connect_to(Wurten)

        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P1)
        KW_Oschenik_P1.connect_to(Haselstein)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten)

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        Woella.connect_to(KW_Woella)
        KW_Woella.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        #energy_value = 100
        #Grosssee.energy_value_input.set(energy_value)
        #Feldsee.energy_value_input.set(energy_value)
        #Wurten.energy_value_input.set(energy_value)
        #Oschenik.energy_value_input.set(energy_value)
        #Innerfragant.energy_value_input.set(energy_value)
        #Haselstein.energy_value_input.set(energy_value)
        #Woella.energy_value_input.set(energy_value)
        #Goessnitz.energy_value_input.set(energy_value)
        #Moell.energy_value_input.set(energy_value)

        return shop

    if topology == "Fragant_750MW":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Grosssee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Feldsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten_big(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woella(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten_big = shop.model.reservoir.Wurten_big
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        shop = add_bypass_gate_Haselstein(shop)
        shop = add_bypass_gate_Woella(shop)

        Gate_Haselstein = shop.model.gate.Gate_Haselstein
        Gate_Woella = shop.model.gate.Gate_Woella

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Feldsee(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Haselstein(shop)
        shop = add_PP_Oschenik(shop)
        shop = add_PP_Oschenik_P1(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Woella(shop)
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Feldsee = shop.model.plant.Feldsee
        KW_Wurten = shop.model.plant.Wurten
        KW_Haselstein = shop.model.plant.Haselstein
        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P1 = shop.model.plant.Oschenik_P1
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Woella = shop.model.plant.Woella
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz

        KW_Oschenik_P1.maintenance_flag.set(1)

        if MIP:
            shop.model.plant.Oschenik_P1.mip_flag.set(1)
            shop.model.plant.Oschenik_P23.mip_flag.set(1)
            shop.model.plant.Haselstein.mip_flag.set(1)
            # shop.model.global_settings.global_settings.universal_mip.get()

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten_big)

        Feldsee.connect_to(KW_Feldsee)
        KW_Feldsee.connect_to(Wurten_big)

        Wurten_big.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P1)
        KW_Oschenik_P1.connect_to(Haselstein)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten_big)

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        Woella.connect_to(KW_Woella)
        KW_Woella.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        Haselstein.connect_to(Gate_Haselstein, connection_type='bypass')
        Gate_Haselstein.connect_to(Innerfragant)
        Woella.connect_to(Gate_Woella, connection_type='bypass')
        Gate_Woella.connect_to(Innerfragant)

        return shop

    if topology == "Fragant_no_Haselstein":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Grosssee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Feldsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woella(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Feldsee(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Oschenik(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Woella(shop)
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Feldsee = shop.model.plant.Feldsee
        KW_Wurten = shop.model.plant.Wurten
        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Woella = shop.model.plant.Woella
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz



        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten)

        Feldsee.connect_to(KW_Feldsee)
        KW_Feldsee.connect_to(Wurten)

        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten)

        Woella.connect_to(KW_Woella)
        KW_Woella.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        return shop

    elif topology == "Fragant_Haselstein":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein(shop, use_tactical_limits=use_tactical_limits)
        #shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        #Moell = shop.model.reservoir.Moell

        #shop = add_bypass_gate_Haselstein(shop)
        #shop = add_bypass_gate_Innerfragant(shop)

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Haselstein(shop)
        #shop = add_PP_Auszerfragant(shop)

        KW_Haselstein = shop.model.plant.Haselstein
        #KW_Auszerfragant = shop.model.plant.Auszerfragant

        if MIP:
            shop.model.plant.Haselstein.mip_flag.set(1)

        #Gate_Haselstein = shop.model.gate.Gate_Haselstein
        #Gate_Innerfragant = shop.model.gate.Gate_Innerfragant

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        #Innerfragant.connect_to(KW_Auszerfragant)
        #KW_Auszerfragant.connect_to(Moell)

        #Haselstein.connect_to(Gate_Haselstein, connection_type='bypass')
        #Gate_Haselstein.connect_to(Innerfragant)
        #Innerfragant.connect_to(Gate_Innerfragant, connection_type='bypass')
        #Gate_Innerfragant.connect_to(Moell)

        return shop

    elif topology == "Fragant_Haselstein_big":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein_big(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein_big
        Moell = shop.model.reservoir.Moell
        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Haselstein(shop)
        shop = add_PP_Auszerfragant(shop)

        KW_Haselstein = shop.model.plant.Haselstein
        KW_Auszerfragant = shop.model.plant.Auszerfragant

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        return shop

    elif topology == "Fragant_ramp":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Grosssee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Feldsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woella(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Feldsee(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Haselstein(shop)
        shop = add_PP_Oschenik(shop)
        shop = add_PP_Oschenik_P1(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Woella(shop)
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Feldsee = shop.model.plant.Feldsee
        KW_Wurten = shop.model.plant.Wurten
        KW_Haselstein = shop.model.plant.Haselstein
        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P1 = shop.model.plant.Oschenik_P1
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Woella = shop.model.plant.Woella
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz

        KW_Oschenik_P1.maintenance_flag.set(1)

        ####################################################################################################################
        # Ramping
        ####################################################################################################################
        #shop.model.global_settings.global_settings.production_ramp_penalty_cost.set(pd.Series([ramp_penalty], [starttime]))

        # 12,5% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([3.125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([3.125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([3.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([3.56], [starttime]))

        # 25% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([6.24], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([6.24], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([7.12], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([7.12], [starttime]))

        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1000], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1000], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1000], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1000], [starttime]))

        #discharge_group_AF = shop.model.discharge_group.add_object("discharge_group_AF")
        #discharge_group_AF.ramping_up_m3s.set(6.24)
        #discharge_group_AF.ramping_down_m3s.set(6.24)

        #discharge_group_GOE = shop.model.discharge_group.add_object("discharge_group_GOE")
        #discharge_group_GOE.ramping_up_m3s.set(7.12)
        #discharge_group_GOE.ramping_down_m3s.set(7.12)

        #discharge_group_AF.connect_to(KW_Auszerfragant)
        #discharge_group_GOE.connect_to(KW_Goessnitz)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten)

        Feldsee.connect_to(KW_Feldsee)
        KW_Feldsee.connect_to(Wurten)

        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P1)
        KW_Oschenik_P1.connect_to(Haselstein)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten)

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        Woella.connect_to(KW_Woella)
        KW_Woella.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        return shop

    elif topology == "Fragant_small_and_ramp":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Innerfragant = shop.model.reservoir.Innerfragant
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz

        ####################################################################################################################
        # Ramping
        ####################################################################################################################
        shop.model.global_settings.global_settings.production_ramp_penalty_cost.set(pd.Series([ramp_penalty], [starttime]))
        #shop.model.global_settings.global_settings.production_ramp_penalty_cost.set(1000)

        # 3,125% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([0.78125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([0.78125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.89], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.89], [starttime]))

        # 6,25% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1.5625], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1.5625], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1.78], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1.78], [starttime]))

        # 6,25% Rampe 1/4h
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([0.390625], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([0.390625], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.445], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.445], [starttime]))

        # 12,5% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([3.125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([3.125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([3.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([3.56], [starttime]))

        # 12,5% Ramp 1/4h
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([0.78125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([0.78125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.89], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.89], [starttime]))


        # 25% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([6.24], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([6.24], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([7.12], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([7.12], [starttime]))

        # 25% Ramp 1/4h
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1.56], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1.78], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1.78], [starttime]))

        # NEW - Scenario B4
        KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1.95], [starttime]))
        KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1.95], [starttime]))
        KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.85], [starttime]))
        KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.85], [starttime]))

        # NEW - Scenario B3
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([2.93], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([2.93], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1.28], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1.28], [starttime]))

        # NEW - Scenario B2
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([5.86], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([5.86], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([2.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([2.56], [starttime]))

        # NEW - Scenario B1
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([12.19], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([12.19], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([5.34], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([5.34], [starttime]))

        # NEW - Scenario C
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([24.38], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([24.38], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([10.68], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([10.68], [starttime]))

        # NEW - Scenario D
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([48.75], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([48.75], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([21.36], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([21.36], [starttime]))

        # NEW - Scenario E
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([73.58], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([73.58], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([32.12], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([32.12], [starttime]))

        # NEW - Scenario F
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([97.5], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([97.5], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([42.72], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([42.72], [starttime]))

        # NEW - Scenario F2
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([130], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([130], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([122.06], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([122.06], [starttime]))

        #  NEW - No ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1000], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1000], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1000], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1000], [starttime]))

        # ----------------------------------------------------------------------------------------
        # Discharge group 12,5% Ramp
        #discharge_group_AF = shop.model.discharge_group.add_object("discharge_group_AF")
        #discharge_group_AF.ramping_up_m3s.set(3.125)
        #discharge_group_AF.ramping_down_m3s.set(3.125)

        #discharge_group_GOE = shop.model.discharge_group.add_object("discharge_group_GOE")
        #discharge_group_GOE.ramping_up_m3s.set(3.56)
        #discharge_group_GOE.ramping_down_m3s.set(3.56)

        #discharge_group_AF.connect_to(KW_Auszerfragant)
        #discharge_group_GOE.connect_to(KW_Goessnitz)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        return shop

    elif topology == "Fragant_small_and_ramp_Os_Wu":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop,use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Oschenik = shop.model.reservoir.Oschenik
        Wurten = shop.model.reservoir.Wurten
        Innerfragant = shop.model.reservoir.Innerfragant
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Oschenik(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Auszerfragant(shop)
        shop = add_PP_Goessnitz(shop)

        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Wurten = shop.model.plant.Wurten
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        KW_Goessnitz = shop.model.plant.Goessnitz

        ####################################################################################################################
        # Ramping
        ####################################################################################################################
        shop.model.global_settings.global_settings.production_ramp_penalty_cost.set(pd.Series([ramp_penalty], [starttime]))
        #shop.model.global_settings.global_settings.production_ramp_penalty_cost.set(1000)

        # 3,125% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([0.78125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([0.78125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.89], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.89], [starttime]))

        # 6,25% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1.5625], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1.5625], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1.78], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1.78], [starttime]))

        # 6,25% Rampe 1/4h
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([0.390625], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([0.390625], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.445], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.445], [starttime]))

        # 12,5% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([3.125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([3.125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([3.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([3.56], [starttime]))

        # 12,5% Ramp 1/4h
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([0.78125], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([0.78125], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.89], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.89], [starttime]))


        # 25% Ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([6.24], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([6.24], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([7.12], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([7.12], [starttime]))

        # 25% Ramp 1/4h
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1.56], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1.78], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1.78], [starttime]))

        # NEW - Scenario B4
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1.95], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1.95], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([0.85], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([0.85], [starttime]))

        # NEW - Scenario B3
        KW_Auszerfragant.discharge_ramping_up.set(pd.Series([2.93], [starttime]))
        KW_Auszerfragant.discharge_ramping_down.set(pd.Series([2.93], [starttime]))
        KW_Goessnitz.discharge_ramping_up.set(pd.Series([1.28], [starttime]))
        KW_Goessnitz.discharge_ramping_down.set(pd.Series([1.28], [starttime]))

        # NEW - Scenario B2
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([5.86], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([5.86], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([2.56], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([2.56], [starttime]))

        # NEW - Scenario B1
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([12.19], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([12.19], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([5.34], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([5.34], [starttime]))

        # NEW - Scenario C
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([24.38], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([24.38], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([10.68], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([10.68], [starttime]))

        # NEW - Scenario D
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([48.75], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([48.75], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([21.36], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([21.36], [starttime]))

        # NEW - Scenario E
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([73.58], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([73.58], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([32.12], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([32.12], [starttime]))

        # NEW - Scenario F
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([97.5], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([97.5], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([42.72], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([42.72], [starttime]))

        # NEW - Scenario F2
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([130], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([130], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([122.06], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([122.06], [starttime]))

        #  NEW - No ramp
        #KW_Auszerfragant.discharge_ramping_up.set(pd.Series([1000], [starttime]))
        #KW_Auszerfragant.discharge_ramping_down.set(pd.Series([1000], [starttime]))
        #KW_Goessnitz.discharge_ramping_up.set(pd.Series([1000], [starttime]))
        #KW_Goessnitz.discharge_ramping_down.set(pd.Series([1000], [starttime]))

        # ----------------------------------------------------------------------------------------
        # Discharge group 12,5% Ramp
        #discharge_group_AF = shop.model.discharge_group.add_object("discharge_group_AF")
        #discharge_group_AF.ramping_up_m3s.set(3.125)
        #discharge_group_AF.ramping_down_m3s.set(3.125)

        #discharge_group_GOE = shop.model.discharge_group.add_object("discharge_group_GOE")
        #discharge_group_GOE.ramping_up_m3s.set(3.56)
        #discharge_group_GOE.ramping_down_m3s.set(3.56)

        #discharge_group_AF.connect_to(KW_Auszerfragant)
        #discharge_group_GOE.connect_to(KW_Goessnitz)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        return shop

    elif topology == "Kamering":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Wiederschwing(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)
        shop = add_gate_KAM_Drau(shop)

        Wiederschwing = shop.model.reservoir.Wiederschwing
        Drau = shop.model.reservoir.Drau
        Gate = shop.model.gate.Gate_KAM_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Kamering(shop)

        KW_Kamering = shop.model.plant.Kamering

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Wiederschwing.connect_to(KW_Kamering)
        KW_Kamering.connect_to(Drau)
        Wiederschwing.connect_to(Gate,connection_type='bypass')
        Gate.connect_to(Drau)

        return shop

    elif topology == "Freibach":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Freibach(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)
        shop = add_gate_FRE_Drau(shop)

        Freibach = shop.model.reservoir.Freibach
        Drau = shop.model.reservoir.Drau
        Gate = shop.model.gate.Gate_FRE_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Freibach(shop)

        KW_Freibach = shop.model.plant.Freibach

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Freibach.connect_to(KW_Freibach)
        KW_Freibach.connect_to(Drau)
        Freibach.connect_to(Gate,connection_type='bypass')
        Gate.connect_to(Drau)

        return shop

    elif topology == "Koralpe":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Soboth(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)
        shop = add_gate_SOB_Drau(shop)

        Soboth = shop.model.reservoir.Soboth
        Drau = shop.model.reservoir.Drau
        Gate = shop.model.gate.Gate_SOB_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Koralpe(shop)
        KW_Koralpe = shop.model.plant.Koralpe

        if MIP:
            shop.model.plant.Koralpe.mip_flag.set(1)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Soboth.connect_to(KW_Koralpe)
        KW_Koralpe.connect_to(Drau)
        Soboth.connect_to(Gate,connection_type='bypass')
        Gate.connect_to(Drau)

        return shop

    elif topology == "Forstsee":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Forstsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woerthersee(shop)

        Forstsee = shop.model.reservoir.Forstsee
        Woerthersee = shop.model.reservoir.Woerthersee

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Forstsee(shop)
        KW_Forstsee = shop.model.plant.Forstsee

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Forstsee.connect_to(KW_Forstsee)
        KW_Forstsee.connect_to(Woerthersee)

        return shop

    elif topology == "Forstsee_no_pump":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Forstsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woerthersee(shop)

        Forstsee = shop.model.reservoir.Forstsee
        Woerthersee = shop.model.reservoir.Woerthersee

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Forstsee(shop)
        KW_Forstsee = shop.model.plant.Forstsee

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Forstsee.connect_to(KW_Forstsee)
        KW_Forstsee.connect_to(Woerthersee)

        shop.model.pump.FOR_P1.maintenance_flag.set(1)

        return shop

    elif topology == "Koralpe_full":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Soboth_incl_dead_space(shop)
        shop = add_reservoir_Drau(shop)

        Soboth = shop.model.reservoir.Soboth
        Drau = shop.model.reservoir.Drau

        shop = add_gate_Soboth_Drau(shop)
        Gate = shop.model.gate.Gate_SOB_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Koralpe(shop)
        KW_Koralpe = shop.model.plant.Koralpe

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Soboth.connect_to(KW_Koralpe)
        Soboth.connect_to(Gate,connection_type='bypass')
        Gate.connect_to(Drau)
        KW_Koralpe.connect_to(Drau)

        return shop

    elif topology == "Koralpe_ramp":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Soboth(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)

        Soboth = shop.model.reservoir.Soboth
        Drau = shop.model.reservoir.Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Koralpe(shop)
        KW_Koralpe = shop.model.plant.Koralpe


        shop.model.global_settings.global_settings.production_ramp_penalty_cost.set(
            pd.Series([ramp_penalty], [starttime]))

        #KW_Koralpe.discharge_ramping_up.set(pd.Series([ramp_value], [starttime]))
        #KW_Koralpe.discharge_ramping_down.set(pd.Series([ramp_value], [starttime]))

        discharge_group = shop.model.discharge_group.add_object("discharge_group")
        discharge_group.ramping_up_m3s.set(1)
        discharge_group.ramping_down_m3s.set(1)
        discharge_group.connect_to(KW_Koralpe)

        # KOR.power_ramping_up.set(pd.Series([10], [starttime]))
        # KOR.power_ramping_down.set(pd.Series([10], [starttime]))

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Soboth.connect_to(KW_Koralpe)
        KW_Koralpe.connect_to(Drau)

        return shop

    elif topology == "Malta_Kolbnitz":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Koelnbrein(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Muehldorfersee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Galgenbichl(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goesskar(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Rottau(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kolbnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)

        #shop = add_tunnel_Galgenbichl_Goesskar(shop)
        shop = add_gate_Galgenbichl_Goesskar(shop)
        shop = add_gate_Muehldorfersee_Drau(shop)
        shop = add_gate_Koelnbrein_Drau(shop)
        shop = add_gate_Galgenbichl_Drau(shop)
        shop = add_gate_Goesskar_Drau(shop)
        shop = add_gate_Rottau_Drau(shop)
        shop = add_gate_Kolbnitz_Drau(shop)


        Koelnbrein = shop.model.reservoir.Koelnbrein
        Muehldorfersee = shop.model.reservoir.Muehldorfersee
        Galgenbichl = shop.model.reservoir.Galgenbichl
        Goesskar = shop.model.reservoir.Goesskar
        Rottau = shop.model.reservoir.Rottau
        Kolbnitz = shop.model.reservoir.Kolbnitz
        Drau = shop.model.reservoir.Drau

        #Tunnel = shop.model.tunnel.Tunnel_GAL_GOE
        Gate_GAL_GOE = shop.model.gate.Gate_GAL_GOE
        Gate_MUE = shop.model.gate.Gate_MUE_Drau
        Gate_KOE = shop.model.gate.Gate_KOE_Drau
        Gate_GAL = shop.model.gate.Gate_GAL_Drau
        Gate_GOE = shop.model.gate.Gate_GOE_Drau
        Gate_ROT = shop.model.gate.Gate_ROT_Drau
        Gate_KOLB = shop.model.gate.Gate_KOLB_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_DMO(shop)
        shop = add_PP_DRP(shop)
        shop = add_PP_DMH(shop)
        shop = add_PP_DMU(shop)
        shop = add_PP_KOLB(shop)

        KW_DMO = shop.model.plant.DMO
        KW_DRP = shop.model.plant.DRP
        KW_DMH = shop.model.plant.DMH
        KW_DMU = shop.model.plant.DMU
        KW_KOLB = shop.model.plant.KOLB

        if MIP:
            shop.model.plant.DMH.mip_flag.set(1)
            shop.model.plant.DRP.mip_flag.set(1)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Koelnbrein.connect_to(KW_DMO)
        KW_DMO.connect_to(Galgenbichl)

        Muehldorfersee.connect_to(KW_DRP)
        KW_DRP.connect_to(Goesskar)

        #Galgenbichl.connect_to(Tunnel)
        #Tunnel.connect_to(Goesskar)

        Galgenbichl.connect_to(Gate_GAL_GOE)
        Gate_GAL_GOE.connect_to(Goesskar)

        Goesskar.connect_to(KW_DMH)
        KW_DMH.connect_to(Rottau)

        Rottau.connect_to(KW_DMU)
        KW_DMU.connect_to(Drau)

        # Kolbnitz new
        Kolbnitz.connect_to(KW_KOLB)
        KW_KOLB.connect_to(Rottau)

        Koelnbrein.connect_to(Gate_KOE, connection_type='bypass')
        Muehldorfersee.connect_to(Gate_MUE,connection_type='bypass')
        Galgenbichl.connect_to(Gate_GAL,connection_type='bypass')
        Goesskar.connect_to(Gate_GOE,connection_type='bypass')
        Rottau.connect_to(Gate_ROT,connection_type='bypass')
        Kolbnitz.connect_to(Gate_KOLB,connection_type='bypass')

        #Gate_MUE.connect_to(Goesskar)
        Gate_MUE.connect_to(Drau)
        #Gate_KOE.connect_to(Galgenbichl)
        Gate_KOE.connect_to(Drau)
        Gate_GAL.connect_to(Drau)
        Gate_GOE.connect_to(Drau)
        Gate_ROT.connect_to(Drau)
        Gate_KOLB.connect_to(Drau)

        #pd.Series(schedule, index=date_range)
        default_110kV = 38.88
        default_220kV = 278.88

        # 110 kV
        grid_restriction_group_malta1 = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP_MALTA1')
        grid_restriction_group_malta1.max_p_limit.set(pd.Series([default_110kV,17,default_110kV],
                                                          index=[pd.Timestamp(2023,1,1),pd.Timestamp(2023,3,5,9), pd.Timestamp(2023,3,5,15)]))
        #grid_restriction_group_malta1.max_p_limit.set(default_110kV)

        #220 kV
        grid_restriction_group_malta2 = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP_MALTA2')
        grid_restriction_group_malta2.max_p_limit.set(default_220kV)

        grid_restriction_group_malta1.connect_to(KW_DMO)
        grid_restriction_group_malta1.connect_to(KW_DMU)

        grid_restriction_group_malta2.connect_to(KW_DMH)
        grid_restriction_group_malta2.connect_to(KW_DRP)

        return shop

    elif topology == "Malta":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Koelnbrein(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Muehldorfersee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Galgenbichl(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Goesskar(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Rottau(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)

        #shop = add_tunnel_Galgenbichl_Goesskar(shop)
        shop = add_gate_Galgenbichl_Goesskar(shop)
        shop = add_gate_Muehldorfersee_Drau(shop)
        shop = add_gate_Koelnbrein_Drau(shop)
        shop = add_gate_Galgenbichl_Drau(shop)
        shop = add_gate_Goesskar_Drau(shop)
        shop = add_gate_Rottau_Drau(shop)

        Koelnbrein = shop.model.reservoir.Koelnbrein
        Muehldorfersee = shop.model.reservoir.Muehldorfersee
        Galgenbichl = shop.model.reservoir.Galgenbichl
        Goesskar = shop.model.reservoir.Goesskar
        Rottau = shop.model.reservoir.Rottau
        Drau = shop.model.reservoir.Drau

        #Tunnel = shop.model.tunnel.Tunnel_GAL_GOE
        Gate_GAL_GOE = shop.model.gate.Gate_GAL_GOE
        Gate_MUE = shop.model.gate.Gate_MUE_Drau
        Gate_KOE = shop.model.gate.Gate_KOE_Drau
        Gate_GAL = shop.model.gate.Gate_GAL_Drau
        Gate_GOE = shop.model.gate.Gate_GOE_Drau
        Gate_ROT = shop.model.gate.Gate_ROT_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_DMO(shop)
        shop = add_PP_DRP(shop)
        shop = add_PP_DMH(shop)
        shop = add_PP_DMU(shop)

        KW_DMO = shop.model.plant.DMO
        KW_DRP = shop.model.plant.DRP
        KW_DMH = shop.model.plant.DMH
        KW_DMU = shop.model.plant.DMU

        if MIP:
            shop.model.plant.DMH.mip_flag.set(1)
            shop.model.plant.DRP.mip_flag.set(1)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Koelnbrein.connect_to(KW_DMO)
        KW_DMO.connect_to(Galgenbichl)

        Muehldorfersee.connect_to(KW_DRP)
        KW_DRP.connect_to(Goesskar)

        #Galgenbichl.connect_to(Tunnel)
        #Tunnel.connect_to(Goesskar)

        Galgenbichl.connect_to(Gate_GAL_GOE)
        Gate_GAL_GOE.connect_to(Goesskar)

        Goesskar.connect_to(KW_DMH)
        KW_DMH.connect_to(Rottau)

        Rottau.connect_to(KW_DMU)
        KW_DMU.connect_to(Drau)

        Koelnbrein.connect_to(Gate_KOE, connection_type='bypass')
        Muehldorfersee.connect_to(Gate_MUE,connection_type='bypass')
        Galgenbichl.connect_to(Gate_GAL,connection_type='bypass')
        Goesskar.connect_to(Gate_GOE,connection_type='bypass')
        Rottau.connect_to(Gate_ROT,connection_type='bypass')

        #Gate_MUE.connect_to(Goesskar)
        Gate_MUE.connect_to(Drau)
        #Gate_KOE.connect_to(Galgenbichl)
        Gate_KOE.connect_to(Drau)
        Gate_GAL.connect_to(Drau)
        Gate_GOE.connect_to(Drau)
        Gate_ROT.connect_to(Drau)

        #pd.Series(schedule, index=date_range)
        default_110kV = 38.88
        default_220kV = 278.88

        # 110 kV
        grid_restriction_group_malta1 = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP_MALTA1')
        grid_restriction_group_malta1.max_p_limit.set(pd.Series([default_110kV,17,default_110kV],
                                                          index=[pd.Timestamp(2023,1,1),pd.Timestamp(2023,3,5,9), pd.Timestamp(2023,3,5,15)]))
        #grid_restriction_group_malta1.max_p_limit.set(default_110kV)

        #220 kV
        grid_restriction_group_malta2 = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP_MALTA2')
        grid_restriction_group_malta2.max_p_limit.set(default_220kV)

        grid_restriction_group_malta1.connect_to(KW_DMO)
        grid_restriction_group_malta1.connect_to(KW_DMU)

        grid_restriction_group_malta2.connect_to(KW_DMH)
        grid_restriction_group_malta2.connect_to(KW_DRP)

        return shop

    elif topology == "Kolbnitz":

        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Kolbnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Rottau(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Drau(shop)

        shop = add_gate_Rottau_Drau(shop)

        Rottau = shop.model.reservoir.Rottau
        Kolbnitz = shop.model.reservoir.Kolbnitz
        Drau = shop.model.reservoir.Drau

        Gate_ROT = shop.model.gate.Gate_ROT_Drau

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_DMU(shop)
        shop = add_PP_KOLB(shop)

        KW_DMU = shop.model.plant.DMU
        KW_KOLB = shop.model.plant.KOLB

        if MIP:
            shop.model.plant.DMH.mip_flag.set(1)
            shop.model.plant.DRP.mip_flag.set(1)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Kolbnitz.connect_to(KW_KOLB)
        KW_KOLB.connect_to(Rottau)

        Rottau.connect_to(KW_DMU)
        KW_DMU.connect_to(Drau)

        Rottau.connect_to(Gate_ROT,connection_type='bypass')
        Gate_ROT.connect_to(Drau)

        return shop

    elif topology == "PSKW_Grosssee":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Zirmsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Brettsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Grosssee_adv(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kegelesee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        # Gates
        shop = add_gate_Zirmsee_Grosssee(shop)
        shop = add_gate_Brettsee_Grosssee(shop)
        shop = add_gate_Kegelesee_Moell(shop)

        Zirmsee = shop.model.reservoir.Zirmsee
        Brettsee = shop.model.reservoir.Brettsee
        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell

        Gate_Zirmsee = shop.model.gate.Gate_Zirmsee_Grosssee
        Gate_Brettsee = shop.model.gate.Gate_Brettsee_Grosssee
        Gate_Kegelesee = shop.model.gate.Gate_Kegelesee_Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################

        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Kegele(shop)
        #shop = add_PP_Kegele_pump(shop)
        #shop = add_PP_Brettsee(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Kegele = shop.model.plant.Kegele
        #KW_Brettsee = shop.model.plant.Brettsee

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Moell)

        #Zirmsee.connect_to(Gate_Zirmsee, connection_type='bypass')
        Zirmsee.connect_to(Gate_Zirmsee)
        Gate_Zirmsee.connect_to(Grosssee)
        # Step 2: Zirmsee.connect_to(KW_Brettsee)
        # Step 2: KW_Brettsee.connect_to(Moell)

        # TODO: Brettsee > KW_Brettsee > Möll
        #Brettsee.connect_to(Gate_Brettsee, connection_type='bypass')
        Brettsee.connect_to(Gate_Brettsee)
        Gate_Brettsee.connect_to(Grosssee)
        #Brettsee.connect_to(KW_Brettsee)
        #KW_Brettsee.connect_to(Moell)

        # TODO: Kegelesee > Pumpe Kegele > Großsee
        # (1) Kegele > Gate > Möll
        #Kegelesee.connect_to(Gate_Kegelesee)
        #Gate_Kegelesee.connect_to(Moell)
        # (2) Kegele > KW_Kegele > Grosssee
        Kegelesee.connect_to(KW_Kegele)
        KW_Kegele.connect_to(Grosssee)

        return shop

    elif topology =="Kegele_simple":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Grosssee_adv(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kegelesee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        # Gates
        shop = add_gate_Kegelesee_Moell(shop)

        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell

        Gate_Kegelesee = shop.model.gate.Gate_Kegelesee_Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################

        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Kegele_pump(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Kegele = shop.model.plant.Kegele

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Moell)

        # TODO: Kegelesee > Pumpe Kegele > Großsee
        # (1) Kegele > Gate > Möll
        #Kegelesee.connect_to(Gate_Kegelesee)
        #Gate_Kegelesee.connect_to(Moell)
        # (2) Kegele > KW_Kegele > Grosssee
        Grosssee.connect_to(KW_Kegele)
        KW_Kegele.connect_to(Kegelesee)
        #Kegelesee.connect_to(KW_Kegele)
        #KW_Kegele.connect_to(Grosssee)
        Kegelesee.connect_to(Gate_Kegelesee, connection_type='bypass')
        Gate_Kegelesee.connect_to(Moell)

        return shop

    elif topology =="Kegele_Brettsee_Zirmsee":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Zirmsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Brettsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Grosssee_adv(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kegelesee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        # Gates
        shop = add_gate_Kegelesee_Moell(shop)
        shop = add_gate_Zirmsee_Grosssee(shop)
        shop = add_gate_Brettsee_Grosssee(shop)

        Zirmsee = shop.model.reservoir.Zirmsee
        Brettsee = shop.model.reservoir.Brettsee
        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell

        Gate_Zirmsee = shop.model.gate.Gate_Zirmsee_Grosssee
        Gate_Brettsee = shop.model.gate.Gate_Brettsee_Grosssee
        Gate_Kegelesee = shop.model.gate.Gate_Kegelesee_Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################

        shop = add_PP_Zirknitz(shop)
        # Test Brettsee - shop = add_PP_Kegele_pump(shop)
        #shop = add_PP_Kegele(shop)
        shop = add_PP_Brettsee(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        # Test Brettsee - KW_Kegele = shop.model.plant.Kegele
        KW_Brettsee = shop.model.plant.Brettsee

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        # Grossee - KW Zirknitz - Möll
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Moell)

        # Kegelesee / KW Kegele
        # Kegelesee - KW Kegele (pump) - Grossee
        # Test Brettsee - Grosssee.connect_to(KW_Kegele)
        # Test Brettsee - KW_Kegele.connect_to(Kegelesee)
        # Overflow/Bypass Kegele > Moell
        Kegelesee.connect_to(Gate_Kegelesee, connection_type='bypass')
        Gate_Kegelesee.connect_to(Moell)
        # TODO: Grosssee > Turbine Kegele > Kegele

        # Brettsee - KW Brettsee - Kegelesee
        Brettsee.connect_to(KW_Brettsee)
        KW_Brettsee.connect_to(Kegelesee)
        # Overflow/Bypass Brettsee - Grosssee
        Brettsee.connect_to(Gate_Brettsee, connection_type='bypass')
        Gate_Brettsee.connect_to(Grosssee)
        # TODO: Brettsee > KW_Brettsee > Möll

        # old
        #Brettsee.connect_to(Gate_Brettsee)
        #Gate_Brettsee.connect_to(Grosssee)

        # DONE: Zirmsee > Gate Zirmsee > Grosssee
        Zirmsee.connect_to(Gate_Zirmsee)
        Gate_Zirmsee.connect_to(Grosssee)

        return shop

    elif topology =="Kegele_Brettsee_Zirmsee_2":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Zirmsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Brettsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Grosssee_adv(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kegelesee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        # Gates
        shop = add_gate_Kegelesee_Moell(shop)
        shop = add_gate_Zirmsee_Grosssee(shop)
        shop = add_gate_Brettsee_Grosssee(shop)

        Zirmsee = shop.model.reservoir.Zirmsee
        Brettsee = shop.model.reservoir.Brettsee
        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell

        Gate_Zirmsee = shop.model.gate.Gate_Zirmsee_Grosssee
        Gate_Brettsee = shop.model.gate.Gate_Brettsee_Grosssee
        Gate_Kegelesee = shop.model.gate.Gate_Kegelesee_Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################

        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Kegele(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Kegele = shop.model.plant.Kegele

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        # Grossee - KW Zirknitz - Möll
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Moell)

        # Kegelesee / KW Kegele
        # Kegelesee - KW Kegele (pump) - Grossee
        # Overflow/Bypass Kegele > Moell
        Grosssee.connect_to(KW_Kegele)
        KW_Kegele.connect_to(Kegelesee)
        Kegelesee.connect_to(Gate_Kegelesee, connection_type='bypass')
        Gate_Kegelesee.connect_to(Moell)

        # DONE: Zirmsee > Gate Zirmsee > Grosssee
        Zirmsee.connect_to(Gate_Zirmsee)
        Gate_Zirmsee.connect_to(Grosssee)

        return shop

    elif topology =="Kegele_Brettsee_Zirmsee_3":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Zirmsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Brettsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Grosssee_adv(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kegelesee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        # Gates
        shop = add_gate_Kegelesee_Moell(shop)
        shop = add_gate_Zirmsee_Grosssee(shop)
        shop = add_gate_Brettsee_Grosssee(shop)

        Zirmsee = shop.model.reservoir.Zirmsee
        Brettsee = shop.model.reservoir.Brettsee
        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell

        Gate_Zirmsee = shop.model.gate.Gate_Zirmsee_Grosssee
        Gate_Brettsee = shop.model.gate.Gate_Brettsee_Grosssee
        Gate_Kegelesee = shop.model.gate.Gate_Kegelesee_Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################

        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Brettsee(shop)
        shop = add_PP_Kegele(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Brettsee = shop.model.plant.Brettsee
        KW_Kegele = shop.model.plant.Kegele

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        # Grossee - KW Zirknitz - Möll
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Moell)

        # Kegelesee / KW Kegele
        # Overflow/Bypass Kegele > Moell
        Grosssee.connect_to(KW_Kegele)
        KW_Kegele.connect_to(Kegelesee)
        Kegelesee.connect_to(Gate_Kegelesee, connection_type='bypass')
        Gate_Kegelesee.connect_to(Moell)

        # Brettsee / KW Brettsee / Kegelesee
        # Overflow/Bypass Brettsee > Grosssee
        Brettsee.connect_to(KW_Brettsee)
        KW_Brettsee.connect_to(Kegelesee)
        Brettsee.connect_to(Gate_Brettsee, connection_type='bypass')
        Gate_Brettsee.connect_to(Grosssee)

        # DONE: Zirmsee > Gate Zirmsee > Grosssee
        Zirmsee.connect_to(Gate_Zirmsee)
        Gate_Zirmsee.connect_to(Grosssee)

        return shop

    elif topology =="Kegele_Brettsee_Zirmsee_4":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Zirmsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Brettsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Grosssee_adv(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Kegelesee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop, use_tactical_limits=use_tactical_limits)

        # Gates
        shop = add_gate_Kegelesee_Moell(shop)
        shop = add_gate_Zirmsee_Grosssee(shop)
        shop = add_gate_Brettsee_Grosssee(shop)
        shop = add_bypass_gate_Wurten(shop)

        Zirmsee = shop.model.reservoir.Zirmsee
        Brettsee = shop.model.reservoir.Brettsee
        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell
        Wurten = shop.model.reservoir.Wurten

        Gate_Zirmsee = shop.model.gate.Gate_Zirmsee_Grosssee
        Gate_Brettsee = shop.model.gate.Gate_Brettsee_Grosssee
        Gate_Kegelesee = shop.model.gate.Gate_Kegelesee_Moell

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################

        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Brettsee(shop)
        #shop = add_PP_Kegele(shop)
        shop = add_PP_Wurten(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Brettsee = shop.model.plant.Brettsee
        #KW_Kegele = shop.model.plant.Kegele
        KW_Wurten = shop.model.plant.Wurten

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################

        # Grossee - KW Zirknitz - Wurten
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten)

        # Wurten - KW Wurten - Möll
        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Moell)

        # Kegelesee / KW Kegele
        # Overflow/Bypass Kegele > Moell
        #Grosssee.connect_to(KW_Kegele)
        #KW_Kegele.connect_to(Kegelesee)
        Kegelesee.connect_to(Gate_Kegelesee, connection_type='bypass')
        Gate_Kegelesee.connect_to(Wurten)

        # Brettsee / KW Brettsee / Kegelesee
        # Overflow/Bypass Brettsee > Grosssee
        Brettsee.connect_to(KW_Brettsee)
        KW_Brettsee.connect_to(Kegelesee)
        Brettsee.connect_to(Gate_Brettsee, connection_type='bypass')
        Gate_Brettsee.connect_to(Grosssee)

        # DONE: Zirmsee > Gate Zirmsee > Grosssee
        Zirmsee.connect_to(Gate_Zirmsee)
        Gate_Zirmsee.connect_to(Grosssee)

        return shop

    elif topology == "Bernegger":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_Bernegger_upper(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Bernegger_lower(shop, use_tactical_limits=use_tactical_limits)

        Bernegger_upper = shop.model.reservoir.Bernegger_upper
        Bernegger_lower = shop.model.reservoir.Bernegger_lower

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Bernegger(shop)
        KW_Bernegger = shop.model.plant.Bernegger

        if MIP:
            shop.model.plant.Bernegger.mip_flag.set(1)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Bernegger_upper.connect_to(KW_Bernegger)
        KW_Bernegger.connect_to(Bernegger_lower)
        #Bernegger_upper.connect_to(Gate,connection_type='bypass')
        #Gate.connect_to(Drau)

        return shop

    elif topology == "SHOP_pump_example":

        ####################################################################################################################
        # Reservoir
        ####################################################################################################################
        shop = add_reservoir_RSV1(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_RSV2(shop, use_tactical_limits=use_tactical_limits)

        RSV1 = shop.model.reservoir.RSV1
        RSV2 = shop.model.reservoir.RSV2

        # Powerplants
        ####################################################################################################################
        shop = add_PP_Plant1(shop)
        plant1 = shop.model.plant.Plant1

        if MIP:
            shop.model.plant.Plant1.mip_flag.set(1)

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        RSV1.connect_to(plant1)
        plant1.connect_to(RSV2)

        return shop

    elif topology == "Goessnitz":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################

        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        shop = add_bypass_gate_Goessnitz(shop)

        Gate_Goessnitz = shop.model.gate.Gate_Goessnitz

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Goessnitz(shop)

        KW_Goessnitz = shop.model.plant.Goessnitz

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        Goessnitz.connect_to(Gate_Goessnitz,connection_type='bypass')
        Gate_Goessnitz.connect_to(Moell)

        return shop

    elif topology == "Goessnitz_Ramp":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################

        shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        shop = add_bypass_gate_Goessnitz(shop)

        Gate_Goessnitz = shop.model.gate.Gate_Goessnitz

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Goessnitz(shop)

        KW_Goessnitz = shop.model.plant.Goessnitz

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Goessnitz.connect_to(KW_Goessnitz)
        KW_Goessnitz.connect_to(Moell)

        Goessnitz.connect_to(Gate_Goessnitz,connection_type='bypass')
        Gate_Goessnitz.connect_to(Moell)

        return shop


    elif topology == "Fragant_O3_alt":
        ####################################################################################################################
        # Reservoirs
        ####################################################################################################################
        shop = add_reservoir_Grosssee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Feldsee(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Wurten(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Oschenik(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Innerfragant(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Haselstein(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Woella(shop, use_tactical_limits=use_tactical_limits)
        #shop = add_reservoir_Goessnitz(shop, use_tactical_limits=use_tactical_limits)
        shop = add_reservoir_Moell(shop, use_tactical_limits=use_tactical_limits)

        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        Woella = shop.model.reservoir.Woella
        #Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        shop = add_bypass_gate_Haselstein(shop)
        shop = add_bypass_gate_Woella(shop)
        #shop = add_bypass_gate_Goessnitz(shop)

        #shop = add_bypass_gate_Grosssee(shop)
        #shop = add_bypass_gate_Feldsee(shop)
        #shop = add_bypass_gate_Wurten(shop)
        #shop = add_bypass_gate_Oschenik(shop)
        #shop = add_bypass_gate_Innerfragant(shop)

        Gate_Haselstein = shop.model.gate.Gate_Haselstein
        Gate_Woella = shop.model.gate.Gate_Woella
        #Gate_Goessnitz = shop.model.gate.Gate_Goessnitz

        #Gate_Grosssee = shop.model.gate.Gate_Grosssee
        #Gate_Feldsee = shop.model.gate.Gate_Feldsee
        #Gate_Wurten = shop.model.gate.Gate_Wurten
        #Gate_Oschenik = shop.model.gate.Gate_Oschenik
        #Gate_Innerfragant = shop.model.gate.Gate_Innerfragant

        ####################################################################################################################
        # Powerplants
        ####################################################################################################################
        shop = add_PP_Zirknitz(shop)
        shop = add_PP_Feldsee(shop)
        shop = add_PP_Wurten(shop)
        shop = add_PP_Haselstein(shop)
        shop = add_PP_Oschenik_alt(shop)
        shop = add_PP_Oschenik_P1(shop)
        shop = add_PP_Oschenik_P23(shop)
        shop = add_PP_Woella(shop)
        shop = add_PP_Auszerfragant(shop)
        #shop = add_PP_Goessnitz(shop)

        KW_Zirknitz = shop.model.plant.Zirknitz
        KW_Feldsee = shop.model.plant.Feldsee
        KW_Wurten = shop.model.plant.Wurten
        KW_Haselstein = shop.model.plant.Haselstein
        KW_Oschenik = shop.model.plant.Oschenik
        KW_Oschenik_P1 = shop.model.plant.Oschenik_P1
        KW_Oschenik_P23 = shop.model.plant.Oschenik_P23
        KW_Woella = shop.model.plant.Woella
        KW_Auszerfragant = shop.model.plant.Auszerfragant
        #KW_Goessnitz = shop.model.plant.Goessnitz

        KW_Oschenik_P1.maintenance_flag.set(1)

        if MIP:
            shop.model.plant.Oschenik_P1.mip_flag.set(1)
            shop.model.plant.Oschenik_P23.mip_flag.set(1)
            shop.model.plant.Haselstein.mip_flag.set(1)
            #shop.model.global_settings.global_settings.universal_mip.get()

        ####################################################################################################################
        # Connecting the topological objects
        ####################################################################################################################
        Grosssee.connect_to(KW_Zirknitz)
        KW_Zirknitz.connect_to(Wurten)

        Feldsee.connect_to(KW_Feldsee)
        KW_Feldsee.connect_to(Wurten)

        Wurten.connect_to(KW_Wurten)
        KW_Wurten.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik)
        KW_Oschenik.connect_to(Innerfragant)

        Oschenik.connect_to(KW_Oschenik_P1)
        KW_Oschenik_P1.connect_to(Haselstein)

        Oschenik.connect_to(KW_Oschenik_P23)
        KW_Oschenik_P23.connect_to(Wurten)

        Haselstein.connect_to(KW_Haselstein)
        KW_Haselstein.connect_to(Innerfragant)

        Woella.connect_to(KW_Woella)
        KW_Woella.connect_to(Innerfragant)

        Innerfragant.connect_to(KW_Auszerfragant)
        KW_Auszerfragant.connect_to(Moell)

        #Goessnitz.connect_to(KW_Goessnitz)
        #KW_Goessnitz.connect_to(Moell)


        Haselstein.connect_to(Gate_Haselstein,connection_type='bypass')
        Gate_Haselstein.connect_to(Innerfragant)
        Woella.connect_to(Gate_Woella,connection_type='bypass')
        Gate_Woella.connect_to(Innerfragant)
        #Goessnitz.connect_to(Gate_Goessnitz,connection_type='bypass')
        #Gate_Goessnitz.connect_to(Moell)

        #Grosssee.connect_to(Gate_Grosssee,connection_type='bypass')
        #Gate_Grosssee.connect_to(Wurten)
        #Gate_Grosssee.connect_to(Moell)
        #Feldsee.connect_to(Gate_Feldsee,connection_type='bypass')
        #Gate_Feldsee.connect_to(Wurten)
        #Gate_Feldsee.connect_to(Moell)
        #Wurten.connect_to(Gate_Wurten,connection_type='bypass')
        #Gate_Wurten.connect_to(Innerfragant)
        #Gate_Wurten.connect_to(Moell)
        #Innerfragant.connect_to(Gate_Innerfragant,connection_type='bypass')
        #Gate_Innerfragant.connect_to(Moell)
        #Oschenik.connect_to(Gate_Oschenik,connection_type='bypass')
        #Gate_Oschenik.connect_to(Innerfragant)
        #Gate_Oschenik.connect_to(Moell)

        #grid_restriction_group = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP')
        #grid_restriction_group.max_p_limit.set(240)

        #grid_restriction_group.connect_to(KW_Oschenik)
        #grid_restriction_group.connect_to(KW_Oschenik_P1)
        #grid_restriction_group.connect_to(KW_Oschenik_P23)
        #grid_restriction_group.connect_to(KW_Wurten)
        #grid_restriction_group.connect_to(KW_Feldsee)
        #grid_restriction_group.connect_to(KW_Haselstein)


        #default = 9999
        #grid_restriction_group_all = shop.model.production_group.add_object('GRID_RESTRICTION_GROUP_ALL')
        #grid_restriction_group_all.max_p_limit.set(pd.Series([default,280,default],
                                                   #index=[pd.Timestamp(2023,1,1),pd.Timestamp(2023,5,3,9), pd.Timestamp(2023,5,3,15)]))

        #grid_restriction_group_all.connect_to(KW_Zirknitz)
        #grid_restriction_group_all.connect_to(KW_Oschenik)
        #grid_restriction_group_all.connect_to(KW_Wurten)
        #grid_restriction_group_all.connect_to(KW_Feldsee)
        #grid_restriction_group_all.connect_to(KW_Haselstein)
        #grid_restriction_group_all.connect_to(KW_Auszerfragant)
        #grid_restriction_group_all.connect_to(KW_Woella)
        #grid_restriction_group_all.connect_to(KW_Goessnitz)

        return shop

    else:
        print("Topology not defined.")
        return shop