from Generators_and_Turbines import *

#TODO: load fees from external source

########################################################################################################################
# AUSZERFRAGANT
########################################################################################################################
def add_PP_Auszerfragant(shop):

    AF = shop.model.plant.add_object('Auszerfragant')

    AF.outlet_line.set(713)
    AF.main_loss.set([0])
    AF.penstock_loss.set([1,1,1])
    #AF.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    #AF.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    AF.production_fee.set(pd.Series([6.38, 3.83], index=[pd.Timestamp(2024, 1, 1), pd.Timestamp(2025, 1, 1)]))

    AFg1 = shop.model.generator.add_object('AF_G1')
    AFg2 = shop.model.generator.add_object('AF_G2')
    AFg3 = shop.model.generator.add_object('AF_G3')

    AFg1.connect_to(AF)
    AFg2.connect_to(AF)
    AFg3.connect_to(AF)

    AFg1.penstock.set(1)
    AFg2.penstock.set(2)
    AFg3.penstock.set(3)

    # Auszerfragant: Generator 1

    AFg1.p_min.set(2)
    AFg1.p_max.set(32)
    AFg1.p_nom.set(32)
    AFg1.discharge.set(8)

    # Set the start cost for the generators
    AFg1.startcost.set(1000)
    AFg2.startcost.set(1000)
    AFg3.startcost.set(1000)


    g_eff, g_MW = get_AF_generator(1)
    flow, E475, E480, E485 = get_AF_turbine(1)

    AFg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    AFg1.turb_eff_curves.set([pd.Series(E475,index=flow,name=475),
                               pd.Series(E480,index=flow,name=480),
                               pd.Series(E485,index=flow,name=485)])

    # Auszerfragant: Generator 2

    AFg2.p_min.set(2)
    AFg2.p_max.set(32)
    AFg2.p_nom.set(32)
    AFg2.discharge.set(8)

    g_eff, g_MW = get_AF_generator(2)
    flow, E475, E480, E485 = get_AF_turbine(2)

    AFg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    AFg2.turb_eff_curves.set([pd.Series(E475,index=flow,name=475),
                               pd.Series(E480,index=flow,name=480),
                               pd.Series(E485,index=flow,name=485)])

    # Auszerfragant: Generator 3

    AFg3.p_min.set(2)
    AFg3.p_max.set(36)
    AFg3.p_nom.set(36)
    AFg3.discharge.set(9)

    g_eff, g_MW = get_AF_generator(3)
    flow, E475, E480, E485 = get_AF_turbine(3)

    AFg3.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    AFg3.turb_eff_curves.set([pd.Series(E475,index=flow,name=475),
                               pd.Series(E480,index=flow,name=480),
                               pd.Series(E485,index=flow,name=485)])

    return shop

########################################################################################################################
# DMH
########################################################################################################################
def add_PP_DMH(shop):

    DMH = shop.model.plant.add_object('DMH')

    DMH.outlet_line.set(598)
    DMH.main_loss.set([0])
    DMH.penstock_loss.set([0,0])

    # 2023
    DMH.production_fee.set(pd.Series([6.91],index=[pd.Timestamp(2023,1,1)]))
    DMH.consumption_fee.set(pd.Series([8.625],index=[pd.Timestamp(2023,1,1)]))
    # 2024
    #DMH.production_fee.set(pd.Series([6.38],index=[pd.Timestamp(2024,1,1)]))
    #DMH.consumption_fee.set(pd.Series([5.26],index=[pd.Timestamp(2024,1,1)]))

    DMHg1 = shop.model.generator.add_object('DMH_G1')
    DMHg2 = shop.model.generator.add_object('DMH_G2')
    DMHg3 = shop.model.generator.add_object('DMH_G3')
    DMHg4 = shop.model.generator.add_object('DMH_G4')

    DMHg1.connect_to(DMH)
    DMHg2.connect_to(DMH)
    DMHg3.connect_to(DMH)
    DMHg4.connect_to(DMH)

    DMHg1.penstock.set(1)
    DMHg2.penstock.set(1)
    DMHg3.penstock.set(2)
    DMHg4.penstock.set(2)

    # DMH: Generator 1

    DMHg1.p_min.set(0)
    DMHg1.p_max.set(43.8)
    DMHg1.p_nom.set(43.8)
    DMHg1.discharge.set(0)
    DMHg1.startcost.set(0)

    g_eff, g_MW = get_DMH_generator()
    flow, E1, E2 = get_DMH_turbine()

    DMHg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMHg1.turb_eff_curves.set([pd.Series(E1,index=flow,name=1030),
                               pd.Series(E2,index=flow,name=1105)])

    # DMH: Generator 2

    DMHg2.p_min.set(0)
    DMHg2.p_max.set(43.8)
    DMHg2.p_nom.set(43.8)
    DMHg2.discharge.set(0)
    DMHg2.startcost.set(0)

    g_eff, g_MW = get_DMH_generator()
    flow, E1, E2 = get_DMH_turbine()

    DMHg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMHg2.turb_eff_curves.set([pd.Series(E1,index=flow,name=1030),
                               pd.Series(E2,index=flow,name=1105)])

    # DMH: Generator 3

    DMHg3.p_min.set(0)
    DMHg3.p_max.set(43.8)
    DMHg3.p_nom.set(43.8)
    DMHg3.discharge.set(0)
    DMHg3.startcost.set(0)

    g_eff, g_MW = get_DMH_generator()
    flow, E1, E2 = get_DMH_turbine()

    DMHg3.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMHg3.turb_eff_curves.set([pd.Series(E1,index=flow,name=1030),
                               pd.Series(E2,index=flow,name=1105)])

    # DMH: Generator 4

    DMHg4.p_min.set(0)
    DMHg4.p_max.set(43.8)
    DMHg4.p_nom.set(43.8)
    DMHg4.discharge.set(0)
    DMHg4.startcost.set(0)

    g_eff, g_MW = get_DMH_generator()
    flow, E1, E2 = get_DMH_turbine()

    DMHg4.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMHg4.turb_eff_curves.set([pd.Series(E1,index=flow,name=1030),
                               pd.Series(E2,index=flow,name=1105)])

    # DMH: Pump 2

    DMHp2 = shop.model.pump.add_object("DMH_P2")
    DMHp2.connect_to(shop.model.plant.DMH)
    DMHp2.penstock.set(1)
    DMHp2.p_nom.set(1)
    DMHp2.p_min.set(0)
    DMHp2.p_max.set(1000)
    DMHp2.startcost.set(0)
    DMHp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    DMHp2.turb_eff_curves.set([pd.Series([90.140], index=[4.346], name=1018),
                               pd.Series([90.820], index=[3.873], name=1097),
                               pd.Series([90.900], index=[3.728], name=1120),
                               pd.Series([91.910], index=[3.588], name=1142),
                               pd.Series([91.710], index=[3.230], name=1196)])

    # DMH: Pump 3

    DMHp3 = shop.model.pump.add_object("DMH_P3")
    DMHp3.connect_to(shop.model.plant.DMH)
    DMHp3.penstock.set(2)
    DMHp3.p_nom.set(1)
    DMHp3.p_min.set(0)
    DMHp3.p_max.set(1000)
    DMHp3.startcost.set(0)
    DMHp3.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    DMHp3.turb_eff_curves.set([pd.Series([90.140], index=[4.346], name=1018),
                               pd.Series([90.820], index=[3.873], name=1097),
                               pd.Series([90.900], index=[3.728], name=1120),
                               pd.Series([91.910], index=[3.588], name=1142),
                               pd.Series([91.710], index=[3.230], name=1196)])

    # Limit

    #DMH.max_p_constr.set(pd.Series([DMHg1.p_max.get()], [starttime]))
    #DMH.max_p_constr_flag.set(pd.Series([1], [starttime]))

    return shop

