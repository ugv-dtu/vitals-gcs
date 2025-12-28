from pymavlink import mavutil

class MAVClient:
    def __init__(self, udp_ip="127.0.0.1", udp_port=14550):
        self.master = mavutil.mavlink_connection(f"udp:{udp_ip}:{udp_port}")
        self.master.wait_heartbeat()
        self.mav = self.master.mav

    def set_mode(self, mode):
        mode_id = self.master.mode_mapping()[mode]
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )

    def request_stream(self):
        self.master.mav.request_data_stream_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            5,
            1
        )

    def read(self):
        return self.master.recv_match(blocking=False)
