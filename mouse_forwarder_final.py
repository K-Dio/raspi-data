import serial
from evdev import InputDevice, ecodes

# Replace with the correct event file for your mouse
MOUSE_PATH = "/dev/input/event0"

# Open serial connection to the Pico
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Open the mouse device
mouse = InputDevice(MOUSE_PATH)

# Dictionary to map button codes to their custom names (LB, RB, MB)
button_names = {
    ecodes.BTN_LEFT: "LB",   # Left Button -> LB
    ecodes.BTN_RIGHT: "RB",  # Right Button -> RB
    ecodes.BTN_MIDDLE: "MB", # Middle Button -> MB
}

print("Listening for mouse movements...")

x_move = 0  # Variable to store X movement
y_move = 0  # Variable to store Y movement

for event in mouse.read_loop():
    if event.type == ecodes.EV_REL:  # Relative movement or scroll
        if event.code == ecodes.REL_X:
            x_move = event.value  # Directly set X movement
            ser.write(f"move:{x_move},{y_move}\n".encode())  # Send immediately
            x_move = 0  # Reset X movement after sending
        elif event.code == ecodes.REL_Y:
            y_move = event.value  # Directly set Y movement
            ser.write(f"move:{x_move},{y_move}\n".encode())  # Send immediately
            y_move = 0  # Reset Y movement after sending
        elif event.code == ecodes.REL_WHEEL:  # Vertical scroll
            scroll_direction = "up" if event.value > 0 else "down"
            ser.write(f"scroll:{scroll_direction},{abs(event.value)}\n".encode())
        elif event.code == ecodes.REL_HWHEEL:  # Horizontal scroll (if supported)
            scroll_direction = "left" if event.value > 0 else "right"
            ser.write(f"scroll:{scroll_direction},{abs(event.value)}\n".encode())
    
    elif event.type == ecodes.EV_KEY:  # Button press
        if event.code in button_names:  # Check if the event code is a recognized button
            button_name = button_names[event.code]
            state = "pressed" if event.value else "released"
            ser.write(f"click:{button_name},{state}\n".encode())
