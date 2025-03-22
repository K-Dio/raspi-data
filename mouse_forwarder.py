import serial
import time
import uinput  # Import the uinput library

# Configure serial communication
SERIAL_PORT = '/dev/ttyUSB0'  # Update this to the correct serial port on your Raspberry Pi
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

# Set up uinput device (mouse)
events = (
    uinput.EV_REL, uinput.REL_X,  # X axis movement
    uinput.EV_REL, uinput.REL_Y,  # Y axis movement
    uinput.EV_KEY, uinput.BTN_LEFT,  # Left click
    uinput.EV_KEY, uinput.BTN_RIGHT,  # Right click
    uinput.EV_KEY, uinput.BTN_MIDDLE,  # Middle click
    uinput.EV_REL, uinput.REL_WHEEL,  # Scroll wheel
)

device = uinput.Device(events)

# Mouse listener functions
def on_move(x, y):
    data = f"move:{x},{y}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")
    device.emit(uinput.REL_X, x)  # Move the mouse on X axis
    device.emit(uinput.REL_Y, y)  # Move the mouse on Y axis

def on_click(x, y, button, pressed):
    action = "pressed" if pressed else "released"
    data = f"click:{button},{action},{x},{y}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")
    if button == 1:  # Left click
        device.emit(uinput.BTN_LEFT, pressed)
    elif button == 2:  # Middle click
        device.emit(uinput.BTN_MIDDLE, pressed)
    elif button == 3:  # Right click
        device.emit(uinput.BTN_RIGHT, pressed)

def on_scroll(x, y, dx, dy):
    scroll_amount = dx + dy
    data = f"scroll:{scroll_amount}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")
    device.emit(uinput.REL_WHEEL, scroll_amount)  # Emit scroll event

# Start listening for mouse events
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
