import mido
import mingus.core.chords as chords  
from PyQt6.QtWidgets import QApplication
import sys
from UI import MainWindow
from PyQt6.QtCore import QThread, pyqtSignal

class MidiInputThread(QThread):
    midi_message_received_on = pyqtSignal(int)
    midi_message_received_off = pyqtSignal(int)

    def __init__(self, input_port_name):
        super().__init__()
        self.input_port_name = input_port_name
        self.running = True
        self.notes = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}

    def run(self):
        #open the input port
        print("Opening port...")
        with mido.open_input(self.input_port_name) as inport:
            while self.running:
                for msg in inport:
                    if msg.type == "note_on":
                        # print(f"{''.join(f'{self.notes[msg.note % 12]}{msg.note // 12 - 1}')}  {msg.note}")
                        self.midi_message_received_on.emit(msg.note)
                    elif msg.type == "note_off":
                        self.midi_message_received_off.emit(msg.note)

    def stop(self):
        self.running = False
        self.quit()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    input_port_name = mido.get_input_names()[0]
    midi_thread = MidiInputThread(input_port_name)
    midi_thread.midi_message_received_on.connect(window.draw_pressed_keys)
    midi_thread.midi_message_received_off.connect(window.draw_released_key)

    midi_thread.start()

    try:
        sys.exit(app.exec())
    finally:
        midi_thread.stop()

if __name__ == '__main__':
    main()