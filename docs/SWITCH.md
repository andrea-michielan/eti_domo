# Turn on/off a light or a switch
In order to turn on/off a light or a switch you can use the `switch` method.<br>For example if you want to turn on the light with `act_id = 69`:
```python
hub.switch(69, status=True, is_light=True)
```
Where status is `True` if you want to turn on the light, `False` otherwise.<br>
If instead you want to activate a relay/switch you can set `is_light=False`:
```python
hub.switch(69, status=True, is_light=False)
```
Note: `status` and `is_light` default to `True`, so if you want to turn on the light with `act_id = 69` you can simply write:
```python
hub.switch(69)
```
The server in either cases will respond with a Json acknowledging the request:
```Json
{
    'cseq': 12, 
    'cmd_name': 'generic_reply', 
    'sl_data_ack_reason': 0
}
```