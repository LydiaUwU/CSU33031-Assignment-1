# Device types as clases
# Author: Lydia MacBride

# Device class
# Parameters
# - dev_type: Type of device (1x: sensor, 2x: actuator)
# - dev_id: Numeric identifier of sensor
# - dev_address: IP address of sensor
# - dev_value: Devices value (i.e. temperature)
class Device:
    # Constructor
    def __init__(self, dev_type, dev_id, dev_address):
        self.dev_type = dev_type
        self.dev_id = dev_id
        self.dev_address = dev_address
        self.dev_subs = list()  # Only used by client devices
        self.dev_value = None

    def update(self, dev_value):
        self.dev_value = dev_value

    def get_dev_type(self):
        return self.get_dev_id()

    def get_dev_id(self):
        return self.dev_id

    pass


