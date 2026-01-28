from Misc import *

########################################################################################################################
# DRAU
########################################################################################################################
def add_reservoir_Drau(shop):

    res_drau = shop.model.reservoir.add_object('Drau')

    max_vol = 10000
    res_drau.max_vol.set(max_vol)
    res_drau.lrl.set(339)
    res_drau.hrl.set(339.50)

    res_drau.vol_head.set(pd.Series([339, 339.5],
                                index=[0, max_vol], name=0))

    return shop

########################################################################################################################
# Feldsee
########################################################################################################################
def add_reservoir_Feldsee(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Feldsee = shop.model.reservoir.add_object('Feldsee')

    Feldsee.max_vol.set(2.583)  # maximum volume in Mm3
    Feldsee.lrl.set(2196)  # lowest regulated level in masl
    Feldsee.hrl.set(2221)  # highest regulated level in masl

    #Feldsee.schedule.set(pd.Series([1.179], index=[starttime])) #Mm3
    #Feldsee.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Feldsee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Feldsee",2197)],index=[starttime], name=0))
        Feldsee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Feldsee.tactical_limit_min_flag.set(1)

        Feldsee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Feldsee",2220.5)], index=[starttime], name=0))
        Feldsee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Feldsee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Feldsee')
    Feldsee.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Forstsee
########################################################################################################################
def add_reservoir_Forstsee(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Forstsee = shop.model.reservoir.add_object('Forstsee')

    Forstsee.max_vol.set(6.235705)  # maximum volume in Mm3
    Forstsee.lrl.set(586)  # lowest regulated level in masl
    Forstsee.hrl.set(605.5)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 4.406) #Mm3

    Forstsee.schedule.set(pd.Series(schedule, index=date_range))
    Forstsee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    if use_tactical_limits:
        limit_val = get_limit_val()

        # only min tactical limit
        time_series, min_limit = get_tactical_limit(starttime, endtime, Forstsee.get_name())

        Forstsee.tactical_limit_min.set(pd.Series(min_limit,index=time_series, name=0))
        Forstsee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Forstsee.tactical_limit_min_flag.set(1)

        Forstsee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Forstsee",605.5)], index=[starttime], name=0))
        Forstsee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Forstsee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Forstsee')
    Forstsee.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# FREIBACH
########################################################################################################################
def add_reservoir_Freibach(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Freibach = shop.model.reservoir.add_object('Freibach')

    Freibach.max_vol.set(5.865)  # maximum volume in Mm3
    Freibach.lrl.set(705)  # lowest regulated level in masl
    Freibach.hrl.set(729.2)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 2.424) #Mm3

    Freibach.schedule.set(pd.Series(schedule, index=date_range))
    Freibach.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    if use_tactical_limits:
        limit_val = get_limit_val()

        time_series, min_limit = get_tactical_limit(starttime, endtime, Freibach.get_name())

        Freibach.tactical_limit_min.set(pd.Series(min_limit,index=time_series, name=0))
        Freibach.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Freibach.tactical_limit_min_flag.set(1)

        Freibach.tactical_limit_max.set(pd.Series([convert_head_to_vol("Freibach",722)], index=[starttime], name=0))
        Freibach.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Freibach.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Freibach')
    Freibach.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# GALGENBICHL
########################################################################################################################
def add_reservoir_Galgenbichl(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Galgenbichl = shop.model.reservoir.add_object('Galgenbichl')

    Galgenbichl.max_vol.set(0.89635)  # maximum volume in Mm3
    Galgenbichl.lrl.set(1680)  # lowest regulated level in masl
    Galgenbichl.hrl.set(1704)  # highest regulated level in masl

    #Galgenbichl.schedule.set(pd.Series([0.365], index=[starttime])) #Mm3
    #Galgenbichl.schedule_flag.set(1)

    x = [1704, 1705]
    y = [0.0, 84.766]
    Galgenbichl.flow_descr.set(pd.Series(y,index=x,name=0.0))

    if use_tactical_limits:
        limit_val = get_limit_val()

        Galgenbichl.tactical_limit_min.set(pd.Series([convert_head_to_vol("Galgenbichl",1681)],index=[starttime], name=0))
        Galgenbichl.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Galgenbichl.tactical_limit_min_flag.set(1)

        Galgenbichl.tactical_limit_max.set(pd.Series([convert_head_to_vol("Galgenbichl",1703)], index=[starttime], name=0))
        Galgenbichl.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Galgenbichl.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Galgenbichl')
    Galgenbichl.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# GOESSKAR
########################################################################################################################
def add_reservoir_Goesskar(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Goesskar = shop.model.reservoir.add_object('Goesskar')

    Goesskar.max_vol.set(0.44306)  # maximum volume in Mm3
    Goesskar.lrl.set(1680)  # lowest regulated level in masl
    Goesskar.hrl.set(1704)  # highest regulated level in masl

    #Goesskar.schedule.set(pd.Series([0.219], index=[starttime])) #Mm3
    #Goesskar.schedule_flag.set(1)

    x = [1704, 1705]
    y = [0.0, 102.446]
    Goesskar.flow_descr.set(pd.Series(y,index=x,name=0.0))

    Goesskar.upper_slack.set(0.219)

    Goesskar.energy_value_input.set(100.0)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Goesskar.tactical_limit_min.set(pd.Series([convert_head_to_vol("Goesskar",1681)],index=[starttime], name=0))
        Goesskar.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Goesskar.tactical_limit_min_flag.set(1)

        Goesskar.tactical_limit_max.set(pd.Series([convert_head_to_vol("Goesskar",1703)], index=[starttime], name=0))
        Goesskar.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Goesskar.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Goesskar')
    Goesskar.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# GOESSNITZ
########################################################################################################################

def add_reservoir_Goessnitz(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Goessnitz = shop.model.reservoir.add_object('Goessnitz')

    Goessnitz.max_vol.set(0.385)  # maximum volume in Mm3
    Goessnitz.lrl.set(745.5)  # lowest regulated level in masl
    Goessnitz.hrl.set(746.30)  # highest regulated level in masl

    #Goessnitz.schedule.set(pd.Series([0.301], index=[starttime])) #Mm3
    #Goessnitz.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Goessnitz.tactical_limit_min.set(pd.Series([convert_head_to_vol("Goessnitz",745.5)],index=[starttime], name=0))
        Goessnitz.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Goessnitz.tactical_limit_min_flag.set(1)

        Goessnitz.tactical_limit_max.set(pd.Series([convert_head_to_vol("Goessnitz",746.25)], index=[starttime], name=0))
        Goessnitz.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Goessnitz.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Goessnitz')
    Goessnitz.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# GROSSSEE
########################################################################################################################
def add_reservoir_Grosssee(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Grosssee = shop.model.reservoir.add_object('Grosssee')

    Grosssee.max_vol.set(28.765)  # maximum volume in Mm3
    Grosssee.lrl.set(2333)  # lowest regulated level in masl
    Grosssee.hrl.set(2416.8)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 21.217) #Mm3

    Grosssee.schedule.set(pd.Series(schedule, index=date_range))
    Grosssee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    Grosssee.upper_slack.set(21.3)
    Grosssee.lower_slack.set(21.2)

    #Grosssee.schedule.set(pd.Series([21.217], index=[starttime])) #Mm3
    #Grosssee.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Grosssee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Grosssee",2334)],index=[starttime], name=0))
        Grosssee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Grosssee.tactical_limit_min_flag.set(1)

        Grosssee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Grosssee",2416)], index=[starttime], name=0))
        Grosssee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Grosssee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Grosssee')
    Grosssee.vol_head.set(pd.Series(level,index=storage, name=0))

    return shop

########################################################################################################################
# GROSSSEE Topology Advanced (incl. Zirmsee, Brettsee, Kegelesee)
########################################################################################################################
def add_reservoir_Grosssee_adv(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Grosssee = shop.model.reservoir.add_object('Grosssee_adv')

    Grosssee.max_vol.set(28.765)  # maximum volume in Mm3
    Grosssee.lrl.set(2333)  # lowest regulated level in masl
    Grosssee.hrl.set(2416.8)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 21.217) #Mm3

    Grosssee.schedule.set(pd.Series(schedule, index=date_range))
    Grosssee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    Grosssee.upper_slack.set(21.3)
    Grosssee.lower_slack.set(21.2)

    #Grosssee.schedule.set(pd.Series([21.217], index=[starttime])) #Mm3
    #Grosssee.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Grosssee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Grosssee",2334)],index=[starttime], name=0))
        Grosssee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Grosssee.tactical_limit_min_flag.set(1)

        Grosssee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Grosssee",2416)], index=[starttime], name=0))
        Grosssee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Grosssee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Grosssee')
    Grosssee.vol_head.set(pd.Series(level,index=storage, name=0))

    return shop

########################################################################################################################
# HASELSTEIN
########################################################################################################################
def add_reservoir_Haselstein(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Haselstein = shop.model.reservoir.add_object('Haselstein')

    Haselstein.max_vol.set(0.029709)  # maximum volume in Mm3
    Haselstein.lrl.set(1461)  # lowest regulated level in masl
    Haselstein.hrl.set(1469.5)  # highest regulated level in masl
    #Haselstein.hrl.set(1469)  # highest regulated level in masl

    #Haselstein.schedule.set(pd.Series([0.013], index=[starttime])) #Mm3
    #Haselstein.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Haselstein.tactical_limit_min.set(pd.Series([convert_head_to_vol("Haselstein",1461.5)],index=[starttime], name=0))
        Haselstein.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Haselstein.tactical_limit_min_flag.set(1)

        Haselstein.tactical_limit_max.set(pd.Series([convert_head_to_vol("Haselstein",1469)], index=[starttime], name=0))
        Haselstein.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Haselstein.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Haselstein')
    Haselstein.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# HASELSTEIN with big storage volume (0.1 Mm3)
########################################################################################################################
def add_reservoir_Haselstein_big(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Haselstein = shop.model.reservoir.add_object('Haselstein_big')

    Haselstein.max_vol.set(0.1)  # maximum volume in Mm3
    Haselstein.lrl.set(1461)  # lowest regulated level in masl
    Haselstein.hrl.set(1470.5)  # highest regulated level in masl

    #Haselstein.schedule.set(pd.Series([0.013], index=[starttime])) #Mm3
    #Haselstein.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Haselstein.tactical_limit_min.set(pd.Series([convert_head_to_vol("Haselstein", 1461.5)], index=[starttime], name=0))
        Haselstein.tactical_cost_min.set(pd.Series([limit_val], index=[starttime], name=0))
        Haselstein.tactical_limit_min_flag.set(1)

        Haselstein.tactical_limit_max.set(pd.Series([convert_head_to_vol("Haselstein", 1469)], index=[starttime], name=0))
        Haselstein.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Haselstein.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Haselstein_big')
    Haselstein.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# INNERFRAGANT
########################################################################################################################
def add_reservoir_Innerfragant(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Innerfragant = shop.model.reservoir.add_object('Innerfragant')

    Innerfragant.max_vol.set(0.21)  # maximum volume in Mm3
    Innerfragant.lrl.set(1193)  # lowest regulated level in masl
    Innerfragant.hrl.set(1200.6)  # highest regulated level in masl

    #Innerfragant.schedule.set(pd.Series([0.085], index=[starttime])) #Mm3
    #Innerfragant.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Innerfragant.tactical_limit_min.set(pd.Series([convert_head_to_vol("Innerfragant", 1194)],index=[starttime], name=0))
        Innerfragant.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Innerfragant.tactical_limit_min_flag.set(1)

        Innerfragant.tactical_limit_max.set(pd.Series([convert_head_to_vol("Innerfragant", 1200.5)], index=[starttime], name=0))
        Innerfragant.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Innerfragant.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Innerfragant')
    Innerfragant.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Koelnbrein
########################################################################################################################
def add_reservoir_Koelnbrein(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Koelnbrein = shop.model.reservoir.add_object('Koelnbrein')

    Koelnbrein.max_vol.set(48.04791)  # maximum volume in Mm3
    Koelnbrein.lrl.set(1730)  # lowest regulated level in masl
    Koelnbrein.hrl.set(1902)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 38.235) #Mm3

    Koelnbrein.schedule.set(pd.Series(schedule, index=date_range))
    Koelnbrein.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    Koelnbrein.upper_slack.set(38.3)
    Koelnbrein.lower_slack.set(38.2)

    #Koelnbrein.schedule.set(pd.Series([38.235], index=[starttime])) #Mm3
    #Koelnbrein.schedule_flag.set(1)

    x = [1902.0, 1903.0]
    y = [0.0, 500.0]
    Koelnbrein.flow_descr.set(pd.Series(y,index=x,name=0.0))

    if use_tactical_limits:
        limit_val = get_limit_val()

        # 2nd argument list of [month,day], 3rd argument the respective head levels
        t, max_limit = reoccuring_limit(shop, [[1, 1], [5, 1], [5, 2]], [1896, 1780, 1896],res="Koelnbrein")

        Koelnbrein.tactical_limit_min.set(pd.Series([convert_head_to_vol("Koelnbrein", 1765)],index=[starttime], name=0))
        Koelnbrein.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Koelnbrein.tactical_limit_min_flag.set(1)

        Koelnbrein.tactical_limit_max.set(pd.Series(max_limit, index=t, name=0))
        Koelnbrein.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Koelnbrein.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Koelnbrein')
    Koelnbrein.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# MOELL
########################################################################################################################
def add_reservoir_Moell(shop, use_tactical_limits=True):

    Moell = shop.model.reservoir.add_object('Moell')

    max_vol = 100000

    Moell.max_vol.set(max_vol)
    Moell.lrl.set(339)
    Moell.hrl.set(339.50)

    Moell.vol_head.set(pd.Series([339, 339.5],
                                 index=[0, max_vol], name=0))

    return shop

########################################################################################################################
# MUEHLDORFERSEE
########################################################################################################################
def add_reservoir_Muehldorfersee(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Muehldorfersee = shop.model.reservoir.add_object('Muehldorfersee')

    Muehldorfersee.max_vol.set(1.8528)  # maximum volume in Mm3
    Muehldorfersee.lrl.set(2255)  # lowest regulated level in masl
    Muehldorfersee.hrl.set(2319)  # highest regulated level in masl

    #Muehldorfersee.schedule.set(pd.Series([0.823], index=[starttime])) #Mm3
    #Muehldorfersee.schedule_flag.set(1)

    x = [2319.0, 2320.0]
    y = [0.0, 100.0]
    Muehldorfersee.flow_descr.set(pd.Series(y,index=x,name=0.0))

    if use_tactical_limits:
        limit_val = get_limit_val()

        Muehldorfersee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Muehldorfersee", 2256)],index=[starttime], name=0))
        Muehldorfersee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Muehldorfersee.tactical_limit_min_flag.set(1)

        Muehldorfersee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Muehldorfersee", 2318)], index=[starttime], name=0))
        Muehldorfersee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Muehldorfersee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Muehldorfersee')
    Muehldorfersee.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# OSCHENIK
########################################################################################################################
def add_reservoir_Oschenik(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Oschenik = shop.model.reservoir.add_object('Oschenik')

    Oschenik.max_vol.set(30.77)  # maximum volume in Mm3
    Oschenik.lrl.set(2245)  # lowest regulated level in masl
    Oschenik.hrl.set(2391)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 24.172) #Mm3

    Oschenik.schedule.set(pd.Series(schedule, index=date_range))
    Oschenik.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    Oschenik.upper_slack.set(24.2)
    Oschenik.lower_slack.set(24.1)

    #Oschenik.schedule.set(pd.Series([24.172], index=[starttime])) #Mm3
    #Oschenik.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        # 2nd argument list of [month,day], 3rd argument the respective head levels
        t, max_limit = reoccuring_limit(shop, [[1, 1], [5, 1], [5, 2]], [2390.5, 2344, 2390.5],res="Oschenik")

        Oschenik.tactical_limit_min.set(pd.Series([convert_head_to_vol("Oschenik", 2280)],index=[starttime], name=0))
        Oschenik.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Oschenik.tactical_limit_min_flag.set(1)

        Oschenik.tactical_limit_max.set(pd.Series(max_limit, index=t, name=0))
        Oschenik.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Oschenik.tactical_limit_max_flag.set(1)

        #Oschenik.tactical_limit_max.set(pd.Series([convert_head_to_vol("Oschenik", 2390.5)], index=[starttime], name=0))
        #Oschenik.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        #Oschenik.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Oschenik')
    Oschenik.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# ROTTAU
########################################################################################################################
def add_reservoir_Rottau(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Rottau = shop.model.reservoir.add_object('Rottau')

    #Rottau.max_vol.set(0.12912)  # maximum volume in Mm3
    Rottau.max_vol.set(0.1449264)
    Rottau.lrl.set(596.5)  # lowest regulated level in masl
    Rottau.hrl.set(598.5)  # highest regulated level in masl

    #Rottau.schedule.set(pd.Series([0.018], index=[starttime])) #Mm3
    #Rottau.schedule_flag.set(1)

    x = [598.5, 599.5]
    y = [0.0, 100.0]
    Rottau.flow_descr.set(pd.Series(y,index=x,name=0.0))

    if use_tactical_limits:
        limit_val = get_limit_val()

        Rottau.tactical_limit_min.set(pd.Series([convert_head_to_vol("Rottau", 596.6)],index=[starttime], name=0))
        Rottau.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Rottau.tactical_limit_min_flag.set(1)

        Rottau.tactical_limit_max.set(pd.Series([convert_head_to_vol("Rottau", 597.9)], index=[starttime], name=0))
        Rottau.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Rottau.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Rottau')
    Rottau.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# ROTTAU 650.000 (100%)
########################################################################################################################
def add_reservoir_Rottau650(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Rottau650 = shop.model.reservoir.add_object('Rottau650')

    Rottau650.max_vol.set(0.16504)  # maximum volume in Mm3
    Rottau650.lrl.set(596.5)  # lowest regulated level in masl
    Rottau650.hrl.set(598.5)  # highest regulated level in masl

    #Rottau.schedule.set(pd.Series([0.018], index=[starttime])) #Mm3
    #Rottau.schedule_flag.set(1)

    x = [598.5, 599.5]
    y = [0.0, 100.0]
    Rottau650.flow_descr.set(pd.Series(y,index=x,name=0.0))

    if use_tactical_limits:
        limit_val = get_limit_val()

        Rottau.tactical_limit_min.set(pd.Series([convert_head_to_vol("Rottau", 596.6)],index=[starttime], name=0))
        Rottau.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Rottau.tactical_limit_min_flag.set(1)

        Rottau.tactical_limit_max.set(pd.Series([convert_head_to_vol("Rottau", 597.9)], index=[starttime], name=0))
        Rottau.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Rottau.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Rottau650')
    Rottau650.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Kolbnitz (Dummy reservoir)
########################################################################################################################
def add_reservoir_Kolbnitz(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Kolbnitz = shop.model.reservoir.add_object('Kolbnitz')

    Kolbnitz.max_vol.set(0.150)  # maximum volume in Mm3
    Kolbnitz.lrl.set(700.0)  # lowest regulated level in masl
    Kolbnitz.hrl.set(705.0)  # highest regulated level in masl

    x = [705.0, 706.0]
    y = [0.0, 100.0]
    Kolbnitz.flow_descr.set(pd.Series(y,index=x,name=0.0))

    if use_tactical_limits:
        limit_val = get_limit_val()

        Kolbnitz.tactical_limit_min.set(pd.Series([convert_head_to_vol("Kolbnitz", 700.1)],index=[starttime], name=0))
        Kolbnitz.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Kolbnitz.tactical_limit_min_flag.set(1)

        Kolbnitz.tactical_limit_max.set(pd.Series([convert_head_to_vol("Kolbnitz", 704.9)], index=[starttime], name=0))
        Kolbnitz.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Kolbnitz.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Kolbnitz')
    Kolbnitz.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# SOBOTH
########################################################################################################################
def add_reservoir_Soboth(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Soboth = shop.model.reservoir.add_object('Soboth')

    Soboth.max_vol.set(15.825)      # maximum volume in Mm3
    Soboth.lrl.set(1053.5)          # lowest regulated level in masl
    Soboth.hrl.set(1080)            # highest regulated level in masl
    #Soboth.end_value.set(11.822)    # end point for simulation in Mm3

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 14.350) #Mm3

    Soboth.schedule.set(pd.Series(schedule, index=date_range))
    Soboth.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    Soboth.upper_slack.set(14.4)
    Soboth.lower_slack.set(14.3)

    if use_tactical_limits:
        limit_val = get_limit_val()

        time_series, min_limit = get_tactical_limit(starttime, endtime, Soboth.get_name())
        t, max_limit = reoccuring_limit(shop, [[1, 1]], [1080],res="Soboth")

        Soboth.tactical_limit_min.set(pd.Series(min_limit,index=time_series, name=0))
        Soboth.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Soboth.tactical_limit_min_flag.set(1)

        Soboth.tactical_limit_max.set(pd.Series(max_limit, index=t, name=0))
        Soboth.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Soboth.tactical_limit_max_flag.set(1)

        #Soboth.tactical_limit_min.set(pd.Series(min_limit,index=time_series, name=0))
        #Soboth.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        #Soboth.tactical_limit_min_flag.set(1)

        #Soboth.tactical_limit_max.set(pd.Series([convert_head_to_vol("Soboth", 1080)], index=[starttime], name=0))
        #Soboth.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        #Soboth.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Soboth')
    Soboth.vol_head.set(pd.Series(level,index=storage, name=0))

    return shop

########################################################################################################################
# SOBOTH incl. dead space
########################################################################################################################
def add_reservoir_Soboth_incl_dead_space(shop):

    Soboth = shop.model.reservoir.add_object('Soboth')

    Soboth.max_vol.set(21.873)      # maximum volume in Mm3
    Soboth.lrl.set(1010)          # lowest regulated level in masl
    Soboth.hrl.set(1080)            # highest regulated level in masl

    storage, level = detail_kubatur('Soboth_incl_dead_space')

    Soboth.vol_head.set(pd.Series(level,index=storage, name=0))

    return shop

########################################################################################################################
# Wiederschwing
########################################################################################################################
def add_reservoir_Wiederschwing(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Wiederschwing = shop.model.reservoir.add_object('Wiederschwing')

    Wiederschwing.max_vol.set(0.956)  # maximum volume in Mm3
    Wiederschwing.lrl.set(660.0)  # lowest regulated level in masl
    Wiederschwing.hrl.set(676.5)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 0.354) #Mm3 = 671 masl.

    Wiederschwing.schedule.set(pd.Series(schedule, index=date_range))
    Wiederschwing.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    Wiederschwing.upper_slack.set(0.36)
    Wiederschwing.lower_slack.set(0.34)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Wiederschwing.tactical_limit_min.set(pd.Series([convert_head_to_vol("Wiederschwing", 668.5)],index=[starttime], name=0))
        Wiederschwing.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Wiederschwing.tactical_limit_min_flag.set(1)

        Wiederschwing.tactical_limit_max.set(pd.Series([convert_head_to_vol("Wiederschwing", 676.17)], index=[starttime], name=0))
        Wiederschwing.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Wiederschwing.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Wiederschwing')
    Wiederschwing.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# WOELLA
########################################################################################################################
def add_reservoir_Woella(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Woella = shop.model.reservoir.add_object('Woella')

    Woella.max_vol.set(0.091)  # maximum volume in Mm3
    Woella.lrl.set(1534.5)  # lowest regulated level in masl
    Woella.hrl.set(1542)  # highest regulated level in masl

    #Woella.schedule.set(pd.Series([0.044], index=[starttime])) #Mm3
    #Woella.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Woella.tactical_limit_min.set(pd.Series([convert_head_to_vol("Woella", 1535)],index=[starttime], name=0))
        Woella.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Woella.tactical_limit_min_flag.set(1)

        Woella.tactical_limit_max.set(pd.Series([convert_head_to_vol("Woella", 1541)], index=[starttime], name=0))
        Woella.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Woella.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Woella')
    Woella.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Woerthersee
########################################################################################################################
def add_reservoir_Woerthersee(shop):

    res_Woerthersee = shop.model.reservoir.add_object('Woerthersee')

    max_vol = 10000
    res_Woerthersee.max_vol.set(max_vol)
    res_Woerthersee.lrl.set(439)
    res_Woerthersee.hrl.set(439.50)

    res_Woerthersee.vol_head.set(pd.Series([439, 439.5],
                                index=[0, max_vol], name=0))

    return shop

########################################################################################################################
# WURTEN
########################################################################################################################
def add_reservoir_Wurten(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Wurten = shop.model.reservoir.add_object('Wurten')

    Wurten.max_vol.set(2.627)  # maximum volume in Mm3
    Wurten.lrl.set(1675)  # lowest regulated level in masl
    Wurten.hrl.set(1695)  # highest regulated level in masl

    #Wurten.schedule.set(pd.Series([0.869], index=[starttime])) #Mm3
    #Wurten.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Wurten.tactical_limit_min.set(pd.Series([convert_head_to_vol("Wurten", 1675.5)],index=[starttime], name=0))
        Wurten.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Wurten.tactical_limit_min_flag.set(1)

        Wurten.tactical_limit_max.set(pd.Series([convert_head_to_vol("Wurten", 1694.5)], index=[starttime], name=0))
        Wurten.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Wurten.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Wurten')
    Wurten.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# WURTEN 5hm³
########################################################################################################################
def add_reservoir_Wurten_big(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Wurten_big = shop.model.reservoir.add_object('Wurten_big')

    Wurten_big.max_vol.set(4.91)  # maximum volume in Mm3
    Wurten_big.lrl.set(1675)  # lowest regulated level in masl
    Wurten_big.hrl.set(1703.5)  # highest regulated level in masl

    #Wurten.schedule.set(pd.Series([0.869], index=[starttime])) #Mm3
    #Wurten.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Wurten_big.tactical_limit_min.set(pd.Series([convert_head_to_vol("Wurten_big", 1675.5)],index=[starttime], name=0))
        Wurten_big.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Wurten_big.tactical_limit_min_flag.set(1)

        Wurten_big.tactical_limit_max.set(pd.Series([convert_head_to_vol("Wurten_big", 1703.5)], index=[starttime], name=0))
        Wurten_big.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Wurten_big.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Wurten_big')
    Wurten_big.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Zirmsee
########################################################################################################################
def add_reservoir_Zirmsee(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Zirmsee = shop.model.reservoir.add_object('Zirmsee')

    Zirmsee.max_vol.set(8.218421)  # maximum volume in Mm3
    Zirmsee.lrl.set(2487.0)  # lowest regulated level in masl
    Zirmsee.hrl.set(2529.5)  # highest regulated level in masl

    #Zirmsee.schedule.set(pd.Series([3.21], index=[starttime])) #Mm3
    #Zirmsee.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Zirmsee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Zirmsee", 2487.1)],index=[starttime], name=0))
        Zirmsee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Zirmsee.tactical_limit_min_flag.set(1)

        Zirmsee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Zirmsee", 2529.0)], index=[starttime], name=0))
        Zirmsee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Zirmsee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Zirmsee')
    Zirmsee.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Brettsee
########################################################################################################################
def add_reservoir_Brettsee(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Brettsee = shop.model.reservoir.add_object('Brettsee')

    Brettsee.max_vol.set(1.0)  # maximum volume in Mm3
    Brettsee.lrl.set(2500)  # lowest regulated level in masl
    Brettsee.hrl.set(2529.5)  # highest regulated level in masl

    #Brettsee.schedule.set(pd.Series([0.869], index=[starttime])) #Mm3
    #Brettsee.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Brettsee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Brettsee", 2500.5)],index=[starttime], name=0))
        Brettsee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Brettsee.tactical_limit_min_flag.set(1)

        Brettsee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Brettsee", 2529.0)], index=[starttime], name=0))
        Brettsee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Brettsee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Brettsee')
    Brettsee.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# Kegelesee
########################################################################################################################
def add_reservoir_Kegelesee(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Kegelesee = shop.model.reservoir.add_object('Kegelesee')

    Kegelesee.max_vol.set(1.583081)  # maximum volume in Mm3
    Kegelesee.lrl.set(2157.0)  # lowest regulated level in masl
    Kegelesee.hrl.set(2180.0)  # highest regulated level in masl

    if use_tactical_limits:
        limit_val = get_limit_val()

        #Kegelesee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Kegelesee", 2160.6)], index=[starttime], name=0))
        Kegelesee.tactical_limit_min.set(pd.Series([convert_head_to_vol("Kegelesee", 2161.6)],index=[starttime], name=0))
        Kegelesee.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Kegelesee.tactical_limit_min_flag.set(1)

        Kegelesee.tactical_limit_max.set(pd.Series([convert_head_to_vol("Kegelesee", 2174.9)], index=[starttime], name=0))
        Kegelesee.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Kegelesee.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Kegelesee')
    Kegelesee.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# PSKW Bernegger - Oberlieger
########################################################################################################################
def add_reservoir_Bernegger_upper(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Bernegger_upper = shop.model.reservoir.add_object('Bernegger_upper')

    Bernegger_upper.max_vol.set(1.24)   # maximum volume in Mm3
    Bernegger_upper.lrl.set(600.0)      # lowest regulated level in masl
    Bernegger_upper.hrl.set(660.0)      # highest regulated level in masl

    #Bernegger_upper.schedule.set(pd.Series([3.21], index=[starttime])) #Mm3
    #Bernegger_upper.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Bernegger_upper.tactical_limit_min.set(pd.Series([convert_head_to_vol("Bernegger_upper", 600.0)],index=[starttime], name=0))
        Bernegger_upper.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Bernegger_upper.tactical_limit_min_flag.set(1)

        Bernegger_upper.tactical_limit_max.set(pd.Series([convert_head_to_vol("Bernegger_upper", 660.0)], index=[starttime], name=0))
        Bernegger_upper.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Bernegger_upper.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Bernegger_upper')
    Bernegger_upper.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# PSKW Bernegger - Unterlieger
########################################################################################################################
def add_reservoir_Bernegger_lower(shop,use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    Bernegger_lower = shop.model.reservoir.add_object('Bernegger_lower')

    Bernegger_lower.max_vol.set(1.24)   # maximum volume in Mm3
    Bernegger_lower.lrl.set(0.0)      # lowest regulated level in masl
    Bernegger_lower.hrl.set(60.0)      # highest regulated level in masl

    #Bernegger_upper.schedule.set(pd.Series([3.21], index=[starttime])) #Mm3
    #Bernegger_upper.schedule_flag.set(1)

    if use_tactical_limits:
        limit_val = get_limit_val()

        Bernegger_lower.tactical_limit_min.set(pd.Series([convert_head_to_vol("Bernegger_lower", 0.0)],index=[starttime], name=0))
        Bernegger_lower.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        Bernegger_lower.tactical_limit_min_flag.set(1)

        Bernegger_lower.tactical_limit_max.set(pd.Series([convert_head_to_vol("Bernegger_lower", 60.0)], index=[starttime], name=0))
        Bernegger_lower.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        Bernegger_lower.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('Bernegger_lower')
    Bernegger_lower.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

########################################################################################################################
# SHOP pump example
########################################################################################################################
def add_reservoir_RSV1(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    RSV1 = shop.model.reservoir.add_object('RSV1')

    RSV1.max_vol.set(12)  # maximum volume in Mm3
    RSV1.lrl.set(90)  # lowest regulated level in masl
    RSV1.hrl.set(100)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 6) #Mm3

    RSV1.schedule.set(pd.Series(schedule, index=date_range))
    RSV1.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    if use_tactical_limits:
        limit_val = get_limit_val()

        # only min tactical limit
        time_series, min_limit = get_tactical_limit(starttime, endtime, RSV1.get_name())

        RSV1.tactical_limit_min.set(pd.Series(min_limit,index=time_series, name=0))
        RSV1.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        RSV1.tactical_limit_min_flag.set(1)

        RSV1.tactical_limit_max.set(pd.Series([convert_head_to_vol("RSV1",92)], index=[starttime], name=0))
        RSV1.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        RSV1.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('RSV1')
    RSV1.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop

def add_reservoir_RSV2(shop, use_tactical_limits=True):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]
    endtime = shop.get_time_resolution()['timeresolution'].index[-1]

    RSV2 = shop.model.reservoir.add_object('RSV2')

    RSV2.max_vol.set(5)  # maximum volume in Mm3
    RSV2.lrl.set(40)  # lowest regulated level in masl
    RSV2.hrl.set(50)  # highest regulated level in masl

    schedule, schedule_flag, date_range = set_year_end_schedule(shop, 2.5) #Mm3

    RSV2.schedule.set(pd.Series(schedule, index=date_range))
    RSV2.schedule_flag.set(pd.Series(schedule_flag, index=date_range))

    if use_tactical_limits:
        limit_val = get_limit_val()

        # only min tactical limit
        time_series, min_limit = get_tactical_limit(starttime, endtime, RSV2.get_name())

        RSV2.tactical_limit_min.set(pd.Series(min_limit,index=time_series, name=0))
        RSV2.tactical_cost_min.set(pd.Series([limit_val],index=[starttime], name=0))
        RSV2.tactical_limit_min_flag.set(1)

        RSV2.tactical_limit_max.set(pd.Series([convert_head_to_vol("RSV2",43)], index=[starttime], name=0))
        RSV2.tactical_cost_max.set(pd.Series([limit_val], index=[starttime], name=0))
        RSV2.tactical_limit_max_flag.set(1)

    storage, level = detail_kubatur('RSV2')
    RSV2.vol_head.set(pd.Series(level, index=storage, name=0))

    return shop



def add_tunnel_Galgenbichl_Goesskar(shop):

    Tunnel = shop.model.tunnel.add_object("Tunnel_GAL_GOE")

    Tunnel.start_height.set(1680.1)
    Tunnel.end_height.set(1680.1)

    Tunnel.length.set(9350)
    Tunnel.diameter.set(3)

    Tunnel.max_flow.set(80)

    Tunnel.loss_factor.set(0.00)

    return shop


def add_gate_Galgenbichl_Goesskar(shop):

    Gate = shop.model.gate.add_object("Gate_GAL_GOE")

    Gate.time_delay.set(60)

    discharge = np.array([80.0, 61.1, 40.0, 23.1, 16.3, 0.0, -16.3, -23.1, -40.0, -61.1, -80.0])
    deltameter = np.array([-24.0, -14.0, -6.0, -2.0, -1.0, 0.0, 1.0, 2.0, 6.0, 14.0, 24.0])

    Gate.functions_deltameter_m3s.set([pd.Series(discharge,index=deltameter,name=0)]) #,name=1692

    Gate.max_flow.set(80.0)

    return shop


def add_gate_Muehldorfersee_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_MUE_Drau")
    Gate.max_flow.set(1000.0)

    return shop


def add_gate_Koelnbrein_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_KOE_Drau")
    Gate.max_flow.set(1000.0)

    return shop


def add_gate_Galgenbichl_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_GAL_Drau")
    Gate.max_flow.set(1000.0)

    return shop

def add_gate_Goesskar_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_GOE_Drau")
    Gate.max_flow.set(1000.0)

    return shop


def add_gate_Rottau_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_ROT_Drau")
    Gate.max_flow.set(1000.0)

    return shop

def add_gate_Kolbnitz_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_KOLB_Drau")
    Gate.max_flow.set(1000.0)

    return shop


def add_bypass_gate_Haselstein(shop):
    Gate = shop.model.gate.add_object("Gate_Haselstein")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Goessnitz(shop):
    Gate = shop.model.gate.add_object("Gate_Goessnitz")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Woella(shop):
    Gate = shop.model.gate.add_object("Gate_Woella")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Wurten(shop):
    Gate = shop.model.gate.add_object("Gate_Wurten")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Grosssee(shop):
    Gate = shop.model.gate.add_object("Gate_Grosssee")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Feldsee(shop):
    Gate = shop.model.gate.add_object("Gate_Feldsee")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Innerfragant(shop):
    Gate = shop.model.gate.add_object("Gate_Innerfragant")
    Gate.max_discharge.set(1000)

    return shop

def add_bypass_gate_Oschenik(shop):
    Gate = shop.model.gate.add_object("Gate_Oschenik")
    Gate.max_discharge.set(1000)

    return shop

def add_gate_Soboth_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_SOB_Drau")
    Gate.max_flow.set(1000.0)

    return shop

def add_gate_KAM_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_KAM_Drau")
    Gate.max_flow.set(1000.0)

    return shop

def add_gate_FRE_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_FRE_Drau")
    Gate.max_flow.set(1000.0)

    return shop

def add_gate_SOB_Drau(shop):
    Gate = shop.model.gate.add_object("Gate_SOB_Drau")
    Gate.max_flow.set(1000.0)

    return shop

def add_gate_Zirmsee_Grosssee(shop):
    Gate = shop.model.gate.add_object("Gate_Zirmsee_Grosssee")
    Gate.max_flow.set(3)

    return shop

def add_gate_Brettsee_Grosssee(shop):
    Gate = shop.model.gate.add_object("Gate_Brettsee_Grosssee")
    Gate.max_flow.set(1000)

    return shop

def add_gate_Kegelesee_Moell(shop):
    Gate = shop.model.gate.add_object("Gate_Kegelesee_Moell")
    Gate.max_flow.set(1000)

    return shop


