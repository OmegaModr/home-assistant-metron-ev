"""Contains the MetronEVHub class."""

import websockets
import asyncio

from collections.abc import Callable
#from datetime import datetime

from homeassistant.core import HomeAssistant

#from . import const
from . import metron


class MetronEVHub:
    """Hub for connecting to the Metron EV websocket."""

    def __init__(
        self, hass: HomeAssistant, name: str, host: str, port: int
    ) -> None:
        """Initialise the class."""
        self._host = host
        self._hass = hass
        self._name = name
        self._port = port
        self._uri = f"ws://{host}:{port}/ws"
        self._id = host.lower()
        self._callbacks = set()
        self._is_active = False
        self._metron_ev_status = 0
        self._L1_current_station = 0
        self._L2_current_station = 0
        self._L3_current_station = 0
        self._L1_current_building = 0
        self._L2_current_building = 0
        self._L3_current_building = 0
        self._L1_current_solar = 0
        self._House_energy = 0
        self._button_set_charging_current = 0
        self._main_fuse_rating = 0
        self._dinamic_charging_current_limit = 0
        self._solar_charging_enable = 0
        self._solar_charging_enable_esp = 0
        self._total_charging_power = 0
        self._this_charge_energy = 0
        self._hour_counter = 0
        self._minute_counter = 0
        self._previous_charge_energy = 0
        self._lifetime_energy = 0
        self._solar_energy = 0
        self._solar_SURPLUS_power = 0
        self._local_network_IP_string = 0
        self._ESP32_timer_delay = 0
        self._HC12_Signal_Present = 0
        self._TCA0_cmp2 = 0

    async def test_endpoint(self) -> bool:
        """Test if we can subscribe to the websocket."""
        success = False
        async with websockets.connect(self._uri) as websocket:
            success = not websocket.closed

        return success

    async def update(self) -> None:
        """Background task to loop websocket updates."""
        while True:
            try:
                async with websockets.connect(self._uri) as websocket:
                    self._is_active = not websocket.closed
                    async for message in websocket:
                        latest_message = metron.get_parsed_variables(message)
                        self._metron_ev_status = latest_message.get("Status")
                        self._L1_current_station = latest_message.get("L1_current_station")
                        self._L2_current_station = latest_message.get("L2_current_station")
                        self._L3_current_station = latest_message.get("L3_current_station")
                        self._L1_current_building = latest_message.get("L1_current_building")
                        self._L2_current_building = latest_message.get("L2_current_building")
                        self._L3_current_building = latest_message.get("L3_current_building")
                        self._L1_current_solar = latest_message.get("L1_current_solar")
                        self._button_set_charging_current = latest_message.get("Button_set_charging_current")
                        self._main_fuse_rating = latest_message.get("Main_fuse_rating")
                        self._dinamic_charging_current_limit = latest_message.get("Dinamic_charging_current_limit")
                        self._solar_charging_enable_esp = latest_message.get("Solar_charging_enable_ESP32_reply")
                        self._solar_charging_enable = latest_message.get("Solar_charging_enable")
                        self._total_charging_power = latest_message.get("Total_charging_power")
                        self._this_charge_energy = latest_message.get("This_charge_energy")
                        self._hour_counter = latest_message.get("hour_counter")
                        self._minute_counter = latest_message.get("minute_counter")
                        self._previous_charge_energy = latest_message.get("Previous_charge_energy")
                        self._lifetime_energy = latest_message.get("Lifetime_energy")
                        self._solar_energy = latest_message.get("Solar_energy")
                        self._House_energy = latest_message.get("House_energy")
                        self._solar_SURPLUS_power = latest_message.get("Solar_SURPLUS_power")
                        self._local_network_IP_string = latest_message.get("Local_network_IP_string")
                        self._ESP32_timer_delay = latest_message.get("ESP32_timer_delay")
                        self._HC12_Signal_Present = latest_message.get("HC12_Signal_Present")
                        self._TCA0_cmp2 = latest_message.get("TCA0_cmp2")
                        await self.publish_updates()
            except websockets.WebSocketException as e:
                print(f"WebSocket exception: {e}. Reconnecting in 5 seconds...")
                self._is_active = False
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
                self._is_active = False
                await asyncio.sleep(5)
            else:
                self._is_active = not websocket.closed
                await self.publish_updates()

    @property
    def metron_ev_name(self) -> str:
        """Return status of station."""
        return self._name

    @property
    def TCA0_cmp2(self) -> str:
        """Return status of station."""
        return self._TCA0_cmp2

    @property
    def metron_ev_status(self) -> str:
        """Return status of station."""
        return self._metron_ev_status

    @property
    def L1_current_station(self) -> str:
        """Return the value of L1_current_station."""
        return self._L1_current_station

    @property
    def L2_current_station(self) -> str:
        """Return the value of L2_current_station."""
        return self._L2_current_station

    @property
    def L3_current_station(self) -> str:
        """Return the value of L3_current_station."""
        return self._L3_current_station

    @property
    def L1_current_building(self) -> str:
        """Return the value of L1_current_building."""
        return self._L1_current_building

    @property
    def L2_current_building(self) -> str:
        """Return the value of L2_current_building."""
        return self._L2_current_building

    @property
    def L3_current_building(self) -> str:
        """Return the value of L3_current_building."""
        return self._L3_current_building

    @property
    def L1_current_solar(self) -> str:
        """Return the value of L1_current_solar."""
        return self._L1_current_solar

    @property
    def button_set_charging_current(self) -> str:
        """Return the value of button_set_charging_current."""
        return self._button_set_charging_current

    @property
    def main_fuse_rating(self) -> str:
        """Return the value of main_fuse_rating."""
        return self._main_fuse_rating

    @property
    def dinamic_charging_current_limit(self) -> str:
        """Return the value of dinamic_charging_current_limit."""
        return self._dinamic_charging_current_limit

    @property
    def solar_charging_enable(self) -> str:
        """Return the value of solar_charging_enable."""
        return self._solar_charging_enable

    @property
    def solar_charging_enable_esp(self) -> str:
        """Return the value of solar_charging_enable."""
        return self._solar_charging_enable_esp

    @property
    def total_charging_power(self) -> str:
        """Return the value of total_charging_power."""
        return self._total_charging_power

    @property
    def this_charge_energy(self) -> str:
        """Return the value of this_charge_energy."""
        return self._this_charge_energy

    @property
    def hour_counter(self) -> str:
        """Return the value of hour_counter."""
        return self._hour_counter

    @property
    def minute_counter(self) -> str:
        """Return the value of minute_counter."""
        return self._minute_counter

    @property
    def previous_charge_energy(self) -> str:
        """Return the value of previous_charge_energy."""
        return self._previous_charge_energy

    @property
    def lifetime_energy(self) -> str:
        """Return the value of lifetime_energy."""
        return self._lifetime_energy

    @property
    def solar_energy(self) -> str:
        """Return the value of solar_energy."""
        return self._solar_energy

    @property
    def House_energy(self) -> str:
        """Return the value of solar_energy."""
        return self._House_energy

    @property
    def solar_SURPLUS_power(self) -> str:
        """Return the value of solar_SURPLUS_power."""
        return self._solar_SURPLUS_power

    @property
    def local_network_IP_string(self) -> str:
        """Return the value of local_network_IP_string."""
        return self._local_network_IP_string

    @property
    def ESP32_timer_delay(self) -> str:
        """Return the value of ESP32_timer_delay."""
        return self._ESP32_timer_delay

    @property
    def HC12_Signal_Present(self) -> str:
        """Return the value of HC12_Signal_Present."""
        return self._HC12_Signal_Present

    async def perform_action(self, message) -> None:
        """Send a constructed message to the websockets endpoint."""
        #message.update(const.ACTION_BASE_MESSAGE)
        #message["timestamp"] = datetime.now().timestamp()
        async with websockets.connect(self._uri) as websocket:
            await websocket.send(message)

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback called when the state changes."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Call all callbacks on update."""
        for callback in self._callbacks:
            callback()

    @property
    def available(self) -> bool:
        """Available if the websockets connection has value and is not closed."""
        return self._is_active
