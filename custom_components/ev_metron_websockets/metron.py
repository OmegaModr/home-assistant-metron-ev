"""Contains the Metron string parser class."""

import json
import logging
import re

_LOGGER = logging.getLogger(__name__)


def parse_string(input_string):
    """Break up the legacy alphabet-delimited string."""
    values = re.findall(r'[a-zA-Z](.+?)(?=[a-zA-Z]|$)', input_string)
    parsed_values = []
    for value in values:
        if value.isdigit():
            parsed_values.append(int(value))
        else:
            parsed_values.append(value)
    return parsed_values


def assign_variables(values):
    """Assign values to named variables (legacy string format)."""
    var_names = [
        'Status', 'L1_current_station', 'L2_current_station', 'L3_current_station',
        'L1_current_building', 'L2_current_building', 'L3_current_building',
        'L1_current_solar', 'Button_set_charging_current', 'Main_fuse_rating',
        'Charging_cable_max_current', 'Vreg1_set_charging_current', 'Vreg2_set_charging_current',
        'Station_max_charging_current', 'Dynamic_charging_current_limit', 'Solar_charging_enable',
        'RFID_enable', 'PWMRegister_ESP32_reply_Amps', 'Solar_charging_enable_ESP32_reply',
        'TCA0_cmp2', 'Dynamic_Enable', 'Total_charging_power', 'This_charge_energy',
        'hour_counter', 'minute_counter', 'Previous_charge_energy', 'Since_last_reset_energy',
        'Lifetime_energy', 'PWMRegister_ESP32_slider_Amps', 'WiFi_to_network_enable',
        'Total_house_power', 'House_energy', 'Solar_phases', 'House_phases', 'Car_phases',
        'Total_solar_power', 'Solar_energy', 'Solar_SURPLUS_power', 'WiFi_to_network_state',
        'Local_network_IP_string', 'ESP32_timer_delay', 'HC12_enable', 'number_of_stations',
        'HC12_Channel', 'HC12_Signal_Present',
    ]
    parsed_variables = dict(zip(var_names, values))
    n = len(values)
    expected = len(var_names)
    if n != expected:
        _LOGGER.debug(
            "Legacy message has %d fields, expected %d — firmware version mismatch?",
            n, expected,
        )
    return parsed_variables


def assign_variables_json(obj):
    """Assign values to named variables from a parsed JSON object."""
    def _n(key):
        """Get a numeric field, defaulting to 0 for missing keys (older firmware)."""
        val = obj.get(key, 0)
        return 0 if val is None else val

    def _s(key):
        """Get a string field, defaulting to empty string for missing or null keys."""
        val = obj.get(key, "")
        return val if val is not None else ""

    return {
        "Status": _n('a'),
        "L1_current_station": _n('b'),
        "L2_current_station": _n('c'),
        "L3_current_station": _n('d'),
        "L1_current_building": _n('e'),
        "L2_current_building": _n('f'),
        "L3_current_building": _n('g'),
        "L1_current_solar": _n('h'),
        "Button_set_charging_current": _n('i'),
        "Main_fuse_rating": _n('j'),
        "Charging_cable_max_current": _n('k'),
        "Vreg1_set_charging_current": _n('l'),
        "Vreg2_set_charging_current": _n('m'),
        "Station_max_charging_current": _n('n'),
        "Dynamic_charging_current_limit": _n('o'),
        "Solar_charging_enable": _n('p'),
        "RFID_enable": _n('q'),
        "Pwmregister_ESP32_reply_Amps": _n('r'),
        "Solar_charging_enable_ESP32_reply": _n('s'),
        "TCA0_cmp2": _n('t'),
        "Dynamic_Enable": _n('u'),
        "Total_charging_power": _n('A'),
        "This_charge_energy": _n('B'),
        "hour_counter": _n('C'),
        "minute_counter": _n('D'),
        "Previous_charge_energy": _n('E'),
        "Since_last_reset_energy": _n('F'),
        "Lifetime_energy": _n('G'),
        "Pwmregister_ESP32_slider_Amps": _n('H'),
        "WiFi_to_network_enable": _n('I'),
        "Total_house_power": _n('J'),
        "House_energy": _n('K'),
        "Solar_phases": _n('L'),
        "House_phases": _n('M'),
        "Car_phases": _n('N'),
        "Total_solar_power": _n('O'),
        "Solar_energy": _n('P'),
        "Solar_SURPLUS_power": _n('Q'),
        "WiFi_to_network_state": _n('R'),
        "Local_network_IP_string": _s('S'),
        "ESP32_timer_delay": _n('T'),
        "HC12_enable": _n('U'),
        "Stevilo_postaj": _n('V'),
        "HC12_Channel": _n('W'),
        "HC12_Signal_Present": _n('X'),
        "ID_station": _s('Y'),
        "OCPP_enable": _n('Z'),
        "OCPP_state": _n('AA'),
        "OCPP_local_network_IP_string": _s('AB'),
        "OCPP_charging_current_limit": _n('AC'),
        "last_scanned_card": _s('AD'),
        "rfid_commnad_response": _s('AE'),
        "rfid_stored_cards_num": _n('AF'),
        "Guest_mode": _n('AG'),
        "Change_Parameters_mode": _n('AH'),
        "Front_button": _n('AI'),
        "Metron_Charge_Control_Version": _s('AJ'),
        "OCPP_module_code_version": _s('AK'),
        "temprature_sens_read": _n('AL'),
        "RFID_energy": _n('AM'),
        "MCU_booting_code": _n('AN'),
        "temperature_sens_read_OCPP": _n('AO'),
        "MCU_booting_code_OCPP": _n('AP'),
        "ISO_module_state": _n('AR'),
        "ISO_VEHICLE_EVCCID": _s('AS'),
        "ISO_VEHICLE_SOC": _n('AT'),
        "ISO_VEHICLE_energy": _n('AU'),
        "ISO_VEHICLE_EVCCID_status": _n('AV'),
        "ISO_stored_VEHICLE_num": _n('AW'),
        "ISO_module_code_version": _s('AX'),
        "temperature_sens_read_ISO": _n('AY'),
        "MCU_booting_code_ISO": _n('AZ'),
        "ISO_EVCCID_AutoCharge_prefix_OCPP": _s('BA'),
        "ISO_AutoCharge_enable": _n('BB'),
        "kWh_limit_sider": _n('BC'),
        "P_grid_limit": _n('BD'),
        "Grid_system": _n('BE'),
    }


def get_parsed_variables(ws_string):
    """Parse a websocket message and return (variable dict, format string).

    Tries JSON first (new firmware), falls back to legacy alphabet-delimited
    format, and logs a warning if neither matches.
    """
    try:
        obj = json.loads(ws_string)
    except ValueError:
        pass
    else:
        missing = [k for k in ('a', 'b', 'A', 'G') if k not in obj]
        if missing:
            _LOGGER.debug(
                "JSON message missing core keys %s — older firmware?", missing,
            )
        return assign_variables_json(obj), "json"

    parsed_values = parse_string(ws_string)
    if parsed_values:
        _LOGGER.debug("Received legacy (non-JSON) message format")
        return assign_variables(parsed_values), "legacy"

    _LOGGER.warning("Unrecognised message format: %.120s", ws_string)
    return {}, "unknown"