########################################################################################################################
# DMO
########################################################################################################################
def add_PP_DMO(shop):

    DMO = shop.model.plant.add_object('DMO')

    DMO.outlet_line.set(1692)
    DMO.main_loss.set([0])
    DMO.penstock_loss.set([0])

    # 2023
    DMO.production_fee.set(pd.Series([9.29],index=[pd.Timestamp(2025,1,1)]))
    DMO.consumption_fee.set(pd.Series([11.005],index=[pd.Timestamp(2025,1,1)]))
    # 2024
    #DMO.production_fee.set(pd.Series([6.38],index=[pd.Timestamp(2024,1,1)]))
    #DMO.consumption_fee.set(pd.Series([7.24],index=[pd.Timestamp(2024,1,1)]))

    DMOg1 = shop.model.generator.add_object('DMO_G1')
    DMOg2 = shop.model.generator.add_object('DMO_G2')

    DMOg1.connect_to(DMO)
    DMOg2.connect_to(DMO)

    DMOg1.penstock.set(1)
    DMOg2.penstock.set(1)

    # DMO: Generator 1

    DMOg1.p_min.set(0.46)
    DMOg1.p_max.set(19.4)
    DMOg1.p_nom.set(19.4)
    DMOg1.discharge.set(9.6)
    DMOg1.startcost.set(0)

    g_eff, g_MW = get_DMO_generator()
    flow, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 = get_DMO_turbine()

    mask = np.where(np.isnan(E1))
    flow_E1 = np.delete(flow, mask)
    E1 = np.delete(E1, mask)

    mask = np.where(np.isnan(E2))
    flow_E2 = np.delete(flow, mask)
    E2 = np.delete(E2, mask)

    mask = np.where(np.isnan(E3))
    flow_E3 = np.delete(flow, mask)
    E3 = np.delete(E3, mask)

    mask = np.where(np.isnan(E4))
    flow_E4 = np.delete(flow, mask)
    E4 = np.delete(E4, mask)

    mask = np.where(np.isnan(E5))
    flow_E5 = np.delete(flow, mask)
    E5 = np.delete(E5, mask)

    mask = np.where(np.isnan(E6))
    flow_E6 = np.delete(flow, mask)
    E6 = np.delete(E6, mask)

    mask = np.where(np.isnan(E7))
    flow_E7 = np.delete(flow, mask)
    E7 = np.delete(E7, mask)

    mask = np.where(np.isnan(E8))
    flow_E8 = np.delete(flow, mask)
    E8 = np.delete(E8, mask)

    mask = np.where(np.isnan(E9))
    flow_E9 = np.delete(flow, mask)
    E9 = np.delete(E9, mask)

    mask = np.where(np.isnan(E10))
    flow_E10 = np.delete(flow, mask)
    E10 = np.delete(E10, mask)

    mask = np.where(np.isnan(E11))
    flow_E11 = np.delete(flow, mask)
    E11 = np.delete(E11, mask)

    mask = np.where(np.isnan(E12))
    flow_E12 = np.delete(flow, mask)
    E12 = np.delete(E12, mask)

    mask = np.where(np.isnan(E13))
    flow_E13 = np.delete(flow, mask)
    E13 = np.delete(E13, mask)

    mask = np.where(np.isnan(E14))
    flow_E14 = np.delete(flow, mask)
    E14 = np.delete(E14, mask)

    mask = np.where(np.isnan(E15))
    flow_E15 = np.delete(flow, mask)
    E15 = np.delete(E15, mask)

    mask = np.where(np.isnan(E16))
    flow_E16 = np.delete(flow, mask)
    E16 = np.delete(E16, mask)

    mask = np.where(np.isnan(E17))
    flow_E17 = np.delete(flow, mask)
    E17 = np.delete(E17, mask)

    mask = np.where(np.isnan(E18))
    flow_E18 = np.delete(flow, mask)
    E18 = np.delete(E18, mask)

    mask = np.where(np.isnan(E19))
    flow_E19 = np.delete(flow, mask)
    E19 = np.delete(E19, mask)

    mask = np.where(np.isnan(E20))
    flow_E20 = np.delete(flow, mask)
    E20 = np.delete(E20, mask)

    mask = np.where(np.isnan(E21))
    flow_E21 = np.delete(flow, mask)
    E21 = np.delete(E21, mask)


    DMOg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMOg1.turb_eff_curves.set([pd.Series(E1,index=flow_E1,name=53),
                               pd.Series(E2,index=flow_E2,name=61.45),
                               pd.Series(E3,index=flow_E3,name=69.9),
                               pd.Series(E4,index=flow_E4,name=78.35),
                               pd.Series(E5,index=flow_E5,name=86.8),
                               pd.Series(E6,index=flow_E6,name=95.25),
                               pd.Series(E7,index=flow_E7,name=103.7),
                               pd.Series(E8,index=flow_E8,name=112.15),
                               pd.Series(E9,index=flow_E9,name=120.6),
                               pd.Series(E10,index=flow_E10,name=129.05),
                               pd.Series(E11,index=flow_E11,name=137.5),
                               pd.Series(E12,index=flow_E12,name=145.95),
                               pd.Series(E13,index=flow_E13,name=154.4),
                               pd.Series(E14,index=flow_E14,name=162.85),
                               pd.Series(E15,index=flow_E15,name=171.3),
                               pd.Series(E16,index=flow_E16,name=179.75),
                               pd.Series(E17,index=flow_E17,name=188.2),
                               pd.Series(E18,index=flow_E18,name=196.65),
                               pd.Series(E19,index=flow_E19,name=205.1),
                               pd.Series(E20,index=flow_E20,name=213.55),
                               pd.Series(E21,index=flow_E21,name=222)])

    # DMO: Generator 2

    DMOg2.p_min.set(0.46)
    DMOg2.p_max.set(19.4)
    DMOg2.p_nom.set(19.4)
    DMOg2.discharge.set(9.6)
    DMOg2.startcost.set(0)

    #g_eff, g_MW = get_DMO_generator()
    #flow, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 = get_DMO_turbine()

    DMOg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMOg2.turb_eff_curves.set([pd.Series(E1,index=flow_E1,name=53),
                               pd.Series(E2,index=flow_E2,name=61.45),
                               pd.Series(E3,index=flow_E3,name=69.9),
                               pd.Series(E4,index=flow_E4,name=78.35),
                               pd.Series(E5,index=flow_E5,name=86.8),
                               pd.Series(E6,index=flow_E6,name=95.25),
                               pd.Series(E7,index=flow_E7,name=103.7),
                               pd.Series(E8,index=flow_E8,name=112.15),
                               pd.Series(E9,index=flow_E9,name=120.6),
                               pd.Series(E10,index=flow_E10,name=129.05),
                               pd.Series(E11,index=flow_E11,name=137.5),
                               pd.Series(E12,index=flow_E12,name=145.95),
                               pd.Series(E13,index=flow_E13,name=154.4),
                               pd.Series(E14,index=flow_E14,name=162.85),
                               pd.Series(E15,index=flow_E15,name=171.3),
                               pd.Series(E16,index=flow_E16,name=179.75),
                               pd.Series(E17,index=flow_E17,name=188.2),
                               pd.Series(E18,index=flow_E18,name=196.65),
                               pd.Series(E19,index=flow_E19,name=205.1),
                               pd.Series(E20,index=flow_E20,name=213.55),
                               pd.Series(E21,index=flow_E21,name=222)])

    # DMO: Pump 1

    DMOp1 = shop.model.pump.add_object("DMO_P1")
    DMOp1.connect_to(shop.model.plant.DMO)
    DMOp1.penstock.set(1)
    DMOp1.p_nom.set(8.64)
    DMOp1.p_min.set(0)
    DMOp1.p_max.set(1000)
    DMOp1.startcost.set(0)
    DMOp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    DMOp1.turb_eff_curves.set([pd.Series([88.230], index=[2.712], name=56),
                               pd.Series([87.280], index=[7.080], name=56),
                               pd.Series([91.490], index=[5.832], name=143),
                               pd.Series([92.820], index=[6.768], name=230),
                               pd.Series([91.670], index=[8.640], name=230)])

    # DMO: Pump 2

    DMOp2 = shop.model.pump.add_object("DMO_P2")
    DMOp2.connect_to(shop.model.plant.DMO)
    DMOp2.penstock.set(1)
    DMOp2.p_nom.set(8.64)
    DMOp2.p_min.set(0)
    DMOp2.p_max.set(1000)
    DMOp2.startcost.set(0)
    DMOp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    DMOp2.turb_eff_curves.set([pd.Series([88.230], index=[2.712], name=56),
                               pd.Series([87.280], index=[7.080], name=56),
                               pd.Series([91.490], index=[5.832], name=143),
                               pd.Series([92.820], index=[6.768], name=230),
                               pd.Series([91.670], index=[8.640], name=230)])

    # Limit

    #DMO.max_p_constr.set(pd.Series([DMOg1.p_max.get()], [starttime]))
    #DMO.max_p_constr_flag.set(pd.Series([1], [starttime]))

    return shop

