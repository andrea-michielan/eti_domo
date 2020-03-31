import requests
import sys

class UnauthorizedLogin(Exception):
    """ Raised when a user try to login with wrong username/password combination """
    pass

class RequestError(Exception):
    """ Raised when a user send an invalid request to the server """
    pass

class ServerNotFound(Exception):
    """ Raised when the specified host is not available """
    pass

class LightNotFound(Exception):
    """ Raised when a light is not available """
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

    def __init__(self, host: str):
        """ 
        Instantiate a new :class:`Object` of type :class:`Domo` that communicates with an Eti/Domo server at the specified ip address

        :param host: A string representing the ip address of the Eti/Domo server
        :raises :class:`ServerNotFound`: if the :param:`host` is not available
        """

        # Wrap the host ip in a http url
        self.host = "http://" + host + "/domo/"
        # The sequence start from 1
        self.cseq = 1
        # Session id for the client
        self.id = ""

        # List of items managed by the server
        self.items = {}

        # Check if the host is available
        response = requests.get(self.host, headers=self.header)

        # If not then raise an exception
        if not response.status_code == 200:
            self.host = ""
            raise ServerNotFound

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
        response = requests.post(self.host, params=login_parameters, headers=self.header)

        # Set the client id for the session
        self.id = response.json()['sl_client_id']

        # Check if the user is authorized
        if not response.json()['sl_data_ack_reason'] == 0:
            raise UnauthorizedLogin

        # If the user has access to the server we make the request for all the items available
        self.udpate_lists()

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
                            '"cseq":' + str(self.cseq) + ''
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
        response = requests.post(self.host, params=param, headers=self.header)

        # Get a json dictionary from the response
        response_json = response.json()

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response_json['sl_data_ack_reason'] == 0:
            print(response_json)
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
                        '"cseq":' + str(self.cseq) + ','
                        '"wanted_status":' + status + ''
                    '},'
                    '"sl_appl_msg_type":"domo",'
                    '"sl_client_id":"' + self.id + '",'
                    '"sl_cmd":"sl_data_req"'
                '}')
        
        # Send the post request
        response = requests.post(self.host, params=param, headers=self.header)

        # Increment the cseq counter
        self.cseq += 1

        # Check if the response is valid
        if not response.json()['sl_data_ack_reason'] == 0:
            raise RequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()

    def get_id_from_name(self, floor_name: str, room_name: str, light: str):
        """
        Return the act_id of the item contained in room contained in floor

        :param floor_name: floor that contains the light
        :param room_name: room inside floor_name that contains the light
        :param light: name of the light
        :return int: act_id of the light
        """

        # Get the list of lights
        floors = self.cmd_request(self.available_commands['lights'])['array']

        # Find the id of the light
        for floor in floors:
            if floor['name'] == floor_name:
                for room in floor['array']:
                    if room['name'] == room_name:
                        for item in room['array']:
                            if item['name'] == light:
                                # Light found!
                                return item['act_id']

        # If the light has not been found raise an exception
        raise LightNotFound


if __name__ == "__main__":
    #ip = input("Inserire l'indirizzo IP del server Eti/Domo: ")
    ip = "192.168.1.251"

    # Create a new session with the specified host
    session = ""
    try:
        session = Domo(ip)
    except:
        print("This server is not available")
        sys.exit(-1)

    # Login to the server
    try:
        username = "utente2"
        password = "utente2"
        session.login(username, password)
    except UnauthorizedLogin:
        print("Wrong username/password combination!")
        sys.exit(-1)

    # Print the session id
    print(f"You are now logged in! ID: {session.id}")
