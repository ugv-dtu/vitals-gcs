#!/bin/bash

PORT=$(ls /dev/serial/by-id/* 2>/dev/null | head -n 1)

if [ -z "$PORT" ]; then
  echo "No Pixhawk serial device found"
  exit 1
fi

python -m MAVProxy.mavproxy \
  --master="$PORT" \
  --baudrate=57600 \
  --out=udp:127.0.0.1:14550 \
  --out=udp:127.0.0.1:14551
