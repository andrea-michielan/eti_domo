# Thermoregulation
If you want to change the operational mode of a thermo zone you can use the `thermo_mode` method. <br>
For example if you want to set to *auto* mode the zone with `act_id = 15` you can write:
```python
hub.thermo_mode(act_id=15, mode=2, temp=19.5)
```
Where `temp` is a floating point value describing the target temperature of the zone in degrees Celsius and `mode` is one of the following integer:
* 0: off
* 1: manual mode
* 2: auto mode
* 3: jolly mode

Example of a Json response from the server:
```Json
{
    'cseq': 2, 
    'cmd_name': 'generic_reply', 
    'sl_data_ack_reason': 0
}
```
# Change season
If you want to change the season in order to switch the thermo implant from heating mode to cooling mode or switching off the entire system you can use the `change_season` method.<br>
For example if you want to switch to summer you can write:
```python
hub.change_season(Domo.seasons['summer'])
```
As you can see you have to pass the function a string representing the season that you want to switch to. You can use the `Domo.seasons` dictionary that has the available seasons:
* Domo.seasons['summer']
* Domo.seasons['winter']
* Domo.seasons['off']

Example of a Json response from the server:
```Json
{
    'cseq': 2, 
    'cmd_name': 'generic_reply', 
    'sl_data_ack_reason': 0
}
```