########################################################################################################################
# DRP
########################################################################################################################
def add_PP_DRP(shop):

    DRP = shop.model.plant.add_object('DRP')

    DRP.outlet_line.set(1680)
    DRP.main_loss.set([0])
    DRP.penstock_loss.set([0])

    # 2023
    DRP.production_fee.set(pd.Series([6.91],index=[pd.Timestamp(2023,1,1)]))
    DRP.consumption_fee.set(pd.Series([8.625],index=[pd.Timestamp(2023,1,1)]))
    # 2024
    #DRP.production_fee.set(pd.Series([6.38],index=[pd.Timestamp(2024,1,1)]))
    #DRP.consumption_fee.set(pd.Series([5.26],index=[pd.Timestamp(2024,1,1)]))

    DRPg1 = shop.model.generator.add_object('DRP_G1')
    DRPg2 = shop.model.generator.add_object('DRP_G2')

    DRPg1.connect_to(DRP)
    DRPg2.connect_to(DRP)

    DRPg1.penstock.set(1)
    DRPg2.penstock.set(1)

    # DRP: Generator 1

    DRPg1.p_min.set(19)
    DRPg1.p_max.set(51.6)
    DRPg1.p_nom.set(51.6)
    DRPg1.discharge.set(0)
    DRPg1.startcost.set(0)

    g_eff, g_MW = get_DRP_generator()
    flow, E1 = get_DRP_turbine()

    DRPg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DRPg1.turb_eff_curves.set([pd.Series(E1,index=flow,name=600)])

    # DRP: Generator 2

    DRPg2.p_min.set(19)
    DRPg2.p_max.set(51.6)
    DRPg2.p_nom.set(51.6)
    DRPg2.discharge.set(0)
    DRPg2.startcost.set(0)

    g_eff, g_MW = get_DRP_generator()
    flow, E1 = get_DRP_turbine()

    DRPg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DRPg2.turb_eff_curves.set([pd.Series(E1,index=flow,name=600)])

    # DRP: Pump 1

    DRPp1 = shop.model.pump.add_object("DRP_P1")
    DRPp1.connect_to(shop.model.plant.DRP)
    DRPp1.penstock.set(1)
    DRPp1.p_nom.set(0)
    DRPp1.p_min.set(0)
    DRPp1.p_max.set(1000)
    DRPp1.startcost.set(0)
    DRPp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    DRPp1.turb_eff_curves.set([pd.Series([93.810], index=[7.754], name=551),
                               pd.Series([90.000], index=[6.414], name=639)])

    # DRP: Pump 2

    DRPp2 = shop.model.pump.add_object("DRP_P2")
    DRPp2.connect_to(shop.model.plant.DRP)
    DRPp2.penstock.set(1)
    DRPp2.p_nom.set(0)
    DRPp2.p_min.set(0)
    DRPp2.p_max.set(1000)
    DRPp2.startcost.set(0)
    DRPp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    DRPp2.turb_eff_curves.set([pd.Series([93.810], index=[7.754], name=551),
                               pd.Series([90.000], index=[6.414], name=639)])

    # Limit

    #DRP.max_p_constr.set(pd.Series([DRPg1.p_max.get()], [starttime]))
    #DRP.max_p_constr_flag.set(pd.Series([1], [starttime]))

    return shop

########################################################################################################################
# DMU
########################################################################################################################
def add_PP_DMU(shop):

    DMU = shop.model.plant.add_object('DMU')

    DMU.outlet_line.set(553)
    DMU.main_loss.set([0])
    DMU.penstock_loss.set([0])

    # 2023
    DMU.production_fee.set(pd.Series([9.29],index=[pd.Timestamp(2023,1,1)]))
    # 2024
    #DMU.production_fee.set(pd.Series([6.38],index=[pd.Timestamp(2024,1,1)]))

    DMUg1 = shop.model.generator.add_object('DMU_G1')
    DMUg2 = shop.model.generator.add_object('DMU_G2')

    DMUg1.connect_to(DMU)
    DMUg2.connect_to(DMU)

    DMUg1.penstock.set(1)
    DMUg2.penstock.set(1)

    # DMU: Generator 1

    DMUg1.p_min.set(0)
    DMUg1.p_max.set(5.148)
    DMUg1.p_nom.set(5.148)
    DMUg1.discharge.set(13.20)
    DMUg1.startcost.set(0)

    g_eff, g_MW = get_DMU_generator()
    flow, E1, E2, E3 = get_DMU_turbine()

    DMUg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMUg1.turb_eff_curves.set([pd.Series(E1,index=flow,name=41),
                               pd.Series(E2,index=flow,name=44.7),
                               pd.Series(E3,index=flow,name=46)])

    # DMU: Generator 2

    DMUg2.p_min.set(0)
    DMUg2.p_max.set(5.148)
    DMUg2.p_nom.set(5.148)
    DMUg2.discharge.set(13.20)
    DMUg2.startcost.set(0)

    g_eff, g_MW = get_DMU_generator()
    flow, E1, E2, E3 = get_DMU_turbine()

    DMUg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    DMUg2.turb_eff_curves.set([pd.Series(E1,index=flow,name=41),
                               pd.Series(E2,index=flow,name=44.7),
                               pd.Series(E3,index=flow,name=46)])


    # Limit

    #DMU.max_p_constr.set(pd.Series([DMUg1.p_max.get()], [starttime]))
    #DMU.max_p_constr_flag.set(pd.Series([1], [starttime]))

    return shop

########################################################################################################################
# Kolbnitz
########################################################################################################################
def add_PP_KOLB(shop):

    KOLB = shop.model.plant.add_object('KOLB')

    KOLB.outlet_line.set(600)
    KOLB.main_loss.set([0])
    KOLB.penstock_loss.set([0])
    KOLB.production_fee.set(pd.Series([6.38],index=[pd.Timestamp(2024,1,1)]))

    KOLBg1 = shop.model.generator.add_object('KOLB_G1')

    KOLBg1.connect_to(KOLB)


    KOLBg1.penstock.set(1)

    # KOLB: Generator 1
    KOLBg1.p_min.set(0)
    KOLBg1.p_max.set(25)
    KOLBg1.p_nom.set(25)
    KOLBg1.discharge.set(30)
    KOLBg1.startcost.set(0)

    g_eff, g_MW = get_KOLB_generator()
    flow, E1 = get_KOLB_turbine()

    KOLBg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    KOLBg1.turb_eff_curves.set([pd.Series(E1,index=flow,name=105)])

    #KOLBg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    #KOLBg1.turb_eff_curves.set([pd.Series([82.011,82.729,83.167,83.300,83.107,82.564],index=[5,10,15,20,25,30],name=105)])

    return shop

########################################################################################################################
# GOESSNITZ
########################################################################################################################
def add_PP_Kolbnitz(shop):

    KOLB = shop.model.plant.add_object('KOLB')

    KOLB.outlet_line.set(600)
    KOLB.main_loss.set([0])
    KOLB.penstock_loss.set([0])

    KOLBg1 = shop.model.generator.add_object('KOLB_G1')

    KOLBg1.connect_to(KOLB)

    KOLBg1.penstock.set(1)

    # Kolbnitz Generator 1
    KOLBg1.p_min.set(0)
    KOLBg1.p_max.set(25)
    KOLBg1.p_nom.set(25)
    KOLBg1.discharge.set(30)
    KOLBg1.startcost.set(0)

    #GOg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    KOLBg1.turb_eff_curves.set([pd.Series([82.011,82.729,83.167,83.300,83.107,82.564],index=[5,10,15,20,25,30],name=105)])

    return shop

