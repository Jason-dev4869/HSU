#!/bin/bash
# ──────────────────────────────────────────
# AUTO INSTALL — JetRacer Line Follower
# Chạy: chmod +x install.sh && ./install.sh
# ──────────────────────────────────────────

set -e  # dừng nếu có lỗi

DEVICE=$(uname -m)  # aarch64 = Jetson, x86_64 = PC

echo "=============================="
echo " Detected: $DEVICE"
echo "=============================="

# ---------- 1. ROS setup ----------
echo "[1/5] Setting up ROS repo..."
if ! dpkg -l | grep -q ros-noetic-desktop; then
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" \
        > /etc/apt/sources.list.d/ros-latest.list'
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
    sudo apt-get update
fi

# ---------- 2. APT packages ----------
echo "[2/5] Installing apt packages..."
xargs sudo apt-get install -y < requirements_apt.txt

# ---------- 3. pip packages ----------
echo "[3/5] Installing pip packages..."

if [ "$DEVICE" = "aarch64" ]; then
    echo ">>> Jetson detected: skipping opencv-python (using JetPack build)"
    # Filter out opencv từ requirements
    grep -v "opencv" requirements.txt | pip3 install -r /dev/stdin
else
    echo ">>> PC detected: installing full requirements"
    pip3 install -r requirements.txt
    # Thêm opencv cho PC
    pip3 install opencv-python>=4.5.5.64
fi

# ---------- 4. JetRacer SDK ----------
echo "[4/5] Installing JetRacer SDK..."
if [ ! -d "$HOME/jetracer" ]; then
    git clone https://github.com/waveshare/jetracer.git $HOME/jetracer
    cd $HOME/jetracer && sudo python3 setup.py install
    cd -
fi

# ---------- 5. Catkin workspace ----------
echo "[5/5] Setting up catkin workspace..."
if [ ! -d "$HOME/catkin_ws" ]; then
    mkdir -p $HOME/catkin_ws/src
    cd $HOME/catkin_ws
    catkin init
    catkin build
    echo "source $HOME/catkin_ws/devel/setup.bash" >> ~/.bashrc
fi

echo ""
echo "=============================="
echo " DONE! Kiểm tra I2C:"
echo " sudo i2cdetect -y 1"
echo " (PCA9685 thường ở địa chỉ 0x40)"
echo "=============================="