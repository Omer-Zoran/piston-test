import sys
import time 
import threading
import serial_comm
import json

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea, QGroupBox, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QMenuBar, QAction, QSlider
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui


class Main_UI(QMainWindow):
    
    def __init__(self):
        super(Main_UI, self).__init__()
        uic.loadUi("piston_test_main_window.ui", self)

        self.slider = self.findChild(QSlider, "slider_1")
        self.slider.sliderReleased.connect(lambda: self.update_piston_time())
        self.slider.setRange(0, 100)
        
        self.slider_precent = self.findChild(QtWidgets.QLabel, "precent_1")
        with open("last_position.json", "r") as f:
            data = json.load(f)
        
        precent = int(data['last position'])
        print(precent)
        self.last_slide_value = int(precent)
        self.slider_precent.setText(f"{precent}")
        self.slider.setValue(precent)
        
        self.full_range_piston_time = 13000 #! time in milliseconds
        self.show()
        
        
    def update_piston_time(self):  
        slide_value = self.slider.value()
        direction, time_to_move = self.calc_move_time(slide_value)
        serial_comm.my_serial.send_serial(f"S{time_to_move},{str(direction)}")
        self.slider_precent.setText(f"{slide_value}%")
        
        data  = {'last position' : int(slide_value)}
        with open("last_position.json", "w") as f:
            json.dump(data, f)
        
    def calc_move_time(self, current_silde_value) -> int:        
        if self.last_slide_value > current_silde_value:
            dir = -1
        elif self.last_slide_value < current_silde_value:
            dir = 1
        else:
            return 
        
        
        precent_diff = abs(current_silde_value - self.last_slide_value)
        time_to_move = int(round((precent_diff / 100) * self.full_range_piston_time))
        
        print(time_to_move , dir)
        
        self.last_slide_value = current_silde_value
        
        return dir, time_to_move
    
def manual_input_listener():
    while True:
        input_data = input('\nplease enter a command:\n')
        print(f"manual input: {input_data}")

        serial_comm.my_serial.send_serial(input_data)
        time.sleep(0.001)

def main():
    app = QtWidgets.QApplication(sys.argv)
    UI_WINDOW = Main_UI()
    sys.exit(app.exec_())



if __name__ == '__main__':
    print("start")
    serial_comm.my_serial.set_port('COM16')
    serial_comm.my_serial.reading_termination = "\n"
    serial_comm.my_serial.sending_termination = "\n"
    serial_comm.my_serial.start()
    
    main()
