from pymavlink import mavutil
import time

udp_ip = "127.0.0.1"
udpin = "0.0.0.0"
udp_port = 14550

master = mavutil.mavlink_connection(f"udp:{udp_ip}:{udp_port}")
master.wait_heartbeat()
print("Connected to Pixhawk")

def set_mode(mode):
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )

def get_status():
    """Request and print vehicle status"""
    # Request vehicle attitude
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        1,
        1
    )

    msg = master.recv_match(type=['HEARTBEAT', 'GPS_RAW_INT', 'VFR_HUD', 'ATTITUDE'], blocking=True, timeout=1)
    if msg:
        print(f"Received: {msg.get_type()}")
        print(msg)

while True:
    # set_mode("STABILIZE")
    # print("Flight mode changed to STABILIZE")
    # time.sleep(5)

    # set_mode("GUIDED")
    # print("Flight mode changed to GUIDED")
    get_status()
    time.sleep(1)