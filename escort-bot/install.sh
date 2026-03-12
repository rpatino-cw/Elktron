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

# 3. Install TFLite runtime
echo "[3/5] Installing TFLite runtime..."
pip install --break-system-packages tflite-runtime

# 4. Install Python deps
echo "[4/5] Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt

# 5. Download MobileNet SSD v2 model
echo "[5/5] Downloading TFLite model..."
mkdir -p models
TFLITE_URL="https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip"
wget -q "$TFLITE_URL" -O /tmp/ssd_model.zip
unzip -o /tmp/ssd_model.zip -d models/
mv models/detect.tflite models/ssd_mobilenet_v2.tflite 2>/dev/null || true

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