########################################################################################################################
# FELDSEE
########################################################################################################################
def add_PP_Feldsee(shop):

    FS = shop.model.plant.add_object('Feldsee')

    FS.outlet_line.set(1695)
    FS.main_loss.set([0])
    FS.penstock_loss.set([0,0])
    #FS.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    FS.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    #FS.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    FS.consumption_fee.set(pd.Series([4.235,5.76],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    FSg1 = shop.model.generator.add_object('FS_G1')
    FSg2 = shop.model.generator.add_object('FS_G2')

    FSg1.connect_to(FS)
    FSg2.connect_to(FS)

    FSg1.penstock.set(1)
    FSg2.penstock.set(2)

    # Feldsee: Generator 1

    FSg1.p_min.set(35)
    FSg1.p_max.set(70)
    FSg1.p_nom.set(70)
    FSg1.discharge.set(14.6)
    FSg1.startcost.set(0)

    g_eff, g_MW = get_Feldsee_generator()
    flow, E501, E526, E546 = get_Feldsee_turbine()

    FSg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    FSg1.turb_eff_curves.set([pd.Series(E501,index=flow,name=501),
                               pd.Series(E526,index=flow,name=526),
                               pd.Series(E546,index=flow,name=546)])

    # Feldsee: Generator 2

    FSg2.p_min.set(35)
    FSg2.p_max.set(70)
    FSg2.p_nom.set(70)
    FSg2.discharge.set(14.6)
    FSg2.startcost.set(0)

    g_eff, g_MW = get_Feldsee_generator()
    flow, E501, E526, E546 = get_Feldsee_turbine()

    FSg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    FSg2.turb_eff_curves.set([pd.Series(E501,index=flow,name=501),
                               pd.Series(E526,index=flow,name=526),
                               pd.Series(E546,index=flow,name=546)])

    # Feldsee: Pump 1

    FSp1 = shop.model.pump.add_object("FS_P1")
    FSp1.connect_to(FS)
    FSp1.penstock.set(1)
    FSp1.p_nom.set(65)
    FSp1.p_min.set(0)
    FSp1.p_max.set(1000)
    FSp1.startcost.set(0)
    FSp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    FSp1.turb_eff_curves.set([pd.Series([82], index=[11.2], name=493), pd.Series([82], index=[9.6], name=552)])

    # Feldsee: Pump 2

    FSp2 = shop.model.pump.add_object("FS_P2")
    FSp2.connect_to(FS)
    FSp2.penstock.set(2)
    FSp2.p_nom.set(65)
    FSp2.p_min.set(0)
    FSp2.p_max.set(1000)
    FSp2.startcost.set(0)
    FSp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    FSp2.turb_eff_curves.set([pd.Series([82], index=[11.2], name=493), pd.Series([82], index=[9.6], name=552)])

    return shop

def add_PP_Forstsee(shop):

    FOR = shop.model.plant.add_object('Forstsee')

    FOR.outlet_line.set(439.0)
    FOR.main_loss.set([0])
    FOR.penstock_loss.set([0])

    FOR.production_fee.set(pd.Series([0,0,0,
                                      0,0,0,
                                      0,0],
                            index=[pd.Timestamp(2019,1,1),pd.Timestamp(2020,1,1),pd.Timestamp(2021,1,1),
                                   pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1),
                                   pd.Timestamp(2025,1,1),pd.Timestamp(2027,1,1)]))

    #FOR.consumption_fee.set(pd.Series([3.75,3.75,3.75,
    #                                   4.805,13.215,3.75,
    #                                   3.75,3.75],
    #                        index=[pd.Timestamp(2019,1,1),pd.Timestamp(2020,1,1),pd.Timestamp(2021,1,1),
    #                               pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1),
    #                               pd.Timestamp(2025,1,1),pd.Timestamp(2027,1,1)]))

    FOR.consumption_fee.set(pd.Series([4.44,3.75,3.75,
                                       4.805,9.09,9.09,
                                       9.09,9.09],
                            index=[pd.Timestamp(2019,1,1),pd.Timestamp(2020,1,1),pd.Timestamp(2021,1,1),
                                   pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1),
                                   pd.Timestamp(2025,1,1),pd.Timestamp(2027,1,1)]))

    # Forstsee: Generator
    #FORg1 = shop.model.generator.add_object('FOR_G1')
    #FORg1.connect_to(FOR)
    #FORg1.penstock.set(1)
    #FORg1.p_min.set(0.2)
    #FORg1.p_max.set(2.3)
    #FORg1.p_nom.set(2.3)
    #FORg1.discharge.set(1.8)
    #FORg1.startcost.set(0)

    #g_eff, g_MW = get_Forstsee_generator(1)
    #flow, E165 = get_Forstsee_turbine(1)

    #FORg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    #FORg1.turb_eff_curves.set([pd.Series(E165,index=flow,name=165)])

    # Forstsee: Generator 2
    FORg2 = shop.model.generator.add_object('FOR_G2')
    FORg2.connect_to(FOR)
    FORg2.penstock.set(1)
    FORg2.p_min.set(0.2)
    FORg2.p_max.set(2.1)
    FORg2.p_nom.set(2.0)
    FORg2.discharge.set(1.5)
    FORg2.startcost.set(0)

    g_eff, g_MW = get_Forstsee_generator(2)
    flow, E165 = get_Forstsee_turbine(2)

    FORg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    FORg2.turb_eff_curves.set([pd.Series(E165,index=flow,name=165)])

    # Forstsee: Pump
    FORp1 = shop.model.pump.add_object("FOR_P1")
    FORp1.connect_to(shop.model.plant.Forstsee)
    FORp1.penstock.set(1)
    FORp1.p_nom.set(2.8)
    FORp1.p_min.set(2.5)
    FORp1.p_max.set(2.8)
    FORp1.startcost.set(0)
    FORp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    FORp1.turb_eff_curves.set([pd.Series([89.30], index=[1.68], name=148),pd.Series([89.60], index=[1.62], name=153),
                               pd.Series([89.85], index=[1.57], name=158),pd.Series([90.00], index=[1.52], name=163),
                               pd.Series([89.50], index=[1.47], name=168)])

    return shop

########################################################################################################################
# FREIBACH
########################################################################################################################
def add_PP_Freibach(shop):

    FB = shop.model.plant.add_object('Freibach')

    FB.outlet_line.set(410)
    FB.main_loss.set([0])
    FB.penstock_loss.set([0,0])
    FB.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    FB.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    FBg1 = shop.model.generator.add_object('FB_G1')

    FBg1.connect_to(FB)

    FBg1.penstock.set(1)

    # Feldsee: Generator 1

    FBg1.p_min.set(7)
    FBg1.p_max.set(17)
    FBg1.p_nom.set(17)
    FBg1.discharge.set(6.5)
    FBg1.startcost.set(0)

    g_eff, g_MW = get_Freibach_generator()
    flow, E324 = get_Freibach_turbine()

    FBg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    FBg1.turb_eff_curves.set([pd.Series(E324,index=flow,name=324)])

    # Feldsee: Pump 1

    FBp2 = shop.model.pump.add_object("FB_P2")
    FBp2.connect_to(FB)
    FBp2.penstock.set(2)
    FBp2.p_nom.set(65)
    FBp2.p_min.set(0)
    FBp2.p_max.set(1000)
    FBp2.startcost.set(0)
    FBp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    FBp2.turb_eff_curves.set([pd.Series([80.5], index=[1.35], name=304), pd.Series([75.85], index=[1.16], name=333)])

    #### MAINTANANCE FLAG
    #starttime = shop.get_time_resolution()['timeresolution'].index[0]
    #FBp2.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 5, 1), pd.Timestamp(2025, 8, 30)], name=0))
    #FBg1.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 5, 1), pd.Timestamp(2025, 6, 30)], name=0))

    return shop

