"""Contains the Metron string parser class."""

import re

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

def get_parsed_variables(sample_string):
    """Combine the above into a dict and return for processing."""
    parsed_values = parse_string(sample_string)
    parsed_variables = assign_variables(parsed_values)
    return parsed_variables
