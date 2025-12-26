#!/bin/bash

# Configuration
SERVICE_NAME="equibop-ptt.service"
TEMPLATE_FILE="equibop-ptt.service.template"
USER_SYSTEMD_DIR="$HOME/.config/systemd/user"

echo "=== Equibop PTT Setup ==="

# Check input group
if ! groups | grep -q "\binput\b"; then
    echo "ERROR: User '$USER' is not in the 'input' group."
    echo "Please run: sudo usermod -aG input $USER"
    echo "Then log out and log back in before running this script again."
    exit 1
fi

# Detect Python path
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "ERROR: python3 not found."
    exit 1
fi

# Get Script Path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_PATH="$SCRIPT_DIR/equibop_ptt.py"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "ERROR: Could not find equibop_ptt.py at $SCRIPT_PATH"
    exit 1
fi

# Interactive Configuration
read -p "Enter Device Name Substring [default: Keychron]: " DEVICE_NAME
DEVICE_NAME=${DEVICE_NAME:-Keychron}

read -p "Enter Key Code [default: KEY_F16]: " KEY_CODE
KEY_CODE=${KEY_CODE:-KEY_F16}

echo "------------------------------------------------"
echo "Configuration:"
echo "  Python: $PYTHON_PATH"
echo "  Script: $SCRIPT_PATH"
echo "  Device: $DEVICE_NAME"
echo "  Key:    $KEY_CODE"
echo "------------------------------------------------"

# Generate Service File
mkdir -p "$USER_SYSTEMD_DIR"
SERVICE_FILE="$USER_SYSTEMD_DIR/$SERVICE_NAME"

sed -e "s|__PYTHON_PATH__|$PYTHON_PATH|g" \
    -e "s|__SCRIPT_PATH__|$SCRIPT_PATH|g" \
    -e "s|__DEVICE_NAME__|$DEVICE_NAME|g" \
    -e "s|__KEY_CODE__|$KEY_CODE|g" \
    "$TEMPLATE_FILE" > "$SERVICE_FILE"

echo "Created service file at: $SERVICE_FILE"

# Reload and Enable
systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"
systemctl --user restart "$SERVICE_NAME"

echo "Success! Service started."
echo "Check status with: systemctl --user status $SERVICE_NAME"
