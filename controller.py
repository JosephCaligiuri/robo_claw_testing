import evdev
import serial
import time

def get_controller_values(device, arduino):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_ABS and event.code == 1:
            axis_value = event.value
            # Normalize axis value to range from -100 to 100
            normalized_value = ((axis_value / 32768.0) * 100 + 100) * (127 / 200)


            normalized_value = int(normalized_value)


            
            # Send the normalized value over serial to Arduino
            if normalized_value > 60 and normalized_value < 67:
                normalized_value = 64
            

            arduino.write(bytes(str(normalized_value), 'utf-8'))

            print(f"Axis {event.code}: {normalized_value}")


        elif event.type == evdev.ecodes.EV_KEY:
            print(f"Button {event.code}: {event.value}")

def main():
    # Find the event device path for your controller
    # You can use 'ls /dev/input/' to list input devices and find your controller
    controller_path = '/dev/input/event3'  # Replace X with the appropriate event number
    arduino_port = '/dev/ttyACM0'  # Replace with the correct serial port for your Arduino

    try:
        device = evdev.InputDevice(controller_path)
        print(f"Connected to {device.name}")

        arduino = serial.Serial(port=arduino_port, baudrate=115200, timeout=.1)
        time.sleep(2)  # Allow time for Arduino to initialize

        get_controller_values(device, arduino)

    except FileNotFoundError:
        print(f"Controller not found at {controller_path}")
    except serial.SerialException:
        print(f"Arduino not found at {arduino_port}")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()

if __name__ == "__main__":
    main()