########################################################################################################################
# GOESSNITZ
########################################################################################################################
def add_PP_Goessnitz(shop):

    GO = shop.model.plant.add_object('Goessnitz')

    GO.outlet_line.set(709.6)
    GO.main_loss.set([0])
    GO.penstock_loss.set([0,0])

    GOg1 = shop.model.generator.add_object('GO_G1')
    GOg2 = shop.model.generator.add_object('GO_G2')

    GOg1.connect_to(GO)
    GOg2.connect_to(GO)

    GOg1.penstock.set(1)
    GOg2.penstock.set(2)

    # Goessnitz: Generator 1

    GOg1.p_min.set(0)
    GOg1.p_max.set(1)
    GOg1.p_nom.set(1)
    GOg1.discharge.set(3.5)
    GOg1.startcost.set(0)

    #GOg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    GOg1.turb_eff_curves.set([pd.Series([75, 75, 74.9],index=[1.9, 2.1, 2.3],name=35)])

    # Goessnitz: Generator 2

    GOg2.p_min.set(0)
    GOg2.p_max.set(8)
    GOg2.p_nom.set(8)
    GOg2.discharge.set(25)
    GOg2.startcost.set(0)

    #GOg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    GOg2.turb_eff_curves.set([pd.Series([80, 82, 80],index=[5.34, 20, 25],name=85)])


    return shop

########################################################################################################################
# HASELSTEIN
########################################################################################################################
def add_PP_Haselstein(shop):

    HA = shop.model.plant.add_object('Haselstein')

    HA.outlet_line.set(1205)
    HA.main_loss.set([0])
    HA.penstock_loss.set([0])
    HA.production_fee.set(pd.Series([0],index=[pd.Timestamp(2022,1,1)]))
    #HA.consumption_fee.set(pd.Series([4.805,13.215],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    HA.consumption_fee.set(pd.Series([4.805,5.76],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    HAg1 = shop.model.generator.add_object('HA_G1')
    HAg1.connect_to(HA)
    HAg1.penstock.set(1)


    # Haselstein: Generator 1

    HAg1.p_min.set(3.9)
    HAg1.p_max.set(4)
    HAg1.p_nom.set(4)
    HAg1.discharge.set(1.8)
    HAg1.max_q_constr.set(1000) ###
    HAg1.startcost.set(0)

    g_eff, g_MW = get_Haselstein_generator()
    flow, E260 = get_Haselstein_turbine()

    HAg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    HAg1.turb_eff_curves.set([pd.Series(E260,index=flow,name=260)])

    # Haselstein: Pump 1

    HAp1 = shop.model.pump.add_object("HA_P1")
    HAp1.connect_to(HA)
    HAp1.penstock.set(1)
    HAp1.p_nom.set(5.2) # 1.716
    HAp1.p_min.set(0)
    HAp1.p_max.set(1000)
    HAp1.startcost.set(0)
    HAp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    HAp1.turb_eff_curves.set([pd.Series([90], index=[1.864], name=256),pd.Series([90], index=[1.716], name=278)])

    #HAp1 = shop.model.pump.add_object("HA_P1")
    #HAp1.connect_to(HA)
    #HAp1.penstock.set(1)
    #HAp1.p_nom.set(5.2)
    #HAp1.p_min.set(0)
    #HAp1.p_max.set(1000)
    #HAp1.startcost.set(0)
    #HAp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    #HAp1.turb_eff_curves.set([pd.Series([90], index=[1.716], name=278),pd.Series([90], index=[1.864], name=256)])

    return shop

########################################################################################################################
# KAMERING
########################################################################################################################
def add_PP_Kamering(shop):

    KA = shop.model.plant.add_object('Kamering')

    KA.outlet_line.set(513.97)
    KA.main_loss.set([0])
    KA.penstock_loss.set([0])
    KA.production_fee.set(pd.Series([2.01],index=[pd.Timestamp(2022,1,1)]))

    KAg1 = shop.model.generator.add_object('KA_G1')

    KAg1.connect_to(KA)

    KAg1.penstock.set(1)

    # Kamering: Generator 1

    KAg1.p_min.set(5)
    KAg1.p_max.set(10)
    KAg1.p_nom.set(10)
    KAg1.discharge.set(7.5)
    KAg1.startcost.set(0)

    g_eff, g_MW = get_Kamering_generator()
    flow, E155 = get_Kamering_turbine()

    KAg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    KAg1.turb_eff_curves.set([pd.Series(E155,index=flow,name=155)])

    return shop

########################################################################################################################
# KORALPE
########################################################################################################################
def add_PP_Koralpe(shop):

    starttime = shop.get_time_resolution()['timeresolution'].index[0]

    KOR = shop.model.plant.add_object('Koralpe')

    KOR.outlet_line.set(344.5)
    KOR.main_loss.set([0])
    KOR.penstock_loss.set([0, 0])
    # Values old - 2023/03 KOR.production_fee.set(pd.Series([1.44,9.29,1.44],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1)]))
    # Values old - 2023/02 KOR.consumption_fee.set(pd.Series([4.235,11.005,4.235],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1)]))

    #Values new, update 2023/02/17
    #KOR.production_fee.set(pd.Series([1.44,8.21,5.81],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1)]))
    #KOR.consumption_fee.set(pd.Series([4.235,4.75,4.65],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1),pd.Timestamp(2024,1,1)]))

    KOR.production_fee.set(pd.Series([6.38,6.38,6.38],index=[pd.Timestamp(2024,1,1),pd.Timestamp(2025,1,1),pd.Timestamp(2026,1,1)]))
    KOR.consumption_fee.set(pd.Series([7.24,7.24,7.24],index=[pd.Timestamp(2024,1,1),pd.Timestamp(2025,1,1),pd.Timestamp(2026,1,1)]))

    KORg1 = shop.model.generator.add_object('KOR_G1')
    KORg2 = shop.model.generator.add_object('KOR_G2')

    KORg1.connect_to(KOR)
    KORg2.connect_to(KOR)

    KORg1.penstock.set(1)
    KORg2.penstock.set(1)

    # Koralpe: Generator 1

    KORg1.p_min.set(2)
    KORg1.p_max.set(55)
    KORg1.p_nom.set(55)
    KORg1.discharge.set(10)
    KORg1.startcost.set(0)

    g_eff, g_MW = get_Koralpe_generator(1)
    flow, E660, E700, E735 = get_Koralpe_turbine(1)

    KORg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    KORg1.turb_eff_curves.set([pd.Series(E660,index=flow,name=660),
                               pd.Series(E700,index=flow,name=700),
                               pd.Series(E735,index=flow,name=735)])

    # Koralpe: Generator 2

    KORg2.p_min.set(0)
    KORg2.p_max.set(28)
    KORg2.p_nom.set(28)
    KORg2.discharge.set(4.6)
    KORg2.startcost.set(0)

    g_eff, g_MW = get_Koralpe_generator(2)
    flow, E731 = get_Koralpe_turbine(2)

    KORg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    KORg2.turb_eff_curves.set([pd.Series(E731,index=flow,name=731)])

    # Koralpe: Pump 2

    KORp2 = shop.model.pump.add_object("KOR_P1")
    KORp2.connect_to(shop.model.plant.Koralpe)
    KORp2.penstock.set(2)
    KORp2.p_nom.set(3.817471)
    KORp2.p_min.set(0)
    KORp2.p_max.set(1000)
    KORp2.startcost.set(0)
    KORp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    KORp2.turb_eff_curves.set([pd.Series([75.00000], index=[3.96183], name=714),
                               pd.Series([75.00000], index=[3.81747], name=741)])

    #### MAINTANANCE FLAG
    start = pd.Timestamp(2025, 1, 1)
    end = pd.Timestamp(2025, 3, 21)
    #KORp2.maintenance_flag.set(pd.Series([0, 1, 0], index=[starttime, pd.Timestamp(2025, 3, 30), pd.Timestamp(2025, 7, 30)], name=0))
    #KORp2.maintenance_flag.set(pd.Series([1, 0], index=[starttime, pd.Timestamp(2025, 4, 3)], name=0))

    # Limit

    KOR.max_p_constr.set(pd.Series([KORg1.p_max.get()], [starttime]))
    KOR.max_p_constr_flag.set(pd.Series([1], [starttime]))

    return shop

########################################################################################################################
# OSCHENIK G1 & G2 & G3
########################################################################################################################
def add_PP_Oschenik(shop):

    OS = shop.model.plant.add_object('Oschenik')

    OS.outlet_line.set(1205)
    OS.main_loss.set([0])
    OS.penstock_loss.set([0])
    #OS.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    OS.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    OSg1 = shop.model.generator.add_object('OS_G1')
    OSg2 = shop.model.generator.add_object('OS_G2')
    OSg3 = shop.model.generator.add_object('OS_G3')

    OSg1.connect_to(OS)
    OSg2.connect_to(OS)
    OSg3.connect_to(OS)

    OSg1.penstock.set(1)
    OSg2.penstock.set(1)
    OSg3.penstock.set(1)

    # Oschenik: Generator 1

    OSg1.p_min.set(5)
    OSg1.p_max.set(36)
    OSg1.p_nom.set(36)
    OSg1.discharge.set(3)
    OSg1.startcost.set(0)

    g_eff, g_MW = get_Oschenik_generator(1)
    #1044, 1045, 1100, 1105, 1110
    F1, F2, F3, F4, F5, E1, E2, E3, E4, E5 = get_Oschenik_turbine1()

    OSg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    OSg1.turb_eff_curves.set([pd.Series(E1,index=F1,name=1044),
                              pd.Series(E2,index=F2,name=1045),
                              pd.Series(E3,index=F3,name=1100),
                              pd.Series(E4,index=F4,name=1105),
                              pd.Series(E5,index=F5,name=1110)])

    # Oschenik: Generator 2

    OSg2.p_min.set(5)
    OSg2.p_max.set(36)
    OSg2.p_nom.set(36)
    OSg2.discharge.set(3)
    OSg2.startcost.set(0)

    g_eff, g_MW = get_Oschenik_generator(2)
    flow, E1100, E1105, E1110 = get_Oschenik_turbine(2)

    OSg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    OSg2.turb_eff_curves.set([pd.Series(E1100,index=flow,name=1100),
                               pd.Series(E1105,index=flow,name=1105),
                               pd.Series(E1110,index=flow,name=1110)])

    # Oschenik: Generator 3

    OSg3.p_min.set(5)
    OSg3.p_max.set(42)
    OSg3.p_nom.set(42)
    OSg3.discharge.set(4.1)
    OSg3.startcost.set(0)

    g_eff, g_MW = get_Oschenik_generator(3)
    flow, E1100, E1105, E1110 = get_Oschenik_turbine(3)

    OSg3.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    OSg3.turb_eff_curves.set([pd.Series(E1100,index=flow,name=1100),
                               pd.Series(E1105,index=flow,name=1105),
                               pd.Series(E1110,index=flow,name=1110)])

    return shop


def add_PP_Oschenik_alt(shop):

    OS = shop.model.plant.add_object('Oschenik')

    OS.outlet_line.set(1205)
    OS.main_loss.set([0])
    OS.penstock_loss.set([0])
    #OS.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    OS.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    OSg1 = shop.model.generator.add_object('OS_G1')
    OSg2 = shop.model.generator.add_object('OS_G2')
    OSg3 = shop.model.generator.add_object('OS_G3')

    OSg1.connect_to(OS)
    OSg2.connect_to(OS)
    OSg3.connect_to(OS)

    OSg1.penstock.set(1)
    OSg2.penstock.set(1)
    OSg3.penstock.set(1)

    # Oschenik: Generator 1

    OSg1.p_min.set(5)
    OSg1.p_max.set(36)
    OSg1.p_nom.set(36)
    OSg1.discharge.set(3)
    OSg1.startcost.set(0)

    g_eff, g_MW = get_Oschenik_generator(1)
    #1044, 1045, 1100, 1105, 1110
    F1, F2, F3, F4, F5, E1, E2, E3, E4, E5 = get_Oschenik_turbine1()

    OSg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    OSg1.turb_eff_curves.set([pd.Series(E1,index=F1,name=1044),
                              pd.Series(E2,index=F2,name=1045),
                              pd.Series(E3,index=F3,name=1100),
                              pd.Series(E4,index=F4,name=1105),
                              pd.Series(E5,index=F5,name=1110)])

    # Oschenik: Generator 2

    OSg2.p_min.set(5)
    OSg2.p_max.set(36)
    OSg2.p_nom.set(36)
    OSg2.discharge.set(3)
    OSg2.startcost.set(0)

    g_eff, g_MW = get_Oschenik_generator(2)
    flow, E1100, E1105, E1110 = get_Oschenik_turbine(2)

    OSg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    OSg2.turb_eff_curves.set([pd.Series(E1100,index=flow,name=1100),
                               pd.Series(E1105,index=flow,name=1105),
                               pd.Series(E1110,index=flow,name=1110)])

    # Oschenik: Generator 3

    OSg3.p_min.set(5)
    OSg3.p_max.set(47)
    OSg3.p_nom.set(47)
    OSg3.discharge.set(4.1)
    OSg3.startcost.set(0)

    g_eff, g_MW = get_Oschenik_generator_alt(3)
    flow, E1100, E1105, E1110 = get_Oschenik_turbine(3)

    OSg3.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    OSg3.turb_eff_curves.set([pd.Series(E1100,index=flow,name=1100),
                               pd.Series(E1105,index=flow,name=1105),
                               pd.Series(E1110,index=flow,name=1110)])

    return shop
########################################################################################################################
# OSCHENIK P1
########################################################################################################################
def add_PP_Oschenik_P1(shop):

    OS_P1 = shop.model.plant.add_object('Oschenik_P1')
    OS_P1.outlet_line.set(1458)
    OS_P1.main_loss.set([0])
    OS_P1.penstock_loss.set([0])
    #OS_P1.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    OS_P1.consumption_fee.set(pd.Series([4.235,5.76],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    OSp1 = shop.model.pump.add_object('OS_P1')
    OSp1.connect_to(OS_P1)
    OSp1.penstock.set(1)
    OSp1.p_min.set(0)
    OSp1.p_max.set(1000)
    OSp1.p_nom.set(0)
    OSp1.startcost.set(0)
    OSp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    OSp1.turb_eff_curves.set([pd.Series([88.00], index=[3.950], name=787),
                              pd.Series([89.90], index=[3.330], name=890),
                              pd.Series([89.75], index=[3.000], name=935)])

    return shop

########################################################################################################################
# OSCHENIK P2 & P3
########################################################################################################################
def add_PP_Oschenik_P23(shop):

    OS_P23 = shop.model.plant.add_object('Oschenik_P23')

    OS_P23.main_loss.set([0])
    OS_P23.outlet_line.set(1675)
    OS_P23.penstock_loss.set([0])
    #OS_P23.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    OS_P23.consumption_fee.set(pd.Series([4.235,5.76],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    OSp2 = shop.model.pump.add_object('OS_P2')
    OSp2.connect_to(OS_P23)
    OSp2.penstock.set(1)
    OSp2.p_min.set(0)
    OSp2.p_max.set(1000)
    OSp2.p_nom.set(0)
    OSp2.startcost.set(0)
    OSp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    OSp2.turb_eff_curves.set([pd.Series([82.70], index=[5.830], name=550),
                              pd.Series([86.75], index=[5.168], name=633),
                              pd.Series([85.00], index=[4.360], name=716)])

    OSp3 = shop.model.pump.add_object('OS_P3')
    OSp3.connect_to(OS_P23)
    OSp3.penstock.set(1)
    OSp3.p_min.set(0)
    OSp3.p_max.set(1000)
    OSp3.p_nom.set(0)
    OSp3.startcost.set(0)
    OSp3.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    OSp3.turb_eff_curves.set([pd.Series([82.70], index=[4.138], name=550),
                              pd.Series([86.75], index=[3.632], name=633),
                              pd.Series([85.00], index=[3.025], name=716)])

    return shop


