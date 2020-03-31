
class Thermo():

    def __init__(self, thermo_json: dict):
        """ 
        From a json dictionary return a Light object representing a light identity

        :param act_id: unique identifier identifying the light
        :param name: non unique name of the light
        :param floor_ind: index of the floor containing the light
        :param room_ind: index of the room containing the light
        :param status: status of the light (on=1/off=0)
        :param temp: temperature of the sensor in the room, in Celsius
        :param mode: Don't know yet (always true)
        :param set_point: if the temp goes below or up this point, then the system automatically turn on the heater
        :param thermo_algo: dictionary representing the algorithm with which the system start up the heater
        :param season: season set by the user (winter, summer or turned off)
        :param leaf: Don't know yet (always true) (maybe if it is a leaf item in a tree likestructure)
        """
        self.act_id = thermo_json['act_id']
        self.name = thermo_json['name']
        self.floor_ind = thermo_json['floor_ind']
        self.room_ind = thermo_json['room_ind']
        self.status = thermo_json['status']
        self.temp = float(thermo_json['temp']) / 10.0
        self.mode = thermo_json['mode']
        self.set_point = float(thermo_json['set_point']) / 10.0
        self.thermo_algo = thermo_json['thermo_algo']
        self.season = thermo_json['season']
        self.leaf = thermo_json['leaf']

class Light():
    
    def __init__(self, light_json: dict):
        """ 
        From a json dictionary return a Light object representing a light identity

        :param act_id: unique identifier identifying the light
        :param name: non unique name of the light
        :param floor_ind: index of the floor containing the light
        :param room_ind: index of the room containing the light
        :param status: status of the light (on=1/off=0)
        :param type: type of light (STEP_STEP, ...)
        :param leaf: Don't know yet (always true)
        """
        self.act_id = light_json['act_id']
        self.name = light_json['name']
        self.floor_ind = light_json['floor_ind']
        self.room_ind = light_json['room_ind']
        self.status = light_json['status']
        self.type = light_json['type']
        self.leaf = light_json['leaf']