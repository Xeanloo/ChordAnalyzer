import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtCore import QSize, Qt, pyqtSlot
import mido

FACTOR = 2
NATKEY_WIDTH = 24 * FACTOR
ACCKEY_WIDTH = 14 * FACTOR
GAP1 = 15 * FACTOR
GAP2 = 13 * FACTOR

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.keys = []
        self.setWindowTitle("PyQt6 Window")
        self.keyboard()
        self.setFixedSize(QSize(50 * NATKEY_WIDTH, 100))
    
    def keyboard(self):
        naturalKeys = []
        accidentalKeys = []
        Notes = ["C", "D", "E", "F", "G", "A", "B"]
        for i in range(50):
            currButton = QPushButton(self)
            currButton.setFixedSize(NATKEY_WIDTH, 100)
            currButton.move(i * NATKEY_WIDTH, 0)
            currButton.setText(Notes[i % 7])
            currButton.setStyleSheet("background-color: white")
            naturalKeys.append(currButton)
            self.keys.append(currButton)
        
        for i in range(7):
            for j in range(2):
                currButton = QPushButton(self)
                currButton.setFixedSize(ACCKEY_WIDTH, 60)
                currButton.move(i * 7 * NATKEY_WIDTH + GAP1 + j * (ACCKEY_WIDTH*2), 0)
                currButton.setStyleSheet("background-color: black")
                accidentalKeys.append(currButton)
                self.keys.insert((i*12) + (j*2) + 1, currButton)
            for j in range(3):
                currButton = QPushButton(self)
                currButton.setFixedSize(ACCKEY_WIDTH, 60)
                currButton.move(i * 7 * (NATKEY_WIDTH) + NATKEY_WIDTH*3 + GAP2 + j * (ACCKEY_WIDTH*2), 0)
                currButton.setStyleSheet("background-color: black")
                accidentalKeys.append(currButton)
                self.keys.insert((i*12) + (j*2) + 6, currButton)

    def draw_pressed_keys(self, note):
        self.keys[note-24].setStyleSheet("background-color: red")
    
    def draw_released_key(self, note):
        #check if note is black or white
        if note % 12 in [1, 3, 6, 8, 10]:
            self.keys[note-24].setStyleSheet("background-color: black")
        else:
            self.keys[note-24].setStyleSheet("background-color: white")   
        