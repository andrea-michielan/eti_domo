# List request
This method allows you to request a specific list of items (lights, switches, sensors, ...). The default usage is:
```python
hub.list_request(command_name)
```
where `command_name` is a string of a specific command. <br>
A dictionary of available commands can be accessed by:
```python
Domo.available_commands[key]
```
where key can be any of the following:
# "update": ask the server if there are any changes to any item
```python
print("\nRequesting an update...")
print(hub.list_request(Domo.available_commands['update']))
```
Example of a Json returned by the server:
```yaml
{
    'cmd_name': 'status_update_resp', 
    'cseq': 1, 
    'sl_data_ack_reason': 0, 
    'result': [
        {
            'cmd_name': 'thermo_zone_info_ind', 
            'act_id': 88, 
            'name': 'Salotto', 
            'floor_ind': 19, 
            'room_ind': 287, 
            'temp_dec': 142, 
            'status': 0, 
            'mode': 0, 
            'hygro': 46,
            'set_point': 200, 
            'season': 'winter', 
            'antifreeze': 30, 
            't1': 190, 
            't2': 200, 
            't3': 210, 
            'thermo_algo': {
                'type': 'D', 
                'diff_t_dec': 2, 
                'pi_set_in_use': 1
            }, 
            'reason': 1
        }
    ]
}
```
# "relays": request a list of relays/switches
```python
try:
    relays = hub.list_request(Domo.available_commands['relays'])['array']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    for index, relay in enumerate(relays, start=1):
        print(f"[Relay {index}] {relay['name']}, id: {relay['act_id']}, status: {relay['status']}")
```
Example of a Json returned by the server:
```yaml
{
    'cmd_name': 'relays_list_resp', 
    'cseq': 2, 
    'array': [
        {
            'name': 'Basculante', 
            'act_id': 93, 
            'status': 0, 
            'icon_id': 23
        },
        {
            'name': 'ElfoFresh Silent Mode', 
            'act_id': 95, 
            'status': 0, 
            'icon_id': 0
        }
    ], 
    'sl_data_ack_reason': 0
}
```
# "cameras": request a list of tvcc
```python
try:
    cameras = hub.list_request(Domo.available_commands['tvcc'])['array']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    for index, camera in enumerate(cameras, start=1):
        print(f"[Camera {index}] {camera['name']}, uri: {camera['uri']}")
```
# "timers": request a list of timers
```python
try:
    timers = hub.list_request(Domo.available_commands['timers'])['array']
except:
    print("The server cannot soddisfy this request")
else:
    for timer in timers:
        print(f"[Timer name]: {timer['name']}, id: {timer['id']}, enabled: {timer['enabled']}, days: {timer['days']}")
        for time in timer['timetable']:
            print(f"\t[START]: {time['start']['hour']}:{time['start']['min']}:{time['start']['sec']}")
            print(f"\t[END]: {time['stop']['hour']}:{time['stop']['min']}:{time['stop']['sec']}")
            print(f"\t\tEnabled: {time['active']}")
```
Example of a Json returned by the server:
```yaml
{
    'cseq': 3, 
    'cmd_name': 'timers_list_resp', 
    'array': [
        {
            'name': 'Temporizzatore', 
            'id': 117, 
            'enabled': 0, 
            'days': 1,
            'bars': 2, 
            'timetable': [
                {
                    'start': {
                        'hour': 2, 
                        'min': 0, 
                        'sec': 0
                    }, 
                    'stop': {
                        'hour': 8, 
                        'min': 0, 
                        'sec': 0
                    }, 
                    'active': 0, 
                    'index': 0
                }
            ]
        }
    ], 
    'sl_data_ack_reason': 0
}
```
# "thermoregulation": request a list of thermoregulation devices
```python
try:
    floors = hub.list_request(Domo.available_commands['thermoregulation'])['array']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    print(floors)
    for floor in floors:
        print(f"\t[Zone name]: {floor['name']}, status: {floor['status']}, temp: {str(floor['temp'])[:-1]}.{str(floor['temp'])[-1::]}° C, id: {floor['act_id']}")
```
This is an example of a Json returned by the server:
```yaml
{
    'cseq': 1, 
    'cmd_name': 'thermo_list_resp', 
    'array': [
        {
            'act_id': 69, 
            'name': 'Cucina', 
            'floor_ind': 17, 
            'room_ind': 21,
            'status': 0, 
            'temp': 150, 
            'mode': 0, 
            'set_point': 200, 
            'thermo_algo': {
                'type': 'D', 
                'diff_t_dec': 2, 
                'pi_set_in_use': 1
            }, 
            'season': 'winter', 
            'leaf': True
        }, 
        {
            'act_id': 70, 
            'name': 'Soggiorno', 
            'floor_ind': 17,
            'room_ind': 24, 
            'status': 0, 
            'temp': 148, 
            'mode': 0, 
            'set_point': 200, 
            'thermo_algo': {
                'type': 'D', 
                'diff_t_dec': 2, 
                'pi_set_in_use': 1
            }, 
            'season': 'winter', 
            'leaf': True
        }
    ], 
    'humidity': {
        'name': 'Igrometro', 
        'act_id': 89, 
        'value': 46, 
        'unit': '%'
    }, 
    'sl_data_ack_reason': 0
}
```
And this is the formatting done in the previous snippet of python code:
```
[Zone name]: Cucina, status: 0, temp: 15.0° C, id: 69
[Zone name]: Soggiorno, status: 0, temp: 14.8° C, id: 70
[Zone name]: Bagno, status: 0, temp: 16.2° C, id: 71
[Zone name]: Lavanderia, status: 0, temp: 14.1° C, id: 90
[Zone name]: Garage, status: 0, temp: 16.6° C, id: 91
[Zone name]: Camera Matrimoniale, status: 0, temp: 13.4° C, id: 82
[Zone name]: Camera Sud, status: 0, temp: 13.7° C, id: 83
[Zone name]: Camera Centrale, status: 0, temp: 13.7° C, id: 84
[Zone name]: Bagni, status: 0, temp: 13.5° C, id: 85
[Zone name]: Cucina di sopra, status: 0, temp: 13.7° C, id: 86
[Zone name]: Camera esterna, status: 0, temp: 15.0° C, id: 87
[Zone name]: Salotto, status: 0, temp: 14.2° C, id: 88
```
# "analogin": request a list of analog input devices (such as hygrometers)
```python
try:
    analogs = hub.list_request(Domo.available_commands['analogin'])['array']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    for item in analogs:
        print(f"[Item name]: {item['name']}, id: {item['act_id']}, value: {item['value']}{item['unit']}")
```
Example of a Json returned by the server:
```yaml
{
    'cseq': 3, 
    'cmd_name': 'analogin_list_resp', 
    'array': [
        {
            'name': 'Igrometro', 
            'act_id': 89, 
            'value': 47, 
            'unit': '%'
        }
    ],
    'sl_data_ack_reason': 0
}
```
And this is the formatting done in the previous snippet of python code:
```
[Item name]: Hygrometer, id: 89, value: 47%
```
# "digitalin": request a list of digital input devices (such as buttons)
```python
print("\nRequesting the list of digital inputs...")
print(session.list_request(Domo.available_commands['digitalin']))
```
Example of a Json returned by the server:
```yaml
{
    'cmd_name': 'digitalin_list_resp', 
    'cseq': 5, 
    'array': [
        {
            'name': 'Pulsante P05', 
            'act_id': 10, 
            'type': 1, 
            'addr': 1, 
            'ack': 1, 
            'radio_node_id': '00000000', 
            'rf_radio_link_quality': 0, 
            'utc_time': 0
        }, 
        {
            'name': 'Pulsante P06', 
            'act_id': 11,
            'type': 1, 
            'addr': 2, 
            'ack': 1, 
            'radio_node_id': '00000000', 
            'rf_radio_link_quality': 0, 
            'utc_time': 0
        }
    ], 
    'sl_data_ack_reason': 0
}
```
# "lights": request a list of lights
```python
try:
    floors = hub.list_request(Domo.available_commands['lights'])['array']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    for floor in floors:
        print(f"[Floor name]: {floor['name']}, status: {floor['status']}")
        for room in floor['array']:
            print(f"\t[Room name]: {room['name']}, status: {room['status']}")
            for item in room['array']:
                print(f"\t\t[Light name]: {item['name']}, status: {item['status']}, id: {item['act_id']}")
```
Example of a Json returned by the server:
```yaml
{
    'cseq': 6, 
    'cmd_name': 'light_list_resp', 
    'array': [
        {
            'name': 'Piano Terra', 
            'floor_ind': 17, 
            'status': 0, 
            'array': [
                {
                    'name': 'Soggiorno', 
                    'room_ind': 24, 
                    'status': 0, 
                    'array': [
                        {
                            'act_id': 1, 
                            'name': 'Soggiorno', 
                            'floor_ind': 17, 
                            'room_ind': 24, 
                            'status': 0, 
                            'type': 'STEP_STEP', 
                            'leaf': True
                        }
                    ]
                }, 
                {
                    'name': 'Bagno', 
                    'room_ind': 27, 
                    'status': 0, 
                    'array': [
                        {
                            'act_id': 3, 
                            'name': 'Bagno', 
                            'floor_ind': 17, 
                            'room_ind': 27, 
                            'status': 0, 
                            'type': 'STEP_STEP', 
                            'leaf': True
                        }, 
                        {
                            'act_id': 4, 
                            'name': 'Specchio Bagno', 
                            'floor_ind': 17, 
                            'room_ind': 27, 
                            'status': 0, 
                            'type': 'STEP_STEP', 
                            'leaf': True
                        }, 
                    ]
                }
            ]
        }, 
        {
            'name': 'Primo Piano', 
            'floor_ind': 19, 
            'status': 0, 
            'array': [
                {
                    'name': 'Camera Matrimoniale', 
                    'room_ind': 278, 
                    'status': 0, 
                    'array': [
                        {
                            'act_id': 27, 
                            'name': 'Matrimoniale', 
                            'floor_ind': 19, 
                            'room_ind': 278, 
                            'status': 0, 
                            'type': 'STEP_STEP', 
                            'leaf': True
                        }, 
                        {
                            'act_id': 28, 
                            'name': 'Matrimoniale sinistra', 
                            'floor_ind': 19, 
                            'room_ind': 278, 
                            'status': 0, 
                            'type': 'STEP_STEP', 
                            'leaf': True
                        }
                    ]
                }
            ]
        }
    ], 
    'sl_data_ack_reason': 0
}
```
And this is the formatting done in the previous snippet of python code:
```
[Floor name]: Piano Terra, status: 0
        [Room name]: Soggiorno, status: 0
                [Light name]: Soggiorno, status: 0, id: 1
        [Room name]: Bagno, status: 0
                [Light name]: Bagno, status: 0, id: 3
                [Light name]: Specchio Bagno, status: 0, id: 4
[Floor name]: Primo Piano, status: 0
        [Room name]: Camera Matrimoniale, status: 0
                [Light name]: Matrimoniale, status: 0, id: 27
                [Light name]: Matrimoniale sinistra, status: 0, id: 28
```
# "features": request a list of supported features by the server
```python
try:
    features = hub.list_request(Domo.available_commands['features'])['list']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    for index, feature in enumerate(features, start=1):
        print(f"[Feature {index}] {feature}")
```
Example of a Json returned by the server:
```yaml
{
    'cmd_name': 'feature_list_resp', 
    'cseq': 8, 
    'keycode': 'XXXXXXXXXX', 
    'swver': '2.5.0', 
    'type': '0', 
    'board': '3', 
    'serial': 'XXXXXXXXX', 
    'list': [
        'lights', 
        'thermoregulation', 
        'timers', 
        'maps', 
        'relays', 
        'analogin', 
        'digitalin'
    ], 
    'recovery_status': 0, 
    'sl_data_ack_reason': 0
}
```
And this is the formatting done in the previous snippet of python code:
```
[Feature 1] lights
[Feature 2] thermoregulation
[Feature 3] timers
[Feature 4] maps
[Feature 5] relays
[Feature 6] analogin
[Feature 7] digitalin
```
# "users": request a list of user available
```python
try:
    users = hub.list_request(Domo.available_commands['users'])['sl_users_list']
except RequestError:
    print("The server cannot soddisfy this request")
else:
    for index, user in enumerate(users, start=1):
        print(f"[User {index}] {user['name']}")
```
Example of a Json returned by the server:
```yaml
{
    'sl_cmd': 'sl_users_list_resp', 
    'sl_data_ack_reason': 0, 
    'sl_client_id': '22edca7f', 
    'sl_users_list': [
        {'name': 'admin'}, 
        {'name': 'test'}, 
        {'name': 'user'}, 
        {'name': 'user2'}
    ]
}
```
And this is the formatting done in the previous snippet of python code:
```
[User 1] admin
[User 2] test
[User 3] user
[User 4] user2
```
# "maps": request the map of the entire domo server
```python
print("\nRequesting the list of map elements...")
print(hub.list_request(Domo.available_commands['maps']))
```
Example of a Json returned by the server:
```yaml
{
    'cseq': 11, 
    'cmd_name': 'map_descr_resp', 
    'map': [
        {
            'background': 'maps/maps_pianta piano terra.png', 
            'page_label': 'Piano Terra', 
            'page_scale': 1024, 
            'page_id': 0, 
            'array': [
                {
                    'x': 208, 
                    'y': 405, 
                    'width': 89, 
                    'height': 120, 
                    'label': 'Bagno', 
                    'aspect': 'maps_pages_Generico', 
                    'icon_id': 0, 
                    'permission': 1048575, 
                    'read_only': 0, 
                    'address': 0, 
                    'type': 3, 
                    'page': 1
                }, 
                {
                    'x': 234, 
                    'y': 714, 
                    'width': 74, 
                    'height': 118, 
                    'label': 'Soggiorno', 
                    'aspect': 'maps_pages_Generico', 
                    'icon_id': 0, 
                    'permission': 1048575, 
                    'read_only': 0, 
                    'address': 0, 
                    'type': 3, 
                    'page': 12
                }
            ]
        }, 
        {
            'background': 'maps/maps_pianta piano terra_bagno.png',
            'page_label': 'Bagno', 
            'page_scale': 1024, 
            'page_id': 1, 
            'array': [
                {
                    'x': 685, 
                    'y': 450, 
                    'width': 123, 
                    'height': 194, 
                    'label': 'Specchio Bagno', 
                    'aspect': 'maps_lights_Generico', 
                    'icon_id': 0, 
                    'permission': 1048575, 
                    'read_only': 0, 
                    'address': 14, 
                    'type': 0, 
                    'act_id': 4, 
                    'status': 0
                }
            ]
        }
    ], 
    'sl_data_ack_reason': 0
}
```
If you enter an invalid key in any of these methods, a `CommandNotFound` exception will be raised. <br>
If the server does not support the requested command then a `RequestError` will be raised.