def add_PP_Oschenik_P23(shop):

    OS_P23 = shop.model.plant.add_object('Oschenik_P23')

    OS_P23.main_loss.set([0])
    OS_P23.outlet_line.set(1675)
    OS_P23.penstock_loss.set([0])
    #OS_P23.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    OS_P23.consumption_fee.set(pd.Series([4.235,5.76],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    OSp2 = shop.model.pump.add_object('OS_P2')
    OSp2.connect_to(OS_P23)
    OSp2.penstock.set(1)
    OSp2.p_min.set(0)
    OSp2.p_max.set(1000)
    OSp2.p_nom.set(0)
    OSp2.startcost.set(0)
    OSp2.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    OSp2.turb_eff_curves.set([pd.Series([82.70], index=[5.830], name=550),
                              pd.Series([86.75], index=[5.168], name=633),
                              pd.Series([85.00], index=[4.360], name=716)])

    OSp3 = shop.model.pump.add_object('OS_P3')
    OSp3.connect_to(OS_P23)
    OSp3.penstock.set(1)
    OSp3.p_min.set(0)
    OSp3.p_max.set(1000)
    OSp3.p_nom.set(0)
    OSp3.startcost.set(0)
    OSp3.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    OSp3.turb_eff_curves.set([pd.Series([82.70], index=[4.138], name=550),
                              pd.Series([86.75], index=[3.632], name=633),
                              pd.Series([85.00], index=[3.025], name=716)])

    return shop
########################################################################################################################
# WOELLA
########################################################################################################################
def add_PP_Woella(shop):

    WO = shop.model.plant.add_object('Woella')

    WO.outlet_line.set(1205)
    WO.main_loss.set([0])
    WO.penstock_loss.set([0])
    #WO.production_fee.set(pd.Series([2.01,11.5],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    WO.production_fee.set(pd.Series([2.01,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    WOg1 = shop.model.generator.add_object('WO_G1')

    WOg1.connect_to(WO)

    WOg1.penstock.set(1)

    # Woella: Generator 1

    WOg1.p_min.set(6)
    WOg1.p_max.set(17)
    WOg1.p_nom.set(17)
    WOg1.discharge.set(6)
    WOg1.startcost.set(0)

    g_eff, g_MW = get_Woella_generator()
    flow, E311 = get_Woella_turbine()

    WOg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    WOg1.turb_eff_curves.set([pd.Series(E311,index=flow,name=311)])

    return shop

########################################################################################################################
# WURTEN
########################################################################################################################
def add_PP_Wurten(shop):

    WU = shop.model.plant.add_object('Wurten')

    WU.outlet_line.set(1205)
    WU.main_loss.set([0])
    WU.penstock_loss.set([0,0])
    #WU.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    WU.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    WUg1 = shop.model.generator.add_object('WU_G1')
    WUg2 = shop.model.generator.add_object('WU_G2')

    WUg1.connect_to(WU)
    WUg2.connect_to(WU)

    WUg1.penstock.set(1)
    WUg2.penstock.set(2)

    # Generator 1

    WUg1.p_min.set(2)
    WUg1.p_max.set(32)
    WUg1.p_nom.set(32)
    WUg1.discharge.set(7)
    WUg1.startcost.set(0)

    g_eff, g_MW = get_Wurten_generator(1)
    flow, E469 = get_Wurten_turbine(1)

    WUg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    WUg1.turb_eff_curves.set([pd.Series(E469,index=flow,name=469)])

    # Generator 2

    WUg2.p_min.set(2)
    WUg2.p_max.set(35.6)
    WUg2.p_nom.set(35.6)
    WUg2.discharge.set(8.9)
    WUg2.startcost.set(0)

    g_eff, g_MW = get_Wurten_generator(2)
    flow, E469 = get_Wurten_turbine(2)

    WUg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    WUg2.turb_eff_curves.set([pd.Series(E469,index=flow,name=469)])

    return shop

########################################################################################################################
# WURTEN
########################################################################################################################
def add_PP_PSKW_Wurten(shop):

    PSKW_WU = shop.model.plant.add_object('PSKW_Wurten')

    PSKW_WU.outlet_line.set(1651)
    PSKW_WU.main_loss.set([0])
    PSKW_WU.penstock_loss.set([0,0])

    #PSKW_WU.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    PSKW_WUg1 = shop.model.generator.add_object('WU_G1')

    PSKW_WUg1.connect_to(PSKW_WU)

    PSKW_WUg1.penstock.set(1)


    # Generator 1

    PSKW_WUg1.p_min.set(45)
    PSKW_WUg1.p_max.set(235)
    PSKW_WUg1.p_nom.set(235)
    PSKW_WUg1.discharge.set(19)
    PSKW_WUg1.startcost.set(0)

    g_eff, g_MW = get_Wurten_generator(1)
    flow, E469 = get_Wurten_turbine(1)

    PSKW_WUg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    PSKW_WUg1.turb_eff_curves.set([pd.Series(E469,index=flow,name=469)])


    return shop

########################################################################################################################
# ZIRKNITZ
########################################################################################################################
def add_PP_Zirknitz(shop):

    # -----------------------------------------------------------------------------------------------------------------------
    # Zirknitz
    # -----------------------------------------------------------------------------------------------------------------------

    ZN = shop.model.plant.add_object('Zirknitz')

    ZN.outlet_line.set(1728)
    ZN.main_loss.set([0])
    ZN.penstock_loss.set([4, 3])
    #ZN.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    ZN.production_fee.set(pd.Series([1.44,3.7],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    ZNg1 = shop.model.generator.add_object('ZN_G1')
    ZNg2 = shop.model.generator.add_object('ZN_G2')

    ZNg1.connect_to(ZN)
    ZNg2.connect_to(ZN)

    ZNg1.penstock.set(1)
    ZNg2.penstock.set(2)

    # Generator 1

    ZNg1.p_min.set(2)
    ZNg1.p_max.set(16)
    ZNg1.p_nom.set(16)
    ZNg1.discharge.set(3.04)
    ZNg1.startcost.set(0)

    g_eff, g_MW = get_Zirknitz_generator()
    flow, E605, E660, E688 = get_Zirknitz_turbine()

    ZNg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    ZNg1.turb_eff_curves.set([pd.Series(E605,index=flow,name=605),
                               pd.Series(E660,index=flow,name=660),
                               pd.Series(E688,index=flow,name=688)])

    # Generator 2

    ZNg2.p_min.set(2)
    ZNg2.p_max.set(16)
    ZNg2.p_nom.set(16)
    ZNg2.discharge.set(3.04)
    ZNg2.startcost.set(0)

    ZNg2.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    ZNg2.turb_eff_curves.set([pd.Series(E605,index=flow,name=605),
                               pd.Series(E660,index=flow,name=660),
                               pd.Series(E688,index=flow,name=688)])

    return shop

########################################################################################################################
# PSKW Großsee - Stufe Brettsee
########################################################################################################################
def add_PP_Brettsee(shop):

    # -----------------------------------------------------------------------------------------------------------------------
    # Stufe Brettsee (25 MW hyd)
    # -----------------------------------------------------------------------------------------------------------------------

    BS = shop.model.plant.add_object('Brettsee')

    #BS.outlet_line.set(2170) #TODO 2120 müA.
    BS.outlet_line.set(2180) # Test Walter 2023-12-06
    BS.main_loss.set([0])
    BS.penstock_loss.set([0])
    #BS.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    BSg1 = shop.model.generator.add_object('BS_G1')
    BSg1.connect_to(BS)
    BSg1.penstock.set(1)

    # Generator 1
    BSg1.p_min.set(0)
    BSg1.p_max.set(25)
    BSg1.p_nom.set(25)
    BSg1.discharge.set(8)
    BSg1.startcost.set(0)

    g_eff, g_MW = get_Brettsee_generator()
    flow, E340, E345, E349 = get_Brettsee_turbine()

    BSg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    BSg1.turb_eff_curves.set([pd.Series(E340,index=flow,name=340),
                               pd.Series(E345,index=flow,name=345),
                               pd.Series(E349,index=flow,name=349)])

    BSp1 = shop.model.pump.add_object('BS_p1')
    BSp1.connect_to(BS)
    BSp1.penstock.set(1)
    BSp1.p_min.set(0)
    BSp1.p_max.set(1000)
    BSp1.p_nom.set(25)
    BSp1.startcost.set(0)
    BSp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    BSp1.turb_eff_curves.set([pd.Series([90], index=[7], name=340),pd.Series([90], index=[6.9], name=349)])

    return shop

