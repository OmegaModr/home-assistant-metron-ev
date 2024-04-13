"""Contains the Metron string parser class."""

import re
import json

def parse_string(input_string):
    """Breakup the string."""
    values = re.findall(r'[a-zA-Z](.+?)(?=[a-zA-Z]|$)', input_string)
    parsed_values = []
    for value in values:
        if value.isdigit():
            parsed_values.append(int(value))
        else:
            parsed_values.append(value)
    return parsed_values

def assign_variables(values):
    """Assign values to named variables."""
    var_names = ['Status', 'L1_current_station', 'L2_current_station', 'L3_current_station', 'L1_current_building', 'L2_current_building', 'L3_current_building', 'L1_current_solar', 'Button_set_charging_current', 'Main_fuse_rating',
                 'Charging_cable_max_current', 'Vreg1_set_charging_current', 'Vreg2_set_charging_current', 'Station_max_charging_current', 'Dinamic_charging_current_limit', 'Solar_charging_enable', 'RFID_enable', 'PWMRegister_ESP32_reply_Amps', 'Solar_charging_enable_ESP32_reply', 'TCA0_cmp2',
                 'Dinamic_Enable', 'Total_charging_power', 'This_charge_energy', 'hour_counter', 'minute_counter', 'Previous_charge_energy', 'Since_last_reset_energy', 'Lifetime_energy', 'PWMRegister_ESP32_slider_Amps', 'WiFi_to_network_enable',
                 'Total_house_power', 'House_energy', 'Solar_phases', 'House_phases', 'Car_phases', 'Total_solar_power', 'Solar_energy', 'Solar_SURPLUS_power', 'WiFi_to_network_state', 'Local_network_IP_string',
                 'ESP32_timer_delay', 'HC12_enable', 'number_of_stations', 'HC12_Channel', 'HC12_Signal_Present']

    parsed_variables = dict(zip(var_names, values))
    return parsed_variables

def assign_variables_json(values):
    """Assign values to named variables from json."""
    json_object = json.loads(values)
    value_of_key_s = json_object['s']

    parsed_variables = {
        "Status": json_object['a'],
        "L1_current_station": json_object['b'],
        "L2_current_station": json_object['c'],
        "L3_current_station": json_object['d'],
        "L1_current_building": json_object['e'],
        "L2_current_building": json_object['f'],
        "L3_current_building": json_object['g'],
        "L1_current_solar": json_object['h'],
        "Button_set_charging_current": json_object['i'],
        "Main_fuse_rating": json_object['j'],
        "Charging_cable_max_current": json_object['k'],
        "Vreg1_set_charging_current": json_object['l'],
        "Vreg2_set_charging_current": json_object['m'],
        "Station_max_charging_current": json_object['n'],
        "Dinamic_charging_current_limit": json_object['o'],
        "Solar_charging_enable": json_object['p'],
        "RFID_enable": json_object['q'],
        "Pwmregister_ESP32_reply_Amps": json_object['r'],
        "Solar_charging_enable_ESP32_reply": json_object['s'],
        "TCA0_cmp2": json_object['t'],
        "Dinamic_Enable": json_object['u'],
        "Total_charging_power": json_object['A'],
        "This_charge_energy": json_object['B'],
        "hour_counter": json_object['C'],
        "minute_counter": json_object['D'],
        "Previous_charge_energy": json_object['E'],
        "Since_last_reset_energy": json_object['F'],
        "Lifetime_energy": json_object['G'],
        "Pwmregister_ESP32_slider_Amps": json_object['H'],
        "WiFi_to_network_enable": json_object['I'],
        "Total_house_power": json_object['J'],
        "House_energy": json_object['K'],
        "Solar_phases": json_object['L'],
        "House_phases": json_object['M'],
        "Car_phases": json_object['N'],
        "Total_solar_power": json_object['O'],
        "Solar_energy": json_object['P'],
        "Solar_SURPLUS_power": json_object['Q'],
        "WiFi_to_network_state": json_object['R'],
        "Local_network_IP_string": json_object['S'],
        "ESP32_timer_delay": json_object['T'],
        "HC12_enable": json_object['U'],
        "Stevilo_postaj": json_object['V'],
        "HC12_Channel": json_object['W'],
        "HC12_Signal_Present": json_object['X'],
        "ID_station": json_object['Y'],
        "OCPP_enable": json_object['Z'],
        "OCPP_state": json_object['AA'],
        "OCPP_local_network_IP_string": json_object['AB'],
        "OCPP_charging_current_limit": json_object['AC'],
        "last_scanned_card": json_object['AD'],
        "rfid_commnad_response": json_object['AE'],
        "rfid_stored_cards_num": json_object['AF'],
        "Guest_mode": json_object['AG'],
        "Change_Parameters_mode": json_object['AH'],
        "Front_button": json_object['AI'],
        "Metron_Charge_Control_Version": json_object['AJ'],
        "OCPP_module_code_version": json_object['AK'],
        "temprature_sens_read": json_object['AL'],
        "RFID_energy": json_object['AM'],
        "MCU_booting_code": json_object['AN'],
        "temperature_sens_read_OCPP": json_object['AO'],
        "MCU_booting_code_OCPP": json_object['AP'],
        "ISO_module_state": json_object['AR'],
        "ISO_VEHICLE_EVCCID": json_object['AS'],
        "ISO_VEHICLE_SOC": json_object['AT'],
        "ISO_VEHICLE_energy": json_object['AU'],
        "ISO_VEHICLE_EVCCID_status": json_object['AV'],
        "ISO_stored_VEHICLE_num": json_object['AW'],
        "ISO_module_code_version": json_object['AX'],
        "temperature_sens_read_ISO": json_object['AY'],
        "MCU_booting_code_ISO": json_object['AZ'],
        "ISO_EVCCID_AutoCharge_prefix_OCPP": json_object['BA'],
        "ISO_AutoCharge_enable": json_object['BB'],
        "kWh_limit_sider": json_object['BC'],
        "P_grid_limit": json_object['BD'],
        "Grid_system": json_object['BE']
    }

    return parsed_variables

def is_json(s):
    try:
        json_object = json.loads(s)
    except ValueError:
        return False
    return True

def get_parsed_variables(ws_string):
    """Combine the above into a dict and return for processing."""
    if is_json(ws_string):
      parsed_variables = assign_variables_json(ws_string)
    else:
      parsed_values = parse_string(ws_string)
      parsed_variables = assign_variables(parsed_values)
    return parsed_variables
