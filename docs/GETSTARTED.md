# Domo object
In order to communicate with the eti/domo server you will first need to instantiate a *Domo* object.
This object has just one parameter: the IP address of the eti/domo:
```python
try:
    hub = Domo('192.168.1.250')
except ServerNotFound:
    print('Wrong IP address!')
```
If the eti/domo is not found at the specified IP address, then a `ServerNotFound` exception will be raised.
# Login
You will then need to login with your personal eti/domo credentials using the *login* method:
```python
if not hub.login('username', 'password'):
    print('Wrong credentials, try again!')
```
The login method will return `True` if the user is authenticated, `False` otherwise.
# Keep alive
The `keep_alive` method is used to ask the server to keep alive the connection. The method return `True` if the connection is still alive, `False` otherwise:
```python
if not hub.keep_alive():
    print('You need to login again!')
```
# Update lists
The `update_lists` method is used to update the `items` field of the Domo object, this field contains every identity that your eti/domo server is currently managing (lights, switches, thermoregulations, sensors, ...):
```python
hub.update_lists()
for light in hub.items['lights']:
    print(light['name'])
```
In this example we first call the `update_lists` method on our *Domo* object, and then we print out the names of every lights.
# Available objects
We have seen in the previuos example that we can access the `hub.items` dicionary by using for example the key `lights`. Here is a list of available keys (note that your eti/domo server must have these items configured):
* "lights"
* "thermoregulation"
* "timers"
* "maps"
* "relays"
* "analogin"
* "digitalin"
* "tvcc"

If you don't know which of these are available with your server, you can make a request of available features to the server by following [this](/docs/LISTREQUEST.md) link.