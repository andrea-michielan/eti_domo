import requests
import sys

# Header for every http request made to the server
header = {
    "Content-Type": "application/x-www-form-urlencoded", 
    "Connection": "Keep-Alive"
}

class Domo:

    def __init__(self, host="http://192.168.1.251/domo/"):
        self.host = host
        self.cseq = 1
        self.id = ""

    # Function that makes the login and return if the user is authenticated
    def login(self, username, password):

        # Create the login request
        login_parameters = 'command={"sl_cmd":"sl_registration_req","sl_login":"' + str(username) + '","sl_pwd":"' + str(password) + '"}'

        # Send the post request with the login parameters
        response = requests.post(self.host, params=login_parameters, headers=header)

        # Set the client id for the session
        self.id = response.json()['sl_client_id']

        # Return true if the user is authenticated
        return not self.id == ""


    # Function that request an update and return the json of the result
    def update_request(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"status_update_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of the relays
    def relays_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"relays_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of the tvcc
    def tvcc_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"tvcc_cameras_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of timers
    def timers_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"timers_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of thermos
    def thermos_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"nested_thermo_list_req","cseq":' + str(self.cseq) + ',"extended_infos":2,"topologic_scope":"plant","value":0},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of analog inputs (higrometers)
    def analogin_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"analogin_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of digital inputs
    def digitalin_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"digitalin_list_req","cseq":' + str(self.cseq) + ',"filter":1023},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of terminals group (?)
    def terminals_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"terminals_group_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a json list of the lights
    def lights_list(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"nested_light_list_req","cseq":' + str(self.cseq) + ',"topologic_scope":"plant","value":0},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()['array']

    # Get the list of users, it seems like cseq is not sent, and even the server won't return it
    def users_list(self):

        # Create the requests' parameters
        param = 'command={"sl_client_id":"' + self.id + '","sl_cmd":"sl_users_list_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        #self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get all the elements of the map
    def get_map(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"cmd_name":"map_descr_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Get a list of all the features available
    def get_features(self):

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"feature_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()

    # Turn on or off the light
    def light_switch(self, act_id, on=True):

        status = "1" if on else "0"

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"act_id":' + str(act_id) + ',"client":"' + self.id + '","cmd_name":"light_switch_req","cseq":' + str(self.cseq) + ',"wanted_status":' + status + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Return the json of the response
        return response.json()


if __name__ == "__main__":
    session = Domo()
    if not session.login("utente2", "utente2"):
        print("Wrong username/password!")
        sys.exit(-1)
    print(f"You are now logged in! ID: {session.id}")
    #print("\nRequesting an update...")
    #print(session.update_request())
    print("\nRequesting the list of relays...")
    print(session.relays_list())
    print("\nRequesting the list of users...")
    print(session.users_list())
    print("\nRequesting the list of features...")
    print(session.get_features())
    #print("\nRequesting the list of map elements...")
    #print(session.get_map())
    print("\nRequesting the list of lights...")
    floors = session.lights_list()
    for floor in floors:
        print(f"[Nome Piano]: {floor['name']}, stato: {floor['status']}")
        for room in floor['array']:
            print(f"\t[Nome Stanza]: {room['name']}, stato: {room['status']}")
            for item in room['array']:
                print(f"\t\t[Nome Oggetto]: {item['name']}, stato: {item['status']}, id: {item['act_id']}")

    #print("\nAccensione luce con id=33...")
    #print(session.light_switch(33))

    #print("\nRequesting an update...")
    #print(session.update_request())

    print("\nRequesting the list of analog inputs...")
    analogs = session.analogin_list()['array']
    for item in analogs:
        print(f"[Nome oggetto]: {item['name']}, id: {item['act_id']}, valore: {item['value']}{item['unit']}")

    # All the buttons
    #print("\nRequesting the list of digital inputs...")
    #print(session.digitalin_list())

    print("\nRequesting the list of timers...")
    timers = session.timers_list()['array']
    for timer in timers:
        print(f"[Nome timer]: {timer['name']}, id: {timer['id']}, abilitato: {timer['enabled']}, giorni: {timer['days']}")
        for time in timer['timetable']:
            print(f"\t[INIZIO]: {time['start']['hour']}:{time['start']['min']}:{time['start']['sec']}")
            print(f"\t[FINE]: {time['stop']['hour']}:{time['stop']['min']}:{time['stop']['sec']}")
            print(f"\t\tAbilitato: {time['active']}")


    print("\nRequesting the list of thermos...")
    floors = session.thermos_list()['array']
    for floor in floors:
        print(f"[Nome Piano]: {floor['name']}")
        for room in floor['array']:
            print(f"\t[Nome Stanza]: {room['name']}, stato: {room['status']}, temp: {str(room['temp'])[:-1]}.{str(room['temp'])[-1::]}° C, id: {room['act_id']}")
    

    print("\nRequesting the list of terminals...")
    print(session.terminals_list())
    print("\nRequesting the list of tvcc...")
    print(session.tvcc_list())

    #print("\nSpegnimento luce con id=33...")
    #session.light_switch(33, False)

    #print("\nRequesting an update...")
    #print(session.update_request())


