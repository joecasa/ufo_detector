#!/bin/bash

# Define variables
VENV_DIR="venv"
DEVICE_PATH="/dev/video2"
VIDEO_GROUP="video"

# Update and install necessary packages
echo "Updating system and installing prerequisites..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-opencv v4l-utils

# Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install Python dependencies inside the virtual environment
echo "Installing Python dependencies..."
pip install opencv-python

# Check if the user is in the video group
if groups $(whoami) | grep &>/dev/null "\b${VIDEO_GROUP}\b"; then
    echo "User is already in the ${VIDEO_GROUP} group."
else
    echo "Adding user to ${VIDEO_GROUP} group..."
    sudo usermod -aG $VIDEO_GROUP $(whoami)
    echo "You need to log out and log back in for group changes to take effect."
    NEW_GROUP_ADDED=true
fi

# Check and adjust permissions on the video device
if [ -e "$DEVICE_PATH" ]; then
    echo "Adjusting permissions on ${DEVICE_PATH}..."
    sudo chmod 666 $DEVICE_PATH
else
    echo "Warning: ${DEVICE_PATH} does not exist or is not connected."
fi

# Final instructions
echo "Setup complete."
if [ "$NEW_GROUP_ADDED" == true ]; then
    echo "Please log out and log back in to apply the group changes."
else
    echo "You can now run the Python script."
fi
