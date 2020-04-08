# Came Eti/Domo
An unofficial and self mantained interface to the REST API of a Came eti/domo server.
## Installation
To use this package you can use pip install:
```
pip install eti-domo
```
And then import Domo and the different custom exceptions that will be raised:
```python
from eti_domo import Domo, RequestError, ServerNotFound, CommandNotFound
```

# First step
The first step is to familiarize with the Domo object and its login method at [this](/docs/GETSTARTED.md) link.

# Retrieving info from the server
You can then start to ask the server for some info such as a list of lights, to do so follow [this](/docs/LISTREQUEST.md) link.

# Turning on/off a light/relay
[Here](/docs/SWITCH.md) is a how-to guide for turning on lights.

# Thermoregulation
If you want to jump right into the thermoregulation you can follow [this](/docs/THERMO.md) guide.

# Home Assistant
I'm also developing a Home Assistant custom integration, check this repository for further update.
