#!/bin/bash
# Elktron SO-101 — Setup Script
# Works on: Mac (MPS), Linux (CUDA), Raspberry Pi 5
# Usage: chmod +x install.sh && ./install.sh

set -e

echo "=== Elktron SO-101 — LeRobot Setup ==="

# 1. Create venv
echo "[1/4] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 2. Install LeRobot from source (recommended for latest SO-101 support)
echo "[2/4] Installing LeRobot from source..."
pip install --upgrade pip
pip install git+https://github.com/huggingface/lerobot.git

# 3. Install remaining deps
echo "[3/4] Installing additional dependencies..."
pip install -r requirements.txt

# 4. Verify
echo "[4/4] Verifying installation..."
python3 -c "import lerobot; print(f'LeRobot {lerobot.__version__} installed')"
python3 -c "import torch; print(f'PyTorch {torch.__version__} | CUDA: {torch.cuda.is_available()} | MPS: {torch.backends.mps.is_available()}')"

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Connect both arms via USB-C"
echo "  2. Find ports:  ls /dev/ttyACM*  (Linux/Pi) or  ls /dev/cu.usb*  (Mac)"
echo "  3. Update ports in record.py if needed"
echo "  4. Record demos:  python record.py --task optic_seating --episodes 50"
echo "  5. Train:          python train.py --task optic_seating --device mps"
echo "  6. Deploy:         python deploy.py --task optic_seating"
echo ""