def add_PP_Kegele(shop):

    KE = shop.model.plant.add_object('Kegele')

    KE.main_loss.set([0])
    KE.outlet_line.set(2180.0)
    KE.penstock_loss.set([0])
    #KE.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    KEg1 = shop.model.generator.add_object('KE_G1')
    KEg1.connect_to(KE)
    KEg1.penstock.set(1)

    # Generator 1
    KEg1.p_min.set(0)
    KEg1.p_max.set(75)
    KEg1.p_nom.set(75)
    KEg1.discharge.set(38)
    KEg1.startcost.set(0)

    g_eff, g_MW = get_Kegelesee_generator()
    flow, E215, E220, E225 = get_Kegelesee_turbine()

    KEg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    KEg1.turb_eff_curves.set([pd.Series(E215,index=flow,name=215),
                               pd.Series(E220,index=flow,name=220),
                               pd.Series(E225,index=flow,name=225)])

    # Neue Pumpe 75 MW
    #KEp1 = shop.model.pump.add_object('KE_p1')
    #KEp1.connect_to(KE)
    #KEp1.penstock.set(1)
    #KEp1.p_min.set(0)
    #KEp1.p_max.set(1000)
    #KEp1.p_nom.set(75)
    #KEp1.startcost.set(0)
    #KEp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    #KEp1.turb_eff_curves.set([pd.Series([90], index=[28], name=150),
                              #pd.Series([90], index=[31], name=260)])

    # 19.9 - 20
    KGp1 = shop.model.pump.add_object("KG_p1")
    KGp1.connect_to(KE)
    KGp1.penstock.set(1)
    KGp1.p_min.set(0)
    KGp1.p_max.set(1000)
    KGp1.p_nom.set(75)
    KGp1.startcost.set(0)
    KGp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 50]))
    #KGp1.turb_eff_curves.set([pd.Series([90], index=[28], name=150),
    #                          pd.Series([90], index=[31], name=260)])
    KGp1.turb_eff_curves.set([pd.Series([91], index=[30], name=215),
                              pd.Series([90], index=[30.5], name=220),
                              pd.Series([89], index=[31], name=225)])

    return shop

def add_PP_Kegele_pump(shop):

    KG = shop.model.plant.add_object('Kegele')

    #KG.outlet_line.set(2161.5)
    KG.outlet_line.set(2120.0)
    KG.main_loss.set([0])
    KG.penstock_loss.set([0])
    #KG.production_fee.set(pd.Series([0],index=[pd.Timestamp(2022,1,1)]))
    #KG.consumption_fee.set(pd.Series([4.805,13.215],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    #KGg1 = shop.model.generator.add_object('KG_G1')
    #KGg1.connect_to(KG)
    #KGg1.penstock.set(1)


    # Kegele: Generator 1

    #KGg1.p_min.set(3.9)
    #KGg1.p_max.set(4)
    #KGg1.p_nom.set(4)
    #KGg1.discharge.set(1.8)
    #KGg1.max_q_constr.set(1000) ###
    #KGg1.startcost.set(0)

    #g_eff, g_MW = get_Haselstein_generator()
    #flow, E260 = get_Haselstein_turbine()

    #KGg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    #KGg1.turb_eff_curves.set([pd.Series(E260,index=flow,name=260)])

    # Kegele: Pump 1

    KGp1 = shop.model.pump.add_object("KG_P1")
    KGp1.connect_to(KG)
    KGp1.penstock.set(1)
    KGp1.p_nom.set(50)
    KGp1.p_min.set(0)
    KGp1.p_max.set(1000)
    KGp1.startcost.set(0)
    KGp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    #KGp1.turb_eff_curves.set([pd.Series([90], index=[19.9], name=225),pd.Series([90], index=[20], name=238)])
    KGp1.turb_eff_curves.set([pd.Series([90], index=[19.9], name=150),pd.Series([90], index=[20], name=260)])

    return shop

########################################################################################################################
# PSKW Bernegger
########################################################################################################################
def add_PP_Bernegger(shop):

    BN = shop.model.plant.add_object('Bernegger')

    BN.outlet_line.set(10)
    BN.main_loss.set([0])
    BN.penstock_loss.set([0,0])
    #FS.production_fee.set(pd.Series([1.44,9.29],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))
    #FS.consumption_fee.set(pd.Series([4.235,11.005],index=[pd.Timestamp(2022,1,1),pd.Timestamp(2023,1,1)]))

    BNg1 = shop.model.generator.add_object('BN_G1')

    BNg1.connect_to(BN)

    BNg1.penstock.set(1)

    # PSKW Bernegger: Generator 1

    BNg1.p_min.set(70)
    BNg1.p_max.set(315)
    BNg1.p_nom.set(315)
    BNg1.discharge.set(55.6)
    BNg1.startcost.set(0)

    g_eff, g_MW = get_Bernegger_generator()
    flow, E600, E630, E660 = get_Bernegger_turbine()

    BNg1.gen_eff_curve.set(pd.Series(g_eff, index=g_MW))
    BNg1.turb_eff_curves.set([pd.Series(E600,index=flow,name=600),
                               pd.Series(E630,index=flow,name=630),
                               pd.Series(E660,index=flow,name=660)])

    # PSKW Bernegger: Pump 1
    # TODO >> Pump eff Bernegger

    BNp1 = shop.model.pump.add_object("BN_P1")
    BNp1.connect_to(BN)
    BNp1.penstock.set(1)
    BNp1.p_nom.set(65)
    BNp1.p_min.set(0)
    BNp1.p_max.set(1000)
    BNp1.startcost.set(0)
    BNp1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 100]))
    BNp1.turb_eff_curves.set([pd.Series([88.85], index=[47.4], name=600),
                              pd.Series([91.32], index=[46.4], name=630),
                              pd.Series([93.61], index=[45.4], name=660)])

    return shop

########################################################################################################################
# PSKW SHOP Pump example
########################################################################################################################
def add_PP_Plant1(shop):

    plant1 = shop.model.plant.add_object('Plant1')

    plant1.outlet_line.set(40)
    plant1.main_loss.set([0.0002])
    plant1.penstock_loss.set([0.0001])


    p1g1 = shop.model.generator.add_object('P1G1')
    p1g1.connect_to(plant1)
    p1g1.penstock.set(1)

    # PSKW SHOP Plant 1: Generator 1

    p1g1.p_min.set(25)
    p1g1.p_nom.set(100)
    p1g1.p_max.set(100)
    p1g1.startcost.set(500)
    # p1g1.discharge.set(55.6)

    p1g1.gen_eff_curve.set(pd.Series([95, 98], index=[0, 100]))
    p1g1.turb_eff_curves.set(
        [pd.Series([80, 95, 90], index=[25, 90, 100], name=90),
         pd.Series([82, 98, 92], index=[25, 90, 100], name=100)])

    # PSKW SHOP: Pump 1

    p1p1 = shop.model.pump.add_object("P1P1")
    p1p1.connect_to(shop.model.plant.Plant1)
    p1p1.penstock.set(1)
    p1p1.p_nom.set(40)
    p1p1.p_min.set(40)
    p1p1.p_max.set(40)
    p1p1.startcost.set(500)
    p1p1.gen_eff_curve.set(pd.Series([100, 100], index=[0, 50]))
    p1p1.turb_eff_curves.set([pd.Series([87], index=[80], name=40),
                              pd.Series([86], index=[70], name=50),
                              pd.Series([85], index=[60], name=60)])

    return shop
