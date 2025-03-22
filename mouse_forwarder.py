import serial
import time
from pynput.mouse import Controller, Listener

# Configure serial communication
SERIAL_PORT = '/dev/serial0'  # Primary UART port
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

# Mouse listener functions
def on_move(x, y):
    data = f"move:{x},{y}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")

def on_click(x, y, button, pressed):
    action = "pressed" if pressed else "released"
    data = f"click:{button},{action},{x},{y}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")

def on_scroll(x, y, dx, dy):
    data = f"scroll:{dx},{dy},{x},{y}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")

# Start listening for mouse events
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
