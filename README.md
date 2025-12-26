# Equibop PTT Workaround

This is a Python script that provides a reliable **Push-to-Talk (PTT)** solution for [Equibop](https://github.com/Equibop/Equibop) (a [Vesktop](https://github.com/Vencord/Vesktop) fork) on Linux, specifically designed to bypass limitations on **Wayland**.

## Why?

On Linux, especially under Wayland, global hotkeys in Electron applications (like Discord, Vesktop, and Equibop) are often unreliable or completely non-functional when the application is not in focus. This makes using Push-to-Talk difficult while gaming or working in other windows.

This tool solves that by interacting directly with the Linux input subsystem (`evdev`) to detect key presses globally, regardless of window focus, and triggers the microphone toggle in Equibop.

## Features

- **Global Key Detection**: Works anywhere, even in Wayland sessions.
- **Low Latency**: Directly reads input events.
- **Minimal Resource Usage**: Idle CPU usage is negligible (0%).
- **Configurable**: Choose your input device and key.

## Prerequisites

- Linux OS
- Python 3
- User permissions to access `/dev/input/` (usually requires `root` or being in the `input` group)
- [Equibop](https://github.com/Equibop/Equibop) installed and runnable via the `equibop` command.

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/yourusername/equibop-ptt.git
    cd equibop-ptt
    ```

2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to use a virtual environment or `pip3` depending on your distro)*

## Usage

1.  **List available input devices**:
    Find the name of your keyboard or input device.
    ```bash
    sudo python3 equibop_ptt.py --list-devices
    ```

2.  **Run the script**:
    Replace `"Keychron"` with a substring that matches your device name.
    ```bash
    sudo python3 equibop_ptt.py --device "Keychron" --key "KEY_F16"
    ```
    *Note: `sudo` is often required to read `/dev/input/` unless you have configured udev rules for your user.*

3.  **Command Line Arguments**:
    - `--device`: Substring to match the input device name (default: "keyboard").
    - `--key`: The key code to listen for (default: "KEY_F16"). See `evdev` docs for key names.
    - `--verbose`: Enable debug logging.

## License

MIT License. See [LICENSE](LICENSE) for details.
