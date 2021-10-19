# Device types as clases
# Author: Lydia MacBride

# Device class
# Parameters
# - dev_type: Type of device (1x: sensor, 2x: actuator)
# - dev_id: Numeric identifier of sensor
# - dev_subbed: Is the client subscribed to this device
# - dev_value: Devices value (i.e. temperature)
# TODO: Name parameter
class Device:
    # Constructor
    def __init__(self, dev_type, dev_id, dev_subbed, dev_value):
        self.dev_type = dev_type
        self.dev_id = dev_id
        self.dev_subbed = dev_subbed
        self.dev_value = dev_value

    def update(self, dev_value):
        self.dev_value = dev_value

    def get_dev_type(self):
        return self.get_dev_id()

    def get_dev_id(self):
        return self.dev_id

    pass


