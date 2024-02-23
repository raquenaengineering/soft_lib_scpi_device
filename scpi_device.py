


# class for completely generic SCPI device #
# made for the classes scpi_serial_device and scpi_socket device to inherit from it #

import logging
logging.basicConfig(level=logging.DEBUG)		# enable debug messages
import time

class scpi_device():

    t = 0.1                         # delay between messages, to give time to the devices to reply to requests
    device_id = None                # needs to be reimplemented for each specific device
    connected = False
    endline  = '\n'                 # some devices don't require an endline to communicate, some others do, send it always
    separator = "------------------------------------------------------------------------------------------------------"

    def __init__(self):
        logging.debug("scpi_device.__init__() method was called")

    def connect(self):
        logging.debug("scpi_device.connect() method was called")

    def send_command(self,command):  # do I need another thread for this ???
        logging.debug("scpi_device.send_command() method was called")

    def receive_response(self):
        logging.debug("scpi_device.receive_response() method was called")

    def get_id(self):
        logging.debug("scpi_device.get_id() method was called")
        self.send_command("*idn?")
        time.sleep(self.t)
        id = self.receive_response()
        logging.debug("Device ID:")
        logging.debug(id)
        return(id)

    def confirm_device_id(self):
        logging.debug("scpi_device.confirm_device_id() method was called")
        id = self.get_id()
        logging.debug("ID returned from scpi_device.get_id()")
        logging.debug(id)
        logging.debug("ID of the class")
        logging.debug(self.device_id)
        ret = None

        try:
            logging.debug(id.find(self.device_id))
        except:
            logging.warning("Device ID couldn't be read")
        else:
            if(id.find(self.device_id) != -1):              # instance of the device id found
                ret = True
            else:
                ret = False
            return(ret)

    def reset(self):
        self.send_command("*rst")



if __name__ == "__main__":

    dev = scpi_device()
    dev.connect()
    dev.send_command("*rst")
    dev.receive_response()
    dev.get_id()
    dev.confirm_device_id()


