import serial
from evdev import InputDevice, ecodes

# Replace with the correct event file for your mouse
MOUSE_PATH = "/dev/input/event0"

# Open serial connection to the Pico
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Open the mouse device
mouse = InputDevice(MOUSE_PATH)

print("Listening for mouse movements...")

for event in mouse.read_loop():
    if event.type == ecodes.EV_REL:  # Relative movement
        if event.code == ecodes.REL_X:
            ser.write(f"move_x:{event.value}\n".encode())
        elif event.code == ecodes.REL_Y:
            ser.write(f"move_y:{event.value}\n".encode())
    elif event.type == ecodes.EV_KEY:  # Button press
        if event.code in [ecodes.BTN_LEFT, ecodes.BTN_RIGHT]:
            state = "pressed" if event.value else "released"
            ser.write(f"click:{event.code},{state}\n".encode())
