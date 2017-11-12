# Database query and record funtion for universal energy management system
import time
from data_management.database_format import db_optimal_power_flow, db_economic_dispatch, db_unit_commitment


class database_operation():
    # Database operation in universal energy management system
    def unit_commitment_default_data(*args):
        Target_time = args[0]
        default_result = db_optimal_power_flow \
            (TIME_STAMP=Target_time,
             AC_PD=0,
             AC_QD=0,
             UAC_PD=0,
             UAC_QD=0,
             DC_PD=0,
             UDC_PD=0,
             PV_PG=0,
             WP_PG=0,
             PRICE=0,
             DG_STATUS=0,
             DG_PG=0,
             DG_QG=0,
             UG_STATUS=0,
             UG_PG=0,
             UG_QG=0,
             BIC_PG=0,
             BIC_QG=0,
             BAT_PG=0,
             BAT_SOC=0,
             PMG=0,
             V_DC=0,
             PV_CURT=0,
             WP_CURT=0,
             AC_SHED=0,
             UAC_SHED=0,
             DC_SHED=0,
             UDC_SHED=0, )
        return default_result

    def optimal_power_flow_default_data(*args):
        Target_time = args[0]
        default_result = db_optimal_power_flow \
            (TIME_STAMP=Target_time,
             AC_PD=0,
             AC_QD=0,
             UAC_PD=0,
             UAC_QD=0,
             DC_PD=0,
             UDC_PD=0,
             PV_PG=0,
             WP_PG=0,
             DG_STATUS=0,
             DG_PG=0,
             DG_QG=0,
             UG_STATUS=0,
             UG_PG=0,
             UG_QG=0,
             BIC_PG=0,
             BIC_QG=0,
             BAT_PG=0,
             BAT_SOC=0,
             PMG=0,
             V_DC=0,
             PV_CURT=0,
             WP_CURT=0,
             AC_SHED=0,
             UAC_SHED=0,
             DC_SHED=0,
             UDC_SHED=0, )
        return default_result

    def economic_dispatch_default_data(*args):
        Target_time = args[0]
        default_result = db_optimal_power_flow \
            (TIME_STAMP=Target_time,
             AC_PD=0,
             AC_QD=0,
             UAC_PD=0,
             UAC_QD=0,
             DC_PD=0,
             UDC_PD=0,
             PV_PG=0,
             WP_PG=0,
             PRICE=0,
             DG_STATUS=0,
             DG_PG=0,
             DG_QG=0,
             UG_STATUS=0,
             UG_PG=0,
             UG_QG=0,
             BIC_PG=0,
             BIC_QG=0,
             BAT_PG=0,
             BAT_SOC=0,
             PMG=0,
             V_DC=0,
             PV_CURT=0,
             WP_CURT=0,
             AC_SHED=0,
             UAC_SHED=0,
             DC_SHED=0,
             UDC_SHED=0, )
        return default_result

    def database_query(input, session):
        # The input information check for the databases
        print(time.time())

    def database_record(*args):
        # The result storage operation for obtained result
        session = args[0]
        model = args[1]
        Target_time = args[2]
        ## control model of UC, ED or OPF
        function = args[3]

        database_target = {"UC": db_unit_commitment,
                           "ED": db_economic_dispatch,
                           "OPF": db_optimal_power_flow}

        if session.query(database_target[function].PV_PG).filter(
                        database_target[function].TIME_STAMP == Target_time).count() == 0:
            if function == "OPF":
                blank_row = database_operation.optimal_power_flow_default_data(Target_time)
                session.add(blank_row)
                session.commit()

        if function == "OPF":
            row = session.query(database_target[function]).filter(
                database_target[function].TIME_STAMP == Target_time).first()
            row.AC_PD = model["Load_ac"]["PD"]
            row.AC_QD = model["Load_ac"]["QD"]
            row.UAC_PD = model["Load_uac"]["PD"]
            row.UAC_QD = model["Load_uac"]["QD"]
            row.DC_PD = model["Load_dc"]["PD"]
            row.UDC_PD = model["Load_udc"]["PD"]
            row.PV_PG = model["PV"]["PG"]
            row.WP_PG = model["WP"]["PG"]
            row.DG_STATUS = model["DG"]["GEN_STATUS"]
            row.DG_PG = model["DG"]["COMMAND_SET_POINT_PG"]
            row.DG_QG = model["DG"]["COMMAND_SET_POINT_QG"]
            row.UG_STATUS = model["UG"]["GEN_STATUS"]
            row.UG_PG = model["UG"]["COMMAND_SET_POINT_PG"]
            row.UG_QG = model["UG"]["COMMAND_SET_POINT_QG"]
            row.BIC_PG = model["BIC"]["COMMAND_AC2DC"] - model["BIC"]["COMMAND_DC2AC"]
            row.BIC_QG = model["BIC"]["COMMAND_Q"]
            row.BAT_PG = model["ESS"]["COMMAND_PG"]
            row.BAT_SOC = model["ESS"]["SOC"]
            row.PMG = model["PMG"]
            row.V_DC = model["V_DC"]
            row.PV_CURT = model["PV"]["COMMAND_CURT"]
            row.WP_CURT = model["WP"]["COMMAND_CURT"]
            row.AC_SHED = model["Load_ac"]["COMMAND_SHED"]
            row.UAC_SHED = model["Load_uac"]["COMMAND_SHED"]
            row.DC_SHED = model["Load_dc"]["COMMAND_SHED"]
            row.UDC_SHED = model["Load_udc"]["COMMAND_SHED"]
            session.commit()
        else:
            from configuration.configuration_time_line import default_look_ahead_time_step
            from configuration.configuration_time_line import default_time
            if function == "ED":
                T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
                delta_T = default_time["Time_step_ed"]
            else:
                T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]
                delta_T = default_time["Time_step_uc"]

            for i in range(T):
                if session.query(database_target[function].PV_PG).filter(
                                database_target[function].TIME_STAMP == Target_time).count() == 0:
                    blank_row = database_operation.economic_dispatch_default_data(Target_time + i * delta_T)

                    blank_row.AC_PD = model["Load_ac"]["PD"][i]
                    blank_row.UAC_PD = model["Load_uac"]["PD"][i]
                    blank_row.DC_PD = model["Load_dc"]["PD"][i]
                    blank_row.UDC_PD = model["Load_udc"]["PD"][i]
                    blank_row.PV_PG = model["PV"]["PG"][i]
                    blank_row.WP_PG = model["WP"]["PG"][i]
                    blank_row.DG_STATUS = model["DG"]["GEN_STATUS"][i]
                    blank_row.DG_PG = model["DG"]["COMMAND_SET_POINT_PG"][i]
                    blank_row.UG_STATUS = model["UG"]["GEN_STATUS"][i]
                    blank_row.UG_PG = model["UG"]["COMMAND_SET_POINT_PG"][i]
                    blank_row.BIC_PG = model["BIC"]["COMMAND_AC2DC"][i] - model["BIC"]["COMMAND_DC2AC"][i]
                    blank_row.BAT_PG = model["ESS"]["COMMAND_PG"][i]
                    blank_row.BAT_SOC = model["ESS"]["SOC"][i]
                    blank_row.PMG = model["PMG"][i]
                    blank_row.PV_CURT = model["PV"]["COMMAND_CURT"][i]
                    blank_row.WP_CURT = model["WP"]["COMMAND_CURT"][i]
                    blank_row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][i]
                    blank_row.UAC_SHED = model["Load_uac"]["COMMAND_SHED"][i]
                    blank_row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][i]
                    blank_row.UDC_SHED = model["Load_udc"]["COMMAND_SHED"][i]

                    session.add(blank_row)
                    session.commit()
                else:
                    row = session.query(database_target[function]).filter(
                        database_target[function].TIME_STAMP == Target_time).first()

                    row.AC_PD = model["Load_ac"]["PD"][i]
                    row.UAC_PD = model["Load_uac"]["PD"][i]
                    row.DC_PD = model["Load_dc"]["PD"][i]
                    row.UDC_PD = model["Load_udc"]["PD"][i]
                    row.PV_PG = model["PV"]["PG"][i]
                    row.WP_PG = model["WP"]["PG"][i]
                    row.DG_STATUS = model["DG"]["GEN_STATUS"][i]
                    row.DG_PG = model["DG"]["COMMAND_SET_POINT_PG"][i]
                    row.UG_STATUS = model["UG"]["GEN_STATUS"][i]
                    row.UG_PG = model["UG"]["COMMAND_SET_POINT_PG"][i]
                    row.BIC_PG = model["BIC"]["COMMAND_AC2DC"][i] - model["BIC"]["COMMAND_DC2AC"][i]
                    row.BAT_PG = model["ESS"]["COMMAND_PG"][i]
                    row.BAT_SOC = model["ESS"]["SOC"][i]
                    row.PMG = model["PMG"][i]
                    row.PV_CURT = model["PV"]["COMMAND_CURT"][i]
                    row.WP_CURT = model["WP"]["COMMAND_CURT"][i]
                    row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][i]
                    row.UAC_SHED = model["Load_uac"]["COMMAND_SHED"][i]
                    row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][i]
                    row.UDC_SHED = model["Load_udc"]["COMMAND_SHED"][i]
                    session.commit()