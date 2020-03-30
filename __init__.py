import requests
import sys

# Header for every http request made to the server
header = {
    "Content-Type": "application/x-www-form-urlencoded", 
    "Connection": "Keep-Alive"
}

class UnauthorizedLogin(Exception):
    """
    Raised when a user try to login with wrong username/password combination
    """
    pass

class RequestError(Exception):
    """
    Raised when a user send an invalid request to the server
    """
    pass

class Domo:

    def __init__(self, host: str = "http://192.168.1.251/domo/"):
        """ 
        Instantiate a new :class:`Object` of type :class:`Domo` that communicates with an Eti/Domo server at the specified ip address

        :param host: A string representing the ip address of the Eti/Domo server
        """

        self.host = "http://" + host + "/domo/"
        self.cseq = 1
        self.id = ""

    def login(self, username: str, password: str) -> None:
        """
        Method that takes in the username and password and attempt a login to the server.
        If the login is correct, then the ``id`` parameter of the object :class:`Domo` will be set to the session id given by the server.

        :param username: username of the user
        :param password: password of the user
        :return: ``<None>``
        :raises UnauthorizedLogin: if the combination of username and password is incorrect.
        """

        # Create the login request
        login_parameters = 'command={"sl_cmd":"sl_registration_req","sl_login":"' + str(username) + '","sl_pwd":"' + str(password) + '"}'

        # Send the post request with the login parameters
        response = requests.post(self.host, params=login_parameters, headers=header)

        # Set the client id for the session
        self.id = response.json()['sl_client_id']

        # Check if the user is authorized
        if not response.json()['sl_data_ack_reason'] == 0:
            raise UnauthorizedLogin

    def update_request(self) -> dict:
        """ 
        Method that send the server an update request, usually sent after every action (such as turning on a light).
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"status_update_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def relays_list(self) -> dict:
        """ 
        Get a json list of all the relays controlled by the Eti/Domo.

        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"relays_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def tvcc_list(self) -> dict:
        """ 
        Get a json list of all the tvcc cameras controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"tvcc_cameras_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def timers_list(self) -> dict:
        """ 
        Get a json list of all the timers controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"timers_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def thermos_list(self) -> dict:
        """ 
        Get a json list of all the thermos zone and sensors controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"nested_thermo_list_req","cseq":' + str(self.cseq) + ',"extended_infos":2,"topologic_scope":"plant","value":0},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def analogin_list(self) -> dict:
        """ 
        Get a json list of all the analog input devices (such as hygrometer) controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"analogin_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def digitalin_list(self) -> dict:
        """ 
        Get a json list of all the digital input devices (such as the lights' buttons) controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"digitalin_list_req","cseq":' + str(self.cseq) + ',"filter":1023},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def terminals_list(self) -> dict:
        """ 
        Get a json list of all of terminals group (don't kwow what that is) controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"terminals_group_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def lights_list(self) -> dict:
        """ 
        Get a json list of all of the lights controlled by the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"nested_light_list_req","cseq":' + str(self.cseq) + ',"topologic_scope":"plant","value":0},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()['array']

    def users_list(self) -> dict:
        """ 
        Get a json list of users registered on the server Eti/Domo.
        ``Note``: this is the only request that does not send and receive any cseq.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_client_id":"' + self.id + '","sl_cmd":"sl_users_list_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        #self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def get_map(self) -> dict:
        """ 
        Get a json list of all the maps save in the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"cmd_name":"map_descr_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def get_features(self) -> dict:
        """ 
        Get a json list of features available with the Eti/Domo.
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"client":"' + self.id + '","cmd_name":"feature_list_req","cseq":' + str(self.cseq) + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()

    def light_switch(self, act_id: int, on: bool = True) -> dict:
        """ 
        Get a json list of all of terminals group (don't kwow what that is) controlled by the Eti/Domo.
        
        :param act_id: id of the light to be turned on or off
        :param on: True if the light is to be turned on, False if off
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Check if the user wants the light to be turned on or off
        status = "1" if on else "0"

        # Create the requests' parameters
        param = 'command={"sl_appl_msg":{"act_id":' + str(act_id) + ',"client":"' + self.id + '","cmd_name":"light_switch_req","cseq":' + str(self.cseq) + ',"wanted_status":' + status + '},"sl_appl_msg_type":"domo","sl_client_id":"' + self.id + '","sl_cmd":"sl_data_req"}'
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response.json()


if __name__ == "__main__":

    # Create a new session with the specified host
    session = Domo()

    # Login to the server
    try:
        session.login("gigi", "toni")
    except UnauthorizedLogin:
        print("Wrong username/password combo!")
        sys.exit(-1)

    # Print the session id
    print(f"You are now logged in! ID: {session.id}")

    
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


