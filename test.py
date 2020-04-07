import sys
from __init__ import RequestError, UnauthorizedLogin, ServerNotFound, Domo, CommandNotFound


def print_relays(session):
    print("\nRequesting the list of relays...")
    relays = {}
    try:
        relays = session.list_request(Domo.available_commands['relays'])['array']
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        for index, relay in enumerate(relays, start=1):
            print(f"[Relay {index}] {relay['name']}, id: {relay['act_id']}, status: {relay['status']}")

def print_users(session):
    print("\nRequesting the list of users...")
    users = {}
    try:
        users = session.list_request(Domo.available_commands['users'])['sl_users_list']
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        for index, user in enumerate(users, start=1):
            print(f"[Utente {index}] {user['name']}")

def print_features(session):
    print("\nRequesting the list of features...")
    features = {}
    try:
        features = session.list_request(Domo.available_commands['features'])
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        print(features)
        #for index, feature in enumerate(features, start=1):
        #    print(f"[Feature {index}] {feature}")

def print_map(session):
    print("\nRequesting the list of map elements...")
    print(session.list_request(Domo.available_commands['map']))

def print_lights(session):
    print("\nRequesting the list of lights...")
    floors = {}
    try:
        floors = session.list_request(Domo.available_commands['lights'])['array']
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        for floor in floors:
            print(f"[Nome Piano]: {floor['name']}, stato: {floor['status']}")
            for room in floor['array']:
                print(f"\t[Nome Stanza]: {room['name']}, stato: {room['status']}")
                for item in room['array']:
                    print(f"\t\t[Nome Oggetto]: {item['name']}, stato: {item['status']}, id: {item['act_id']}")

def print_analogin(session):
    print("\nRequesting the list of analog inputs...")
    analogs = {}
    try:
        analogs = session.list_request(Domo.available_commands['analogin'])['array']
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        for item in analogs:
            print(f"[Nome oggetto]: {item['name']}, id: {item['act_id']}, valore: {item['value']}{item['unit']}")

def print_digitalin(session):
    print("\nRequesting the list of digital inputs...")
    print(session.list_request(Domo.available_commands['digitalin']))

def print_timers(session):  
    print("\nRequesting the list of timers...")
    timers = {}
    try:
        timers = session.list_request(Domo.available_commands['timers'])['array']
    except:
        print("The server cannot soddisfy this request")
    else:
        for timer in timers:
            print(f"[Nome timer]: {timer['name']}, id: {timer['id']}, abilitato: {timer['enabled']}, giorni: {timer['days']}")
            for time in timer['timetable']:
                print(f"\t[INIZIO]: {time['start']['hour']}:{time['start']['min']}:{time['start']['sec']}")
                print(f"\t[FINE]: {time['stop']['hour']}:{time['stop']['min']}:{time['stop']['sec']}")
                print(f"\t\tAbilitato: {time['active']}")

def print_thermos(session):  
    print("\nRequesting the list of thermos...")
    floors = {}
    try:
        floors = session.list_request(Domo.available_commands['thermoregulation'])['array']
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        print(floors)
        for floor in floors:
            print(f"\t[Nome Zona]: {floor['name']}, stato: {floor['status']}, temp: {str(floor['temp'])[:-1]}.{str(floor['temp'])[-1::]}° C, id: {floor['act_id']}")
    
def print_tvcc(session): 
    print("\nRequesting the list of tvcc...")
    cameras = {}
    try:
        cameras = session.list_request(Domo.available_commands['tvcc'])['array']
    except RequestError:
        print("The server cannot soddisfy this request")
    else:
        for index, camera in enumerate(cameras, start=1):
            print(f"[Camera {index}] {camera['name']}, uri: {camera['uri']}")

def print_update(session):
    print("\nRequesting an update...")
    print(session.list_request(Domo.available_commands['update']))

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
        #username = input("Inserire il nome utente: ")
        #password = input("Inserire la password: ")
        username = "utente2"
        password = "utente2"
        session.login(username, password)
    except UnauthorizedLogin:
        print("Wrong username/password combination!")
        sys.exit(-1)

    # Print the session id
    print(f"You are now logged in! ID: {session.id}")

    # Main body
    while True:
        choice = input(f'\nWhat do you want to do next?\n1: "List of lights", \n2: "List of thermos",\n3: "List of users",\n4: "List of tvcc cameras",\n5: "Map",\n6: "List of analog input",\n7: "List of digital input",\n8: "List of timers",\n9: "List of relays",\n10: "List of features",\n11: "Turn on/off light by name",\n12: "Turn on/off light by id"\n13: "Activate relays"\n14: "Update"\n15: "Exit"\n - ')
        choice = int(choice)
        if choice == 1:
            print_lights(session)
        elif choice == 2:
            print_thermos(session)
        elif choice == 3:
            print_users(session)
        elif choice == 4: 
            print_tvcc(session)
        elif choice == 5:
            print_map(session)
        elif choice == 6:
            print_analogin(session)
        elif choice == 7:
            print_digitalin(session)
        elif choice == 8:
            print_timers(session)
        elif choice == 9:
            print_relays(session)
        elif choice == 10: 
            print_features(session)
        elif choice == 11: 
            piano = input("Inserisci il nome del piano: ")
            stanza = input("Inserisci il nome della stanza: ")
            luce = input("Inserisci il nome della luce: ")
            on = input("Vuoi accenderla (1) o spegnerla (0)? ")
            print(f"Piano scelto: {piano}, Stanza scelta: {stanza}, Luce scelta: {luce}, accenderla: {on}")
            value = True if on == "1" else False
            id = session.get_id_from_name(piano, stanza, luce)
            if id == -1:
                print("Luce non esistente!")
                continue
            else:
                print(session.switch(id, status=value, is_light=True))
        elif choice == 12: 
            id = input("Inserisci l'id della luce: ")
            on = input("Vuoi accenderla (1) o spegnerla (0)? ")
            value = True if on == "1" else False
            print(session.switch(int(id), status=value, is_light=True))
        elif choice == 13:
            id = input("Inserisci l'id del relay: ")
            on = input("Vuoi attivarlo (1) o disattivarlo (0)? ")
            value = True if on == "1" else False
            print(session.switch(int(id), status=value, is_light=False))
        elif choice == 14: 
            print_update(session)
        elif choice == 15: 
            sys.exit(0)

