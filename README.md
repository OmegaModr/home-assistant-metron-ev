[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# Metron EV charger component for Home Assistant

Custom component to support Metron EV chargers.

A few useful sensors are exported along with services to set charging current, time delay and toggle solar charging

## Installation

There are 2 different methods of installing the custom component

### HACS installation

1. Add this repository from HACS->Integrations->Custom repositories.
2. Enter https://github.com/OmegaModr/home-assistant-metron-ev and select integration as the type
3. Install the latest version
4. Restart Home Assistant.
5. Install the component from Settings->Integrations. You may have to clear the browser cache to make the Metron integration appear in the list.

### Git installation

1. Make sure you have git installed on your machine.
2. Navigate to you home assistant configuration folder.
3. Create a `custom_components` folder of it does not exist, navigate down into it after creation.
4. Execute the following command: `git clone https://github.com/OmegaModr/home-assistant-metron-ev.git ev_metron_websockets`

## Frontend cards

To use the services and sensors on lovelace dashboards use the Charger-card at https://github.com/tmjo/charger-card

As a basic starting point use the configuration below to get you started.
Change the entity names to your specific ones.

```yaml
type: custom:charger-card
entity: sensor.ovca_station_name
brand: template
show_leds: true
details:
  name:
    entity_id: sensor.ovca_station_name
    attribute: name
  status:
    entity_id: sensor.ovca_station_status
  substatus:
    entity_id: sensor.ovca_solar_charging_enable
  currentlimits:
    - 0
    - 6
    - 8
    - 12
    - 14
    - 16
  collapsiblebuttons:
    group1:
      text: Charge rate
      icon: mdi:speedometer
    group2:
      text: Additional info
      icon: mdi:information
    group3:
      visible: false
  info_left:
    - entity_id: sensor.ovca_station_active
      text: Online
      icon: mdi:connection
    - entity_id: sensor.ovca_telemetry_signal_present
      text: Signal Strength
      icon: mdi:signal
  group1:
    - entity_id: sensor.ovca_dinamic_charging_current_limit
      text: Current Limit
      unit_show: true
      service: metron.set_dynamic_limit
      service_data:
        current: '#SERVICEVAL#'
    - entity_id: sensor.ovca_timer_delay
      text: Charge Delay
      unit_show: false
      icon: mdi:clock
      service: metron.set_charger_delay
      dropdownitems:
        - 60
        - 180
        - 240
      service_data:
        current: '#SERVICEVAL#'
    - entity_id: sensor.ovca_solar_charging_state
      text: Solar Charging
      unit_show: false
      icon: mdi:solar-power
      service: metron.toggle_solar
      type: service
      service_data:
        current: '#SERVICEVAL#'
  group2:
    - entity_id: sensor.ovca_l1_current
      text: L1 Current
      unit_show: true
    - entity_id: sensor.ovca_l2_current
      text: L2 Current
      unit_show: true
    - entity_id: sensor.ovca_l3_current
      text: L3 Current
      unit_show: true
    - entity_id: sensor.ovca_previous_charge_energy
      text: Previous charge
      unit_show: true
    - entity_id: sensor.ovca_solar_surplus_power
      text: Solar Surplus
      icon: mdi:solar-power
      unit_show: true
  stats:
    default:
      - entity_id: sensor.ovca_total_charging_power
        text: Charge Power
        unit_show: true
      - entity_id: sensor.ovca_this_charge_energy
        text: This Charge
        unit_show: true
      - entity_id: sensor.ovca_charging_time
        text: Charge Time

```

## Configuration

Configuration is done through in Configuration > Integrations where you first configure the name and ip address of the station.

## Use
The basic use of the integrations from the UI should be self-explanatory. The integration defines a number of services that can be used from automations and scripts to control the charger and the charging process. The available services can be found in Home Assistant at Developer tools->Services.

The easiest way to set up services and their parameters is to use the automation editor or the developer tools. However, you can also write the code in plain yaml. The UI will use device_id as target for the services. This is a random string generated internally by HA and is not very user friendly. 

Three examples of the services you can call:
```yaml
service: ev_metron_websockets.toggle_solar
data:
  device_id: c06269a64fc9f8f8dc150142f3bde4ce
```
```yaml
service: ev_metron_websockets.set_dynamic_limit
data:
  current: 12
  device_id: c06269a64fc9f8f8dc150142f3bde4ce
```
```yaml
service: ev_metron_websockets.set_charger_delay
data:
  time: 60
  device_id: c06269a64fc9f8f8dc150142f3bde4ce
```
