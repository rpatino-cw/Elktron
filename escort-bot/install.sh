#!/bin/bash
# Elktron Escort Bot — Pi 5 Setup Script
# Run on a fresh Raspberry Pi OS (Bookworm) install
# Usage: chmod +x install.sh && ./install.sh

set -e

echo "=== Elktron Escort Bot — Pi 5 Setup ==="

# 1. System updates
echo "[1/5] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install picamera2 + dependencies (pre-installed on Pi OS, but just in case)
echo "[2/5] Installing camera dependencies..."
sudo apt-get install -y python3-picamera2 python3-libcamera

# 3. Install OpenCV (inference engine — replaces tflite-runtime)
echo "[3/5] Installing OpenCV..."
sudo apt-get install -y python3-opencv

# 4. Install Python deps
echo "[4/5] Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt

# 5. Download MobileNet SSD v2 model (frozen graph + config for OpenCV DNN)
echo "[5/5] Downloading MobileNet SSD model for OpenCV DNN..."
mkdir -p models
MODEL_URL="https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pb"
CONFIG_URL="https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
wget -q "$MODEL_URL" -O models/ssd_mobilenet_v2.pb || echo "[WARN] Model download failed — see README for manual download"
wget -q "$CONFIG_URL" -O models/ssd_mobilenet_v2.pbtxt || echo "[WARN] Config download failed — see README for manual download"

# Create COCO labels file (person = class 0)
cat > models/coco_labels.txt << 'LABELS'
person
bicycle
car
motorcycle
airplane
bus
train
truck
boat
traffic light
fire hydrant
stop sign
parking meter
bench
bird
cat
dog
horse
sheep
cow
elephant
bear
zebra
giraffe
backpack
umbrella
handbag
tie
suitcase
frisbee
skis
snowboard
sports ball
kite
baseball bat
baseball glove
skateboard
surfboard
tennis racket
bottle
wine glass
cup
fork
knife
spoon
bowl
banana
apple
sandwich
orange
broccoli
carrot
hot dog
pizza
donut
cake
chair
couch
potted plant
bed
dining table
toilet
tv
laptop
mouse
remote
keyboard
cell phone
microwave
oven
toaster
sink
refrigerator
book
clock
vase
scissors
teddy bear
hair drier
toothbrush
LABELS

echo ""
echo "=== Setup complete! ==="
echo "Test camera:  libcamera-hello --timeout 5000"
echo "Run bot:      python3 main.py"
echo ""
