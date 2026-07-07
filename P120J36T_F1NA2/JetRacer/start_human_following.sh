#!/bin/bash
# Chay camera/lidar/chassis truoc, doi on dinh hoan toan, roi moi chay follow_node + dashboard.
# Muc dich: tranh CPU burst luc khoi dong dong thoi lam gscam/Argus bi timeout va crash.

set -e

echo "=== [1/2] Khoi dong camera + lidar + chassis ==="
roslaunch human_following 01_sensors.launch &
SENSORS_PID=$!

echo "=== Doi 10 giay cho camera/Argus on dinh hoan toan ==="
sleep 10

echo "=== [2/2] Khoi dong follow_node + dashboard web ==="
roslaunch human_following 02_follow_and_dashboard.launch &
FOLLOW_PID=$!

# Cho ca 2 chay, Ctrl-C se kill ca 2
trap "kill $SENSORS_PID $FOLLOW_PID 2>/dev/null" EXIT
wait
