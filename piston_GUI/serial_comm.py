import serial
import serial.tools.list_ports
import time

import threading
import queue

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_color(c, data):
    print(f"{c}{data}{bcolors.ENDC}")


def get_all_ports():
    ports = serial.tools.list_ports.comports()
    
    port_list = []
    for port, desc, hwid in sorted(ports):
        port_list.append(port)
        print("{}: {} [{}]".format(port, desc, hwid))
    return port_list

class MySerial(threading.Thread):
    ser = serial.Serial()
    ser.baudrate = 115200
    kill_flag = False

    sending_termination = ""
    reading_termination = ""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        
        self.ser.port = 'COM18'
        self.input_queue = queue.Queue()
        self.kill_flag = False
        
        self.ser.timeout = 1  # Set read timeout to 1 second

    @property
    def sending_termination(self):
        return self._sending_termination
    
    @sending_termination.setter
    def sending_termination(self, value):
        self._sending_termination = value
        print("sending_termination: ", end="")
        print(" ".join(f"{ord(c):02x}" for c in self.sending_termination))

    @property
    def reading_termination(self):
        return self._reading_termination
    
    @reading_termination.setter
    def reading_termination(self, value):
        self._reading_termination = value
        print("reading_termination: ", end="")
        print(" ".join(f"{ord(c):02x}" for c in self.reading_termination))

    def set_port(self, port):
        self.ser.port = port

    def connect(self):
        try:
            self.ser.open()
            print_color(bcolors.OKGREEN, f"{self.ser.port} connected")
        except:
            print_color(bcolors.FAIL, f"{self.ser.port} failed to open")
            
    def disconnect(self):
        try:
            self.ser.close()
            print_color(bcolors.OKGREEN, f"{self.ser.port} disconnected")
        except:
            print_color(bcolors.FAIL, f"{self.ser.port} failed to disconnect")

    def send_serial(self, packet):
        if self.ser.is_open:
            # print(f"{self.ser.port}>>> {packet}")
            print_color(bcolors.OKGREEN, f"{self.ser.port}>>> {packet}")
            self.ser.write((packet + self.sending_termination).encode())
            self.input_queue.put(packet)
        else:
            print_color(bcolors.FAIL, "Serial port is not open")

    def get_data(self):
        if not self.input_queue.empty():
            # print(self.input_queue.qsize())
            return self.input_queue.get()
        else:
            return ""
    
    # use this function inside a loop, not as a thread
    def loop(self):
        if self.ser.is_open:
            if self.ser.in_waiting:
                
                # data_from_serial = self.ser.readline().decode('utf-8')
                # data_from_serial = data_from_serial.strip("\r\n")
                data_from_serial = self.ser.read_until(self.reading_termination.encode()).decode('utf-8').strip(self.reading_termination)
                # print_color(bcolors.OKGREEN, f"{self.ser.port}<<< {data_from_serial}")
                
                self.input_queue.put(data_from_serial)
        else:
            time.sleep(0.1)
            self.connect()

        if self.kill_flag:
            self.ser.close()

    def run(self):
        print("MySerial running")
        while True:
            self.loop()
            time.sleep(0.000001)

            if self.kill_flag:
                break


my_serial = MySerial()


if __name__ == "__main__":
    # print("ports: ", get_all_ports())
    print("asd")

# while True:
#     time.sleep(1)