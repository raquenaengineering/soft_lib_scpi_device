

'''

The class defined on this file, unifies the common characteristics used on each SCPI serial device
on our context, the power supply and the function generator.


'''

import logging
logging.basicConfig(level=logging.DEBUG)		# enable debug messages

import time
import sys

import serial           # the function generator works with serial port communication (over USB)

class scpi_serial_device():
    serial_port = None          # placeholder for the serial port
    port_name = None          # default port for the ea-ps 2042 power supply
    serial_baudrate = 9600      # default connection speed for
    endline = b"\n"
    device_id = None
    t = 0.1                     # delay between messages, to give time to the devices to reply to requests


    # class methods #########################

    def __init__(self):
        logging.debug("__init__ method was called")

    def serial_connect(self, port_name):  # serial_connect, could also be called simply connect, and
        logging.debug("serial_connect method called")
        logging.debug(port_name)
        logging.debug("port name " + port_name)

        try:  # closing port just in case was already open. (SHOULDN'T BE !!!)
            self.serial_port.close()
            logging.debug("Serial port closed")
            logging.debug(
                "IT SHOULD HAVE BEEN ALWAYS CLOSED, REVIEW CODE!!!")  # even though the port can't be closed, this message is shown. why ???
        except:
            logging.debug("serial port couldn't be closed")
            logging.debug("Wasn't open, as it should always be")

        try:  # try to establish serial connection
            self.serial_port = serial.Serial(  # serial constructor
                port=port_name,
                baudrate=self.serial_baudrate,
                # baudrate = 115200,
                # bytesize=EIGHTBITS,
                # parity=PARITY_NONE,
                # stopbits=STOPBITS_ONE,
                # timeout=None,
                timeout=0,  # whenever there's no dat on the buffer, returns inmediately (spits '\0')
                xonxoff=False,
                rtscts=False,
                write_timeout=None,
                dsrdtr=False,
                inter_byte_timeout=None,
                exclusive=None
            )

        except Exception as e:  # both port open, and somebody else blocking the port are IO errors.
            logging.debug("ERROR OPENING SERIAL PORT")
            #self.on_port_error(e)

        else:  # IN CASE THERE'S NO EXCEPTION (I HOPE)
            logging.debug("SERIAL CONNECTION SUCCESFUL !")
        # self.status_bar.showMessage("Connected")
        # here we should also add going  to the "DISCONNECT" state.

        logging.debug("serial_port.is_open:")
        try:
            logging.debug(self.serial_port.is_open)
        except:
            logging.debug("No serial port object was created")
        else:
            #self.reset()
            logging.debug("done: ")

    def send_command(self,command):  # do I need another thread for this ???
        logging.debug("send_command() method called")
        command_bytes = command.encode('utf-8')
        command_bytes = command_bytes + self.endline
        try:
            self.serial_port.write(command_bytes)
        except:
            logging.debug("Serial sending command failed, exiting")
            sys.exit()


        # logging.debug("send_serial() method called")
        # logging.debug("Send Serial")
        # message_to_send = command.encode("utf-8")  # this should have effect on the serial_thread
        # print("type of message_to_send")
        # print(type(self.message_to_send))
        # print("type of endline")
        # print(type(self.endline))
        # message_to_send = message_to_send + self.endline
        #
        # print("serial_message_to_send")
        # print(message_to_send)

    def receive_response(self):
        logging.debug("receive_response() method called")
        try:
            response = self.serial_port.read(1024)
        except:
            logging.debug("Serial receiving response failed, exiting")
            sys.exit()
        else:
            response_str = response.decode('utf-8')
            return(response_str)

    def get_id(self):
        logging.debug("get_id() method called")
        self.send_command("*idn?")
        time.sleep(0.1)
        id = self.receive_response()
        logging.debug(id)
        return(id)

    def confirm_device_id(self):
        id = self.get_id()
        logging.debug(id)
        ret = None
        logging.debug(id.find(self.device_id))
        if(id.find(self.device_id) != -1):              # instance of the device id found
            ret = True
        else:
            ret = False
        return(ret)

    def reset(self):
        self.send_command("*rst")

# TRIGGER THE SIGNAL A MESSAGE IS SENT --> SO WE CAN GET THE MESSAGE ON THE LOG WINDOW.

# add here action trigger, so it can be catched by main window.

if __name__ == "__main__":
    dev = scpi_serial_device()
    dev.serial_connect("COM11")

    for i in range(1,100):
        dev.send_command()


