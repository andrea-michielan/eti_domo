import requests
import sys

class RequestError(Exception):
    """ Raised when a user send an invalid request to the server """
    pass

class ServerNotFound(Exception):
    """ Raised when the specified host is not available """
    pass

class CommandNotFound(Exception):
    """ Raised if the user tries to send a command to the server that does not exists """
    pass

class Domo:

    # Header for every http request made to the server
    header = {
        "Content-Type": "application/x-www-form-urlencoded", 
        "Connection": "Keep-Alive"
    }

    # Dictionary of available commands
    available_commands = {
        "update": "status_update_req",
        "relays": "relays_list_req",
        "cameras": "tvcc_cameras_list_req",
        "timers": "timers_list_req",
        "thermoregulation": "thermo_list_req",
        "analogin": "analogin_list_req",
        "digitalin": "digitalin_list_req",
        "lights": "nested_light_list_req",
        "features": "feature_list_req",
        "users": "sl_users_list_req",
        "maps": "map_descr_req"
    }

    # Dictionary of seasons available
    seasons = {
        "off": "plant_off",
        "winter": "winter",
        "summer": "summer"
    }

    # Dictionary of thermo zone status
    thermo_status = {
        0: "off",
        1: "man",
        2: "auto",
        3: "jolly"
    }

    def __init__(self, host: str):
        """ 
        Instantiate a new :class:`Object` of type :class:`Domo` that communicates with an Eti/Domo server at the specified ip address

        :param host: A string representing the ip address of the Eti/Domo server
        :raises :class:`ServerNotFound`: if the :param:`host` is not available
        """

        # Wrap the host ip in a http url
        self._host = "http://" + host + "/domo/"
        # The sequence start from 1
        self._cseq = 1
        # Session id for the client
        self.id = ""

        # List of items managed by the server
        self.items = {}

        # Check if the host is available
        response = requests.get(self._host, headers=self.header)

        # If not then raise an exception
        if not response.status_code == 200:
            self._host = ""
            raise ServerNotFound

    def login(self, username: str, password: str):
        """
        Method that takes in the username and password and attempt a login to the server.
        If the login is correct, then the ``id`` parameter of the object :class:`Domo` will be set to the session id given by the server.

        :param username: username of the user
        :param password: password of the user
        :return: ``<None>``
        """

        # Create the login request
        login_parameters = 'command={"sl_cmd":"sl_registration_req","sl_login":"' + str(username) + '","sl_pwd":"' + str(password) + '"}'

        # Send the post request with the login parameters
        response = requests.post(self._host, params=login_parameters, headers=self.header)

        # Set the client id for the session
        self.id = response.json()['sl_client_id']

        # Check if the user is authorized
        if not response.json()['sl_data_ack_reason'] == 0:
            return False

        return True

    def keep_alive(self):

        parameters = 'command={"sl_client_id":"' + self.id + '","sl_cmd":"sl_keep_alive_req"}'

        # Send the post request with the login parameters
        response = requests.post(self._host, params=parameters, headers=self.header)

        return response.json()['sl_data_ack_reason'] == 0

    def update_lists(self):
        """ 
        Function that update the items dictionary containing all the items managed by the eti/domo server 
        """

        # Get a list of available features for the user
        features_list = self.list_request(self.available_commands['features'])['list']
        # Populate the items dictionary containing every item of the server
        for feature in features_list:
            # Get the json response from the server
            tmp_list = self.list_request(self.available_commands[feature])
            # Parse the json into a more readable and useful structure
            self.items[feature] = tmp_list


    def list_request(self, cmd_name):
        """ 
        Method that send the server a request and retrieve a list of items identified by the :param:`cmd_name` parameter
        
        :return: a json dictionary representing the response of the server
        :raises RequestError: if the request is invalid
        :raises CommandNotFound: if the command requested does not exists
        """

        # Check if the command exists
        if not cmd_name in self.available_commands.values():
            raise CommandNotFound

        # If the user requested the map, then we don't need to pass the client id
        client_id = '' if cmd_name == "map_descr_req" else '"client":"' + self.id + '",'

        # If the user requested a list of users, then the parameters are different
        sl_cmd = '"sl_cmd":"sl_users_list_req"' if cmd_name == "sl_users_list_req" else '"sl_cmd":"sl_data_req"'
        sl_appl_msg =   ('"sl_appl_msg":{' 
                            '' + client_id + ''
                            '"cmd_name":"' + cmd_name + '",'
                            '"cseq":' + str(self._cseq) + ''
                        '},'
                        '"sl_appl_msg_type":"domo",' if not cmd_name == "sl_users_list_req" else ''
                        )

        # Create the requests' parameters
        param = (
                'command={' 
                    '' + sl_appl_msg + ''
                    '"sl_client_id":"' + self.id + '",'
                    '' + sl_cmd + ''
                '}'
                )
        
        # Send the post request
        response = requests.post(self._host, params=param, headers=self.header)

        # Get a json dictionary from the response
        response_json = response.json()

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response_json['sl_data_ack_reason'] == 0:
            raise RequestError

        # Return the json of the response
        return response_json

    def switch(self, act_id: int, status: bool = True, is_light: bool = True) -> dict:
        """ 
        Method to turn on or off a light switch or a relays
        
        :param act_id: id of the light/relay to be turned on or off
        :param status: True if the light/relay is to be turned on, False if off
        :param is_light: True if the item to switch is a light, False if it is a relay
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Check if the user wants the light to be turned on or off
        status = "1" if status else "0"

        # Check if the user want to switch a light or activate a relay
        cmd_name = "light_switch_req" if is_light else "relay_activation_req"

        # Create the requests' parameters
        param = ('command={'
                    '"sl_appl_msg":{'
                        '"act_id":' + str(act_id) + ','
                        '"client":"' + self.id + '",'
                        '"cmd_name":"' + cmd_name + '",'
                        '"cseq":' + str(self._cseq) + ','
                        '"wanted_status":' + status + ''
                    '},'
                    '"sl_appl_msg_type":"domo",'
                    '"sl_client_id":"' + self.id + '",'
                    '"sl_cmd":"sl_data_req"'
                '}')
        
        # Send the post request
        response = requests.post(self._host, params=param, headers=self.header)

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()

    def thermo_mode(self, act_id: int, mode: int, temp: float) -> dict:
        """ 
        Method to change the operational mode of a thermo zone
        
        :param act_id: id of the thermo zone to be configured
        :param mode: 0 Turned off, 1 Manual mode, 2 Auto mode, 3 Jolly mode
        :param temp: Temperature to set
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Check if the mode exists
        if mode not in [0, 1, 2, 3]:
            raise RequestError

        # Transform the temperature from float to int, we need to pass the server
        # an integer value, which is in Celsius, but multiplied by 10
        # we also round the float value to only 1 digits 
        value = int(round(temp * 10, 1))

        # Create the requests' parameters
        param = ('command={'
                    '"sl_appl_msg":{'
                        '"act_id":' + str(act_id) + ','
                        '"client":"' + self.id + '",'
                        '"cmd_name":"thermo_zone_config_req",'
                        '"cseq":' + str(self._cseq) + ','
                        '"extended_infos": 0,'
                        '"mode":' + str(mode) + ','
                        '"set_point":' +  str(value) + ''
                    '},'
                    '"sl_appl_msg_type":"domo",'
                    '"sl_client_id":"' + self.id + '",'
                    '"sl_cmd":"sl_data_req"'
                '}')
        
        # Send the post request
        response = requests.post(self._host, params=param, headers=self.header)

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()

    def change_season(self, season: str) -> dict:
        """ 
        Method that change the season of the entire thermo implant

        :param season: string defining the season, it must be contained into the season dictionary
        :return dict: a dictionary containing the response from the server
        """

        # Check if the season exists
        if season not in ["plant_off", "summer", "winter"]:
            raise RequestError

        # Create the requests' parameters
        param = ('command={'
                    '"sl_appl_msg":{'
                        '"client":"' + self.id + '",'
                        '"cmd_name":"thermo_season_req",'
                        '"cseq":' + str(self._cseq) + ','
                        '"season":"' + season + '"'
                    '},'
                    '"sl_appl_msg_type":"domo",'
                    '"sl_client_id":"' + self.id + '",'
                    '"sl_cmd":"sl_data_req"'
                '}')
        
        # Send the post request
        response = requests.post(self._host, params=param, headers=self.header)

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()
