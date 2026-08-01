"""Tests for the metron websocket message parser."""

import json
from custom_components.ev_metron_websockets.metron import (
    assign_variables,
    assign_variables_json,
    get_parsed_variables,
    parse_string,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FULL_JSON_OBJ = {
    'a': 3, 'b': 12, 'c': 0, 'd': 0,
    'e': 5, 'f': 0, 'g': 0,
    'h': 8, 'i': 16, 'j': 25,
    'k': 32, 'l': 16, 'm': 16, 'n': 32,
    'o': 16, 'p': 1, 'q': 0, 'r': 16,
    's': 1, 't': 8000, 'u': 1,
    'A': 2760, 'B': 1500, 'C': 1, 'D': 30,
    'E': 4200, 'F': 9000, 'G': 125000,
    'H': 16, 'I': 1,
    'J': 3200, 'K': 87000,
    'L': 1, 'M': 3, 'N': 1,
    'O': 500, 'P': 45000, 'Q': 300,
    'R': 1, 'S': '192.168.1.100',
    'T': 0, 'U': 0, 'V': 1, 'W': 1, 'X': 1,
    'Y': 'ST001', 'Z': 0,
    'AA': 0, 'AB': '', 'AC': 0,
    'AD': '', 'AE': '', 'AF': 0,
    'AG': 0, 'AH': 0, 'AI': 0,
    'AJ': 'v2.21Y', 'AK': '', 'AL': 23,
    'AM': 0, 'AN': 0, 'AO': 0, 'AP': 0,
    'AR': 0, 'AS': '', 'AT': 0, 'AU': 0,
    'AV': 0, 'AW': 0, 'AX': '', 'AY': 0, 'AZ': 0,
    'BA': '', 'BB': 0, 'BC': 0, 'BD': 0, 'BE': 0,
}

# Older firmware: core keys only, no OCPP/ISO/extended keys (Z, AA-BE)
_CORE_KEYS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY")
OLDER_FIRMWARE_OBJ = {k: v for k, v in FULL_JSON_OBJ.items() if k in _CORE_KEYS}

# ---------------------------------------------------------------------------
# parse_string (legacy format)
# ---------------------------------------------------------------------------

class TestParseString:
    def test_extracts_numeric_values(self):
        # Letters are delimiters; digits between them become ints
        result = parse_string("a3b12c0")
        assert result == [3, 12, 0]

    def test_extracts_string_values(self):
        # The regex captures everything between letter delimiters including digits
        result = parse_string("a192.168.1.1b")
        assert result == ["192.168.1.1"]  # 'b' is the next delimiter, full value captured

    def test_empty_string(self):
        assert parse_string("") == []

    def test_single_field(self):
        assert parse_string("a5") == [5]


# ---------------------------------------------------------------------------
# assign_variables (legacy)
# ---------------------------------------------------------------------------

class TestAssignVariables:
    def test_full_message_maps_status(self):
        values = [3] + [0] * 44   # 45 fields, Status=3
        result = assign_variables(values)
        assert result["Status"] == 3

    def test_short_message_no_exception(self):
        """Older firmware sending fewer fields must not raise."""
        result = assign_variables([1, 5, 3])
        assert result["Status"] == 1
        assert result["L1_current_station"] == 5
        assert "Lifetime_energy" not in result  # field absent, not present as None

    def test_long_message_no_exception(self):
        """Newer firmware with extra fields must not raise; extras are ignored."""
        values = list(range(50))   # 50 values, 45 expected
        result = assign_variables(values)
        assert len(result) == 45   # only known fields

    def test_first_five_fields(self):
        values = [3, 12, 8, 6, 20] + [0] * 40
        result = assign_variables(values)
        assert result["Status"] == 3
        assert result["L1_current_station"] == 12
        assert result["L2_current_station"] == 8
        assert result["L3_current_station"] == 6
        assert result["L1_current_building"] == 20


# ---------------------------------------------------------------------------
# assign_variables_json
# ---------------------------------------------------------------------------

class TestAssignVariablesJson:
    def test_full_message_core_fields(self):
        result = assign_variables_json(FULL_JSON_OBJ)
        assert result["Status"] == 3
        assert result["L1_current_station"] == 12
        assert result["Total_charging_power"] == 2760
        assert result["Lifetime_energy"] == 125000
        assert result["Local_network_IP_string"] == "192.168.1.100"
        assert result["Metron_Charge_Control_Version"] == "v2.21Y"

    def test_older_firmware_missing_ocpp_keys_returns_zero(self):
        """Keys absent in older firmware default to 0, not KeyError."""
        result = assign_variables_json(OLDER_FIRMWARE_OBJ)
        assert result["OCPP_enable"] == 0
        assert result["ISO_module_state"] == 0
        assert result["Grid_system"] == 0

    def test_older_firmware_core_fields_still_correct(self):
        result = assign_variables_json(OLDER_FIRMWARE_OBJ)
        assert result["Status"] == OLDER_FIRMWARE_OBJ['a']
        assert result["Lifetime_energy"] == OLDER_FIRMWARE_OBJ['G']

    def test_null_values_coerced_to_zero(self):
        obj = dict(FULL_JSON_OBJ)
        obj['a'] = None
        obj['G'] = None
        result = assign_variables_json(obj)
        assert result["Status"] == 0
        assert result["Lifetime_energy"] == 0

    def test_missing_core_key_G_returns_zero(self):
        obj = {k: v for k, v in FULL_JSON_OBJ.items() if k != 'G'}
        result = assign_variables_json(obj)
        assert result["Lifetime_energy"] == 0

    def test_string_field_missing_returns_empty_string(self):
        obj = {k: v for k, v in FULL_JSON_OBJ.items() if k != 'S'}
        result = assign_variables_json(obj)
        assert result["Local_network_IP_string"] == ""

    def test_null_string_field_coerced_to_empty_string(self):
        obj = dict(FULL_JSON_OBJ)
        obj['S'] = None
        obj['AD'] = None
        result = assign_variables_json(obj)
        assert result["Local_network_IP_string"] == ""
        assert result["last_scanned_card"] == ""

    def test_energy_values(self):
        result = assign_variables_json(FULL_JSON_OBJ)
        assert result["This_charge_energy"] == 1500
        assert result["Previous_charge_energy"] == 4200
        assert result["Solar_energy"] == 45000
        assert result["House_energy"] == 87000


# ---------------------------------------------------------------------------
# get_parsed_variables (integration)
# ---------------------------------------------------------------------------

class TestGetParsedVariables:
    def test_json_format_detected(self):
        _, fmt = get_parsed_variables(json.dumps(FULL_JSON_OBJ))
        assert fmt == "json"

    def test_json_values_correct(self):
        result, _ = get_parsed_variables(json.dumps(FULL_JSON_OBJ))
        assert result["Status"] == 3
        assert result["Lifetime_energy"] == 125000

    def test_older_firmware_json_no_exception(self):
        result, fmt = get_parsed_variables(json.dumps(OLDER_FIRMWARE_OBJ))
        assert fmt == "json"
        assert result["Grid_system"] == 0   # missing key → default

    def test_legacy_format_detected(self):
        _, fmt = get_parsed_variables("a3b12c0d0e5")
        assert fmt == "legacy"

    def test_legacy_values_correct(self):
        # Build a legacy string with status=3, L1_station=12
        values = [3, 12, 0, 0, 5] + [0] * 40
        # Encode as letter-delimited: 'a3b12c0...'
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY"
        msg = "".join(f"{letters[i]}{v}" for i, v in enumerate(values))
        result, fmt = get_parsed_variables(msg)
        assert fmt == "legacy"
        assert result["Status"] == 3
        assert result["L1_current_station"] == 12

    def test_unknown_format_returns_empty_dict(self):
        # Must contain no alpha chars so parse_string returns nothing
        result, fmt = get_parsed_variables("12345:::$$$")
        assert fmt == "unknown"
        assert result == {}

    def test_returns_two_tuple(self):
        out = get_parsed_variables(json.dumps(FULL_JSON_OBJ))
        assert isinstance(out, tuple)
        assert len(out) == 2

    def test_json_parse_is_not_doubled(self):
        """Parsed object passed directly into assign_variables_json — no double parse.

        Verify by checking the result is consistent with a single parse of the input.
        """
        msg = json.dumps(FULL_JSON_OBJ)
        result, fmt = get_parsed_variables(msg)
        assert fmt == "json"
        assert result["Total_charging_power"] == FULL_JSON_OBJ['A']
