import evdev
import subprocess
import argparse
import sys
import os
from evdev import ecodes

def run_equibop_toggle(verbose=False):
    cmd = ["equibop", "--toggle-mic"]
    
    # Check if running as root
    if os.geteuid() == 0:
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            if verbose: print(f"Root detected. Switching to user '{sudo_user}' for command execution.")
            cmd = ["sudo", "-u", sudo_user] + cmd
        else:
            print("Warning: Running as root but SUDO_USER is not set. 'equibop' might fail or refuse to run.")
            # Optionally add --no-sandbox if you really want to force root, but it's dangerous for Electron.
            # cmd.append("--no-sandbox") 
    
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"Failed to run command {' '.join(cmd)}: {e}")


def list_devices():
    print("Available Input Devices:")
    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            print(f"  {device.path}: {device.name}")
    except PermissionError:
        print("Error: Permission denied accessing input devices.")
        print(f"Try running with 'sudo' or add your user to the 'input' group:")
        print(f"  sudo usermod -aG input {os.environ.get('USER', '$USER')}")
        print("  (You will need to log out and log back in)")
        sys.exit(1)

def find_device(device_name_substring):
    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    except PermissionError:
        print("Error: Permission denied accessing input devices.")
        print(f"Try running with 'sudo' or add your user to the 'input' group:")
        print(f"  sudo usermod -aG input {os.environ.get('USER', '$USER')}")
        print("  (You will need to log out and log back in)")
        sys.exit(1)

    candidates = []
    for d in devices:
        if device_name_substring.lower() in d.name.lower():
            candidates.append(d)
    return candidates

def main():
    parser = argparse.ArgumentParser(description="PTT script for Equibop")
    parser.add_argument("--device", default="keyboard", help="Substring to match device name (default: 'keyboard')")
    parser.add_argument("--key", default="KEY_F16", help="Key to listen for (default: KEY_F16)")
    parser.add_argument("--list-devices", action="store_true", help="List available devices and exit")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    print(f"Searching for device matching: '{args.device}'")
    candidates = find_device(args.device)

    if not candidates:
        print(f"Error: Could not find any device matching '{args.device}'.")
        print("Run with --list-devices to see available choices.")
        sys.exit(1)
    
    device = candidates[0]
    if len(candidates) > 1:
        print(f"Warning: Found multiple devices matching '{args.device}':")
        for d in candidates:
            print(f"  - {d.name} ({d.path})")
        print(f"Using the first one: {device.name}")
    
    print(f"Selected Device: {device.name}")
    print(f"Listening for Key: {args.key}")

    # Resolve key code
    try:
        if args.key.startswith("KEY_"):
            target_key_code = getattr(ecodes, args.key)
        else:
            # Try appending KEY_ if user forgot it
            target_key_code = getattr(ecodes, "KEY_" + args.key.upper())
    except AttributeError:
        print(f"Error: Invalid key name '{args.key}'. Check evdev/ecodes documentation.")
        sys.exit(1)

    print("PTT Ready. Press Ctrl+C to exit.")
    
    # Grab device to ensure we get events (optional, depending on use case. 
    # Usually better NOT to grab if we just want to spy, 
    # but for PTT sometimes we want to suppress the key.
    # The original script didn't grab, so we won't grab here to be safe and non-blocking.)
    
    try:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.code == target_key_code:
                    val = event.value
                    if val == 1: # Key Down
                        if args.verbose: print(f"Key Down ({args.key}) -> Unmuting")
                        run_equibop_toggle(args.verbose)
                    elif val == 0: # Key Up
                        if args.verbose: print(f"Key Up ({args.key}) -> Muting")
                        run_equibop_toggle(args.verbose)
    except KeyboardInterrupt:
        print("\nExiting.")
    except OSError as e:
        print(f"Device error (disconnected?): {e}")

if __name__ == "__main__":
    main()
