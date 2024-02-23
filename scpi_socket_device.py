

'''

This script will handle setting and getting the ABSOLUTE MINIMUM parameters required to control the CNT alignment system.
Different oscilloscopes may be used, but which one is used will be abstracted to the main script.

'''

import logging
logging.basicConfig(level=logging.WARNING)		# enable debug messages

import time
import sys

import socket           # required to communicate via scpi

from scpi_device import scpi_device


class scpi_socket_device(scpi_device):
    socket_ip = None                                # fixed ip at the current lab setup, may change.
    socket_port = 3000                              # default port for the OWON devices
    sock = None                                     # placeholder for the not yet existing socket
    device_id = None                                # needs to be added on the children classes

# class methods #########################

    def __init__(self):
        logging.debug("__init__ method was called")

        # creating the socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # what does this mean??
        except socket.error:
            logging.warning("failed to create socket")
            sys.exit();
        logging.debug("socket created")


    def connect(self, ip = None):
        logging.debug("connect method was called")

        if(ip != None):                             # ip is optional, if not given, it means it is already existing as a class definition parameter.
            self.socket_ip = ip

        logging.debug("self.socket_ip:")
        logging.debug(self.socket_ip)

        # connecting to remote:
        try:
            self.sock.connect((self.socket_ip, self.socket_port))  # attention !!! socket takes a TUPLE as input parameter
            self.connected = True  # enable connected flag, used to keep track of connection
        except socket.error:
            logging.warning("Failed to connect to ip " + self.socket_ip)
        else:
            logging.debug("socket connected")
            return self.connected

    def send_command(self, cmd_str):
        logging.debug("send_command method was called")
        logging.debug(cmd_str)
        cmd_str = cmd_str + self.endline
        cmd = cmd_str.encode('utf-8')
        try:
            self.sock.sendall(cmd)
            time.sleep(
                0.2)  # FASTER THAN 0.5 GIVS PROBLEMS WITH SOME COMMANDS !!! # maybe not necessary??? check how to do this async.
        except socket.error:
            logging.error("Socket Failed to send")
            logging.error("QUITTING")
            sys.exit()

    def receive_response(self):
        logging.debug("scpi_socket_device:receive_response() method was called")
        reply = self.sock.recv(4096)  # ATTENTION !!! DATA SIZE IS LIMITED HERE, THIS WON'T WORK WITH BIG WAVEWFORMS !!!
        reply.replace(b'\n', b' ')
        logging.debug(reply)
        reply_str = reply.decode('utf-8')

        return (reply_str)

# MAIN FUNCTION ########################################################

if __name__ == "__main__":
    lab_device = scpi_socket_device()
    lab_device.device_id = "OWON,ODP3063"
    lab_device.connect("192.168.178.107")
    print(lab_device.confirm_device_id())

    time.sleep(1)
