import pandas as pd
import numpy as np
from Misc import set_year_end_schedule,convert_head_to_vol

def load_special_conditions(shop,condition=""):

    if condition != "":
        print("############################################################")
        print("# WARNING: Loading special condition: " + condition)

    if condition == "empty_Fragant":
        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        Feldsee.inflow.set(0)
        Wurten.inflow.set(0)
        Oschenik.inflow.set(0)
        Innerfragant.inflow.set(0)
        Haselstein.inflow.set(0)
        Woella.inflow.set(0)
        Goessnitz.inflow.set(0)

        Grosssee.start_head.set(2390)
        Feldsee.start_head.set(2196)
        Wurten.start_head.set(1675)
        Oschenik.start_head.set(2245)
        Innerfragant.start_head.set(1193)
        Haselstein.start_head.set(1461)
        Woella.start_head.set(1534.5)
        Goessnitz.start_head.set(745.7)
        Moell.start_head.set(339)

    elif condition == "Fragant_2035":
        Grosssee = shop.model.reservoir.Grosssee
        Feldsee = shop.model.reservoir.Feldsee
        Wurten = shop.model.reservoir.Wurten
        Oschenik = shop.model.reservoir.Oschenik
        Innerfragant = shop.model.reservoir.Innerfragant
        Haselstein = shop.model.reservoir.Haselstein
        Woella = shop.model.reservoir.Woella
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        #Feldsee.inflow.set(0)
        #Wurten.inflow.set(0)
        #Oschenik.inflow.set(0)
        #Innerfragant.inflow.set(0)
        #Haselstein.inflow.set(0)
        #Woella.inflow.set(0)
        #Goessnitz.inflow.set(0)

        Grosssee.start_head.set(2407)
        Feldsee.start_head.set(2196)
        Wurten.start_head.set(1675)
        Oschenik.start_head.set(2377)
        Innerfragant.start_head.set(1193)
        Haselstein.start_head.set(1465)
        Woella.start_head.set(1534.5)
        Goessnitz.start_head.set(746)
        Moell.start_head.set(339)

    elif condition == "Fragant_2035_small":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        # Reservoirs
        Oschenik = shop.model.reservoir.Oschenik
        Wurten = shop.model.reservoir.Wurten
        Innerfragant = shop.model.reservoir.Innerfragant
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        # Start head
        Oschenik.start_head.set(2377)
        #Oschenik.start_head.set(2331.42)       #FEB
        #Oschenik.start_head.set(2329.98)       #MAR
        #Oschenik.start_head.set(2333.94)       #APR
        #Oschenik.start_head.set(2345.31)       #MAY
        #Oschenik.start_head.set(2365.86)       #JUN
        Wurten.start_head.set(1685)
        Innerfragant.start_head.set(1198)
        Goessnitz.start_head.set(746)
        Moell.start_head.set(339)

        # Condition Oschenik
        # ([ Ende Jänner, Ende Feber, Ende März, Ende April, Ende Mai, Ende Juni]) etc.
        #Oschenik.min_head_constr.set(pd.Series([2331.42, 2329.98, 2333.94, 2345.31, 2365.86,2385.37],
        #                                     index=[starttime,
        #                                            pd.Timestamp(2024,2,1),
        #                                            pd.Timestamp(2024,3,1),
        #                                            pd.Timestamp(2024,4,1),
        #                                            pd.Timestamp(2024,5,1),
        #                                            endtime - pd.Timedelta(1, unit='H')], name=0))

        Oschenik.min_head_constr.set(pd.Series([2000, 2385.37],
                                             index=[starttime,
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))




        # Condition Wurten
        Wurten.min_head_constr.set(pd.Series([1685.0, 1685.0],
                                             index=[starttime,
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

    elif condition == "Goessnitz_2035_small":
        Goessnitz = shop.model.reservoir.Goessnitz
        Moell = shop.model.reservoir.Moell

        Goessnitz.start_head.set(746)
        Moell.start_head.set(339)

    elif condition == "Kamering_default":
        Wiederschwing = shop.model.reservoir.Wiederschwing
        Wiederschwing.start_head.set(676)

    elif condition == "Koralpe_23_24_empty":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        # Endpoint desc Soboth, 11.82 hm3 = 1075 masl
        #schedule, schedule_flag, date_range = set_year_end_schedule(shop, 11.82) #Mm3
        #Soboth.schedule.set(pd.Series(schedule, index=date_range))
        #Soboth.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        #Soboth.upper_slack.set(11.80)
        #Soboth.lower_slack.set(11.84)

        Soboth.start_head.set(1078.24)

        # Soboth.min_head_constr.set(pd.Series([1,2,3,4,5,6],
        # Soboth.min_head_constr.set(pd.Series([1060.0, 1079.0, 1060.0, 1079.0,1060.0,1075]
        Soboth.min_head_constr.set(pd.Series([1079.0, 1060.0, 1079.0,1060.0,1075],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 11, 1),
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080.0, 1080.0, 1080.0, 1080.0],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2023, 12, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "Koralpe_23_24_empty2":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.start_head.set(1074.96)

        Soboth.min_head_constr.set(pd.Series([1005.0, 1079.0, 1060.0, 1075],
                                             index=[starttime,
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080.0, 1005.0, 1010.1, 1080.0, 1075.0],
                                             index=[starttime,                      # starttime
                                                    pd.Timestamp(2023, 11, 5),      # Abstau WK3 1010,1 bis 1004,0 müA. 31.05.2023 - 05.11.2023
                                                    pd.Timestamp(2023, 11, 18),     # Wiederaufstau WK3 bis 1010,1
                                                    pd.Timestamp(2023, 12, 2),      # Beginn Wiederaufstau
                                                    pd.Timestamp(2025, 1, 1)],      # Ende Rechnung
                                             name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    # 2022-02-02 Test Walter
    elif condition == "Koralpe_23_24_default":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1060.0, 1079.0, 1060.0, 1079.0,1060.0,1075],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 6, 15),
                                                    pd.Timestamp(2023, 11, 1),
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080.0, 1080.0, 1080.0, 1080.0],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2023, 12, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    # 2025 default
    elif condition == "Koralpe_26_default":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        # Endpoint desc Soboth, 11.82 hm3 = 1075 masl
        #schedule, schedule_flag, date_range = set_year_end_schedule(shop, 11.82) #Mm3
        #Soboth.schedule.set(pd.Series(schedule, index=date_range))
        #Soboth.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        #Soboth.upper_slack.set(11.80)
        #Soboth.lower_slack.set(11.84)

        Soboth.start_head.set(1075.0)

        # Soboth.min_head_constr.set(pd.Series([1,2,3,4,5,6],
        # Soboth.min_head_constr.set(pd.Series([1060.0, 1079.0, 1060.0, 1079.0,1060.0,1075]
        Soboth.min_head_constr.set(pd.Series([1060.0,
                                              1079.0,
                                              1060.0,
                                              1075],
                                             index=[starttime,
                                                    pd.Timestamp(2026, 6, 15),
                                                    pd.Timestamp(2026, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080.0, 1080.0, 1080.0, 1080.0],
                                             index=[starttime,
                                                    pd.Timestamp(2026, 6, 15),
                                                    pd.Timestamp(2026, 11, 1),
                                                    pd.Timestamp(2026, 12, 31)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

        # Endpoint desc Soboth
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 11.85325) #Mm3
        Soboth.schedule.set(pd.Series(schedule, index=date_range))
        Soboth.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Soboth.upper_slack.set(11.85)
        Soboth.lower_slack.set(11.84)

    # 2025 default incl. Revisionen
    elif condition == "Koralpe_25_revision_default":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        # Endpoint desc Soboth, 11.82 hm3 = 1075 masl
        #schedule, schedule_flag, date_range = set_year_end_schedule(shop, 11.82) #Mm3
        #Soboth.schedule.set(pd.Series(schedule, index=date_range))
        #Soboth.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        #Soboth.upper_slack.set(11.80)
        #Soboth.lower_slack.set(11.84)

        Soboth.start_head.set(1075.0)

        # Soboth.min_head_constr.set(pd.Series([1,2,3,4,5,6],
        # Soboth.min_head_constr.set(pd.Series([1060.0, 1079.0, 1060.0, 1079.0,1060.0,1075]
        Soboth.min_head_constr.set(pd.Series([1060.0,
                                              1079.0,
                                              1060.0,
                                              1075],
                                             index=[starttime,
                                                    pd.Timestamp(2025, 6, 15),
                                                    pd.Timestamp(2025, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080.0, 1080.0, 1080.0, 1080.0],
                                             index=[starttime,
                                                    pd.Timestamp(2025, 6, 15),
                                                    pd.Timestamp(2025, 11, 1),
                                                    pd.Timestamp(2026, 1, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

        # Endpoint desc Soboth
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 11.85325) #Mm3
        Soboth.schedule.set(pd.Series(schedule, index=date_range))
        Soboth.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Soboth.upper_slack.set(11.85)
        Soboth.lower_slack.set(11.84)

    # 2023-06-15 Bewertungsanfrage Siebenbuerger
    elif condition == "Koralpe_24_25_default":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1060.0, 1079.0, 1060.0, 1079.0,1060.0,1075],
                                             index=[starttime,
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    pd.Timestamp(2025, 6, 15),
                                                    pd.Timestamp(2025, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080.0, 1080.0, 1080.0, 1080.0],
                                             index=[starttime, pd.Timestamp(2024, 11, 13), pd.Timestamp(2024, 11, 17),
                                                    pd.Timestamp(2025, 12, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    # 2023-05-15 Update Matzer
    elif condition == "Koralpe_23_24_Matzer":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1005, 1079, 1080, 1075],
                                             index=[starttime,                      # starttime
                                                    pd.Timestamp(2023, 6, 15),      # Badepegel 15.06.2023
                                                    pd.Timestamp(2023, 9, 1),       # Vorzeitiges Verlassen Badepegel am 01.09.2023
                                                    pd.Timestamp(2024, 6, 15),      # Erreichen Badepegel 2024
                                                    pd.Timestamp(2024, 11, 1),      # Ende Badepegel 2024
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1010.1, 1005.1, 1010.1, 1080, 1075],
                                             index=[starttime,                      # starttime
                                                    pd.Timestamp(2023, 10, 30),     # Erreichen Kote 1010,1 müA. am 30. Oktober 2023
                                                    pd.Timestamp(2023, 11, 5),      # Abstau WK3 1010,1 bis 1004,0 müA. 31.05.2023 - 05.11.2023
                                                    pd.Timestamp(2023, 11, 18),     # Wiederaufstau WK3 bis 1010,1
                                                    pd.Timestamp(2023, 12, 2),      # Beginn Wiederaufstau
                                                    pd.Timestamp(2025, 1, 1)],      # Ende Rechnung
                                             name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    # Absenkung KOR falls Badepegel nicht vorzeitig verlassen werden darf
    elif condition == "Koralpe_23_24_orig_oct":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1014.4, 1010.0, 1079, 1053.5, 1075],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 6, 15),
                                                    pd.Timestamp(2023, 11, 1),
                                                    pd.Timestamp(2023, 11, 13),
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1014.5, 1010.1, 1080],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2023, 12, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    # Revision wie kommuniziert 2022/09 (Matzer)
    elif condition == "Koralpe_23_24_orig":
        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1014.4, 1010.0, 1079, 1053.5, 1075],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 6, 15),
                                                    pd.Timestamp(2023, 9, 1),
                                                    pd.Timestamp(2023, 11, 13),
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1014.5, 1010.1, 1080],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2023, 12, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "Koralpe_23_24_Jan":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1014.4, 1010.0,
                                              1079, 1053.5, 1075],
                                             index=[starttime, pd.Timestamp(2023, 6, 15), pd.Timestamp(2023, 9, 1),
                                                    pd.Timestamp(2023, 11, 13),
                                                    pd.Timestamp(2024, 6, 15), pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1014.5, 1010.1, 1080],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2024, 1, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "Koralpe_23_24_Feb":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1014.4, 1010.0, 1079, 1053.5, 1075],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 6, 15),
                                                    pd.Timestamp(2023, 9, 1),
                                                    pd.Timestamp(2023, 11, 13),
                                                    pd.Timestamp(2024, 6, 15),
                                                    pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1014.5, 1010.1, 1080],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2024, 2, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "Koralpe_23_24_Mar":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1014.4, 1010.0,
                                              1079, 1053.5, 1075],
                                             index=[starttime, pd.Timestamp(2023, 6, 15), pd.Timestamp(2023, 9, 1),
                                                    pd.Timestamp(2023, 11, 13),
                                                    pd.Timestamp(2024, 6, 15), pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1014.5, 1010.1, 1080],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2024, 3, 1)], name=0))



        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "Koralpe_23_24_Apr":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1014.4, 1010.0,
                                              1079, 1053.5, 1075],
                                             index=[starttime, pd.Timestamp(2023, 6, 15), pd.Timestamp(2023, 9, 1),
                                                    pd.Timestamp(2023, 11, 13),
                                                    pd.Timestamp(2024, 6, 15), pd.Timestamp(2024, 11, 1),
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Soboth.max_head_constr.set(pd.Series([1080, 1014.5, 1010.5, 1080],
                                             index=[starttime, pd.Timestamp(2023, 11, 13), pd.Timestamp(2023, 11, 17),
                                                    pd.Timestamp(2024, 4, 1)], name=0))



        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "Koralpe_23_24_final":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Soboth = shop.model.reservoir.Soboth

        Soboth.lrl.set(1010.1)

        Soboth.min_head_constr.set(pd.Series([1053.5, 1079, 1010.0, 1079, 1053.5, 1075],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 6, 15),      # 1079
                                                    pd.Timestamp(2023, 9, 1),       # 1010
                                                    pd.Timestamp(2024, 6, 15),      # 1079
                                                    pd.Timestamp(2024, 11, 1),      # 1053.5
                                                    endtime - pd.Timedelta(1, unit='H')], name=0)) #1075

        Soboth.max_head_constr.set(pd.Series([1080, 1010.1, 1080],
                                             index=[starttime,
                                                    pd.Timestamp(2023, 10, 30),
                                                    pd.Timestamp(2023, 12, 1)], name=0))

        Soboth.max_head_constr_flag.set(1)
        Soboth.min_head_constr_flag.set(1)

    elif condition == "PSKW_Grosssee_default":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Zirmsee = shop.model.reservoir.Zirmsee
        Brettsee = shop.model.reservoir.Brettsee
        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Wurten = shop.model.reservoir.Wurten
        Moell = shop.model.reservoir.Moell

        #KW_Brettsee = shop.model.plant.Brettsee

        Grosssee.start_head.set(2407)       # 19.727 hm³
        Brettsee.start_head.set(2510)   # 0.19501 hm³
        Moell.start_head.set(339)
        Zirmsee.start_head.set(2510)
        Kegelesee.start_head.set(2170)  # 0.70 hm³
        Wurten.start_head.set(1680)     #

        # Inflows
        #Zirmsee.inflow.set(0)
        #Brettsee.inflow.set(0)
        #Grosssee.inflow.set(0)
        #Kegelesee.inflow.set(0)
        #Wurten.inflow.set(0)

        # Endpoint desc Grosssee
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 19.727) #Mm3
        Grosssee.schedule.set(pd.Series(schedule, index=date_range))
        Grosssee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Grosssee.upper_slack.set(19.73)
        Grosssee.lower_slack.set(19.71)

        # Endpoint desc Zirmsee
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 3.21) #Mm3
        Zirmsee.schedule.set(pd.Series(schedule, index=date_range))
        Zirmsee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Zirmsee.upper_slack.set(3.22)
        Zirmsee.lower_slack.set(3.20)

        # Endpoint desc Brettsee
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 0.19501)  # Mm3
        Brettsee.schedule.set(pd.Series(schedule, index=date_range))
        Brettsee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Brettsee.upper_slack.set(0.196)
        Brettsee.lower_slack.set(0.194)

        #shop.model.plant.Brettsee.maintenance_flag.set(pd.Series([0,1,0], index=[starttime, start, end]))

        #shop.model.generator[ob.get_name()].maintenance_flag.set(pd.Series(status, index=timeline))
        #shop.model.pump[ob.get_name()].maintenance_flag.set(pd.Series(status, index=timeline))
        #shop.model.plant.Haselstein.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, start, end]))

        # Endpoint desc Kegelesee
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 0.75)  # Mm3
        Kegelesee.schedule.set(pd.Series(schedule, index=date_range))
        Kegelesee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Kegelesee.upper_slack.set(0.76)
        Kegelesee.lower_slack.set(0.74)

    elif condition == "Kegele_simple":

        Grosssee = shop.model.reservoir.Grosssee_adv
        Kegelesee = shop.model.reservoir.Kegelesee
        Moell = shop.model.reservoir.Moell

        Grosssee.start_head.set(2380)   # 6.0742 hm³
        Moell.start_head.set(339)
        Kegelesee.start_head.set(2161)  # 0.70 hm³

        #Grosssee.inflow.set(0)
        #Kegelesee.inflow.set(0)
        #Brettsee.inflow.set(0)
        #Zirmsee.inflow.set(0)

        # Endpoint desc Grosssee
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 6.0742) #Mm3
        Grosssee.schedule.set(pd.Series(schedule, index=date_range))
        Grosssee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Grosssee.upper_slack.set(6.08)
        Grosssee.lower_slack.set(6.06)

        # Endpoint desc Kegelesee
        # 0,75000	2170
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 0.70)  # Mm3
        Kegelesee.schedule.set(pd.Series(schedule, index=date_range))
        Kegelesee.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Kegelesee.upper_slack.set(0.71)
        Kegelesee.lower_slack.set(0.69)

    elif condition == "Fragant_750MW":

        Oschenik = shop.model.reservoir.Oschenik
        Moell = shop.model.reservoir.Moell

        Oschenik.start_head.set(2377)
        Moell.start_head.set(339)

        # Endpoint desc Oschenik
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 21.684) #Mm3
        Oschenik.schedule.set(pd.Series(schedule, index=date_range))
        Oschenik.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Oschenik.upper_slack.set(21.69)
        Oschenik.lower_slack.set(21.68)

    elif condition == "Fragant_Stillstand":
        start = pd.Timestamp(2023,9,4)
        end = pd.Timestamp(2023,9,4,4)

        d = shop.get_time_resolution()['timeresolution'].index[:-1]
        mask = np.where(np.logical_and(d>=start,d<end))

        #setting tactical limits

        v = shop.model.reservoir.Innerfragant.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Innerfragant", 1194.5)
        shop.model.reservoir.Innerfragant.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        v = shop.model.reservoir.Haselstein.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Haselstein", 1462.0)
        shop.model.reservoir.Haselstein.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        v = shop.model.reservoir.Woella.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Woella", 1535.5)
        shop.model.reservoir.Woella.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        start = pd.Timestamp(2023,9,4)
        end = pd.Timestamp(2023,9,9)

        shop.model.plant.Haselstein.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Wurten.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Oschenik.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Oschenik_P1.maintenance_flag.set(pd.Series([1], index=[starttime], name=0))
        shop.model.plant.Oschenik_P23.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Woella.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Auszerfragant.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))

        #Oschenik
        start = pd.Timestamp(2023, 5, 15)
        end = pd.Timestamp(2023, 5, 18)
        d = shop.get_time_resolution()['timeresolution'].index[:-1]
        mask = np.where(np.logical_and(d>=start,d<end))

        v = shop.model.reservoir.Oschenik.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Oschenik", 2330)
        shop.model.reservoir.Oschenik.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        start = pd.Timestamp(2023, 5, 18)
        end = pd.Timestamp(2023, 6, 30)
        v1 = 2330
        v2 = 2377

        d = shop.get_time_resolution()['timeresolution'].index[:-1]
        mask = np.where(np.logical_and(d>=start,d<end))

        slope = (v2 - v1) / len(mask[0])
        v_add = []
        for i in np.arange(0, len(mask[0])):
            v_add.append(convert_head_to_vol("Oschenik", i*slope+v1))

        v = shop.model.reservoir.Oschenik.tactical_limit_max.get().values
        v[mask] =  v_add
        shop.model.reservoir.Oschenik.tactical_limit_max.set(pd.Series(v, index=d, name=0))

    elif condition == "Fragant_Stillstand_2024":
        #start = pd.Timestamp(2024,8,5)
        #end = pd.Timestamp(2024,8,5,4)

        #start = pd.Timestamp(2024,7,1)
        #end = pd.Timestamp(2024,7,1,4)

        start = pd.Timestamp(2024,9,23)
        end = pd.Timestamp(2024,9,23,4)

        d = shop.get_time_resolution()['timeresolution'].index[:-1]
        mask = np.where(np.logical_and(d>=start,d<end))

        #setting tactical limits

        v = shop.model.reservoir.Innerfragant.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Innerfragant", 1194.5)
        shop.model.reservoir.Innerfragant.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        v = shop.model.reservoir.Haselstein.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Haselstein", 1462.0)
        shop.model.reservoir.Haselstein.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        v = shop.model.reservoir.Woella.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Woella", 1535.5)
        shop.model.reservoir.Woella.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        #start = pd.Timestamp(2024,8,5)
        #end = pd.Timestamp(2024,8,10)

        #start = pd.Timestamp(2024,7,1)
        #end = pd.Timestamp(2024,7,6)

        start = pd.Timestamp(2024,9,23)
        end = pd.Timestamp(2024,9,28)

        shop.model.plant.Haselstein.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Wurten.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Oschenik.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Oschenik_P1.maintenance_flag.set(pd.Series([1], index=[starttime], name=0))
        shop.model.plant.Oschenik_P23.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Woella.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))
        shop.model.plant.Auszerfragant.maintenance_flag.set(pd.Series([0,1,0], index=[starttime,start,end], name=0))

    elif condition == "Fragant_Normal":
        start = pd.Timestamp(2025, 5, 15)
        end = pd.Timestamp(2025, 5, 18)
        d = shop.get_time_resolution()['timeresolution'].index[:-1]
        mask = np.where(np.logical_and(d>=start,d<end))

        v = shop.model.reservoir.Oschenik.tactical_limit_max.get().values
        v[mask] = convert_head_to_vol("Oschenik", 2330)
        shop.model.reservoir.Oschenik.tactical_limit_max.set(pd.Series(v,index=d, name=0))

        start = pd.Timestamp(2025, 5, 18)
        end = pd.Timestamp(2025, 6, 30)
        v1 = 2330
        v2 = 2377

        d = shop.get_time_resolution()['timeresolution'].index[:-1]
        mask = np.where(np.logical_and(d>=start,d<end))

        slope = (v2 - v1) / len(mask[0])
        v_add = []
        for i in np.arange(0, len(mask[0])):
            v_add.append(convert_head_to_vol("Oschenik", i*slope+v1))

        v = shop.model.reservoir.Oschenik.tactical_limit_max.get().values
        v[mask] =  v_add
        shop.model.reservoir.Oschenik.tactical_limit_max.set(pd.Series(v, index=d, name=0))

    elif condition == "Bernegger_simple":

        Bernegger_upper = shop.model.reservoir.Bernegger_upper
        Bernegger_lower = shop.model.reservoir.Bernegger_lower

        Bernegger_upper.start_head.set(630)     # 0.62 hm³
        Bernegger_lower.start_head.set(30)      # 0.62 hm³

        Bernegger_upper.inflow.set(0)
        Bernegger_lower.inflow.set(0)

        # Endpoint desc Bernegger_upper
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 0.62) #Mm3
        Bernegger_upper.schedule.set(pd.Series(schedule, index=date_range))
        Bernegger_upper.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Bernegger_upper.upper_slack.set(0.61)
        Bernegger_upper.lower_slack.set(0.63)

    elif condition == "PSKW_Grosssee2_default":

        RSV1 = shop.model.reservoir.RSV1
        RSV2 = shop.model.reservoir.RSV2

        RSV1.start_head.set(92)     # 0.62 hm³
        RSV2.start_head.set(43)      # 0.62 hm³

        RSV1.inflow.set(0)
        RSV2.inflow.set(0)

        # Endpoint desc Bernegger_upper
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 6) #Mm3
        RSV1.schedule.set(pd.Series(schedule, index=date_range))
        RSV1.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        RSV1.upper_slack.set(5.99)
        RSV1.lower_slack.set(6.01)

    elif condition == "Malta_default":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        DMO = shop.model.plant.DMO
        DRP = shop.model.plant.DRP
        DMH = shop.model.plant.DMH
        DMU = shop.model.plant.DMU

        Koelnbrein = shop.model.reservoir.Koelnbrein
        Muehldorfersee = shop.model.reservoir.Muehldorfersee
        Galgenbichl = shop.model.reservoir.Galgenbichl
        Goesskar = shop.model.reservoir.Goesskar
        Rottau = shop.model.reservoir.Rottau
        #Moell = shop.model.reservoir.Moell


        Koelnbrein.start_head.set(1885)       # 38.31
        Muehldorfersee.start_head.set(2310)   # 1.38168 hm³
        Galgenbichl.start_head.set(1700)
        Goesskar.start_head.set(1700)
        Rottau.start_head.set(597.75)
        #Moell.start_head.set(339)

        # Endpoint desc Koelnbrein
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 38.31) #Mm3
        Koelnbrein.schedule.set(pd.Series(schedule, index=date_range))
        Koelnbrein.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Koelnbrein.upper_slack.set(38.25)
        Koelnbrein.lower_slack.set(38.35)

        #DRP.production_fee.set(pd.Series([6.91],index=[pd.Timestamp(2023,1,1)]))
        #DRP.consumption_fee.set(pd.Series([8.625],index=[pd.Timestamp(2023,1,1)]))

        Rottau.min_head_constr.set(pd.Series([596.5, 596.5],
                                             index=[starttime,
                                                    endtime - pd.Timedelta(1, unit='H')], name=0))

        Rottau.max_head_constr.set(pd.Series([597.75, 597.75],
                                             index=[starttime,
                                                    pd.Timestamp(2027, 1, 1)], name=0))

        Rottau.max_head_constr_flag.set(1)
        Rottau.min_head_constr_flag.set(1)

    elif condition == "Malta_simple":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        DMO = shop.model.plant.DMO
        DRP = shop.model.plant.DRP
        DMH = shop.model.plant.DMH
        DMU = shop.model.plant.DMU

        Koelnbrein = shop.model.reservoir.Koelnbrein
        Muehldorfersee = shop.model.reservoir.Muehldorfersee
        Galgenbichl = shop.model.reservoir.Galgenbichl
        Goesskar = shop.model.reservoir.Goesskar
        Rottau = shop.model.reservoir.Rottau
        #Moell = shop.model.reservoir.Moell


        Koelnbrein.start_head.set(1885)       # 38.31
        Muehldorfersee.start_head.set(2310)   # 1.38168 hm³
        Galgenbichl.start_head.set(1700)
        Goesskar.start_head.set(1700)
        Rottau.start_head.set(597.5)
        #Moell.start_head.set(339)

        # Endpoint desc Koelnbrein
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 38.31) #Mm3
        Koelnbrein.schedule.set(pd.Series(schedule, index=date_range))
        Koelnbrein.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Koelnbrein.upper_slack.set(38.31)
        Koelnbrein.lower_slack.set(38.32)

        #DRP.production_fee.set(pd.Series([6.91],index=[pd.Timestamp(2023,1,1)]))
        #DRP.consumption_fee.set(pd.Series([8.625],index=[pd.Timestamp(2023,1,1)]))

    elif condition == "Malta_Kolbnitz_default":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Koelnbrein = shop.model.reservoir.Koelnbrein
        Muehldorfersee = shop.model.reservoir.Muehldorfersee
        Galgenbichl = shop.model.reservoir.Galgenbichl
        Goesskar = shop.model.reservoir.Goesskar
        Rottau = shop.model.reservoir.Rottau
        Kolbnitz = shop.model.reservoir.Kolbnitz
        #Moell = shop.model.reservoir.Moell


        Koelnbrein.start_head.set(1885)       # 38.31
        Muehldorfersee.start_head.set(2310)   # 1.38168 hm³
        Galgenbichl.start_head.set(1700)
        Goesskar.start_head.set(1700)
        Rottau.start_head.set(597.5)
        #Moell.start_head.set(339)


        # Inflows
        #Zirmsee.inflow.set(0)
        #Brettsee.inflow.set(0)
        #Grosssee.inflow.set(0)
        #Kegelesee.inflow.set(0)
        #Wurten.inflow.set(0)

        # Endpoint desc Grosssee
        schedule, schedule_flag, date_range = set_year_end_schedule(shop, 38.31) #Mm3
        Koelnbrein.schedule.set(pd.Series(schedule, index=date_range))
        Koelnbrein.schedule_flag.set(pd.Series(schedule_flag, index=date_range))
        Koelnbrein.upper_slack.set(38.31)
        Koelnbrein.lower_slack.set(38.32)

    elif condition == "Kolbnitz_default":

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Rottau = shop.model.reservoir.Rottau
        Kolbnitz = shop.model.reservoir.Kolbnitz
        #Moell = shop.model.reservoir.Moell


        Rottau.start_head.set(597.5)
        Kolbnitz.start_head.set(702.5)
        #Moell.start_head.set(339)



        # Inflows
        #Zirmsee.inflow.set(0)
        #Brettsee.inflow.set(0)
        #Grosssee.inflow.set(0)
        #Kegelesee.inflow.set(0)
        #Wurten.inflow.set(0)

    elif condition == "Goessnitz_default":
        Goessnitz = shop.model.reservoir.Goessnitz
        #Goessnitz.inflow.set(0)
        #Goessnitz.start_head.set(745.7)

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Goessnitz.lrl.set(744.9)
        Goessnitz.hrl.set(746.3)  # highest regulated level in masl

        Goessnitz.start_head.set(745.0)

        Goessnitz.max_vol.set(0.385)  # maximum volume in Mm3            #  !!!! Special during "Entlandung" scaled down from 0.385Mm3 to 0.1703Mm3 (without "Freizeitspeicher")

        #Goessnitz.min_head_constr.set(pd.Series([744.9, 744.9, 744.9],
        #                                   index=[starttime,
        #                                            pd.Timestamp(2026, 1, 20),
        #                                            endtime], name=0))

        #Goessnitz.max_head_constr.set(pd.Series([745.3, 745.3, 745.3],
         #                                    index=[starttime,
         #                                           pd.Timestamp(2026, 3, 30),
          #                                         endtime], name=0))

        Goessnitz.max_head_constr_flag.set(1)
        Goessnitz.min_head_constr_flag.set(1)

    elif condition == "Forstsee_default":
        Forstsee = shop.model.reservoir.Forstsee

        starttime = shop.get_time_resolution()['timeresolution'].index[0]
        endtime = shop.get_time_resolution()['timeresolution'].index[-1]

        Forstsee.max_vol.set(6.235705)  # maximum volume in Mm3
        Forstsee.lrl.set(586)  # lowest regulated level in masl
        Forstsee.hrl.set(605.5)  # highest regulated level in masl

        Forstsee.start_head.set(600.0)

        Forstsee.min_head_constr.set(pd.Series([586, 603, 586, 603, 586, 603, 586, 586],
                                           index=[starttime,
                                                  pd.Timestamp(2026, 6, 15), pd.Timestamp(2026, 10, 31),
                                                  pd.Timestamp(2027, 6, 15), pd.Timestamp(2027, 10, 31),
                                                  pd.Timestamp(2028, 6, 15), pd.Timestamp(2028, 10, 31),
                                                  endtime], name=0))   #Badepegel


        Forstsee.max_head_constr_flag.set(1)
        Forstsee.min_head_constr_flag.set(1)

    else:
        print("############################################################")
