import sys
import signal
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from pymavlink import mavutil

from scripts.ui.dashboard import Dashboard
from scripts.controller.gamepad import ControllerReader
from scripts.mavlink.mav_client import MAVClient
from scripts.logger.flight_logger import FlightLogger

def main():
    app = QApplication(sys.argv)

    def handle_sigint(*args):
        QApplication.quit()

    signal.signal(signal.SIGINT, handle_sigint)

    sig_timer = QTimer()
    sig_timer.start(100)
    sig_timer.timeout.connect(lambda: None)

    ui = Dashboard()
    ui.resize(1600, 900)
    ui.show()

    mav = MAVClient()
    mav.request_stream()

    logger = FlightLogger()

    joy = {"lx": 0.0, "ly": 0.0, "rx": 0.0, "ry": 0.0}
    gcs_control_enabled = False
    rc8_raw = None

    controller = ControllerReader()
    app.aboutToQuit.connect(controller.stop)
    controller.updated.connect(
        lambda lx, ly, rx, ry: (
            joy.update({"lx": lx, "ly": ly, "rx": rx, "ry": ry}),
            ui.left_joy.update_stick(lx, ly),
            ui.right_joy.update_stick(rx, ry)
        )
    )

    gps = {"lat": None, "lon": None, "sats": None}
    vfr = {"alt": None, "speed": None}
    ekf = {
        "roll": None,
        "pitch": None,
        "yaw": None,
        "x": None,
        "y": None,
        "z": None,
        "flags": None,
        "vel_var": None,
        "pos_horiz_var": None,
        "pos_vert_var": None,
    }
    flight = {"mode": None, "armed": None}

    def send_manual_control(lx, ly, rx, ry):
        def clamp(v, lo, hi):
            return max(lo, min(hi, v))

        pitch = int(clamp(ry * 1000, -1000, 1000))
        roll = int(clamp(rx * 1000, -1000, 1000))
        throttle = int(clamp((ly + 1) * 500, 0, 1000))
        yaw = int(clamp(lx * 1000, -1000, 1000))
        pitch = -pitch
        mav.mav.manual_control_send(
            mav.master.target_system,
            pitch,
            roll,
            throttle,
            yaw,
            0
        )

    def poll_mav():
        nonlocal gcs_control_enabled, rc8_raw

        while True:
            msg = mav.read()
            if not msg:
                break

            mtype = msg.get_type()

            if mtype == "GPS_RAW_INT":
                gps["lat"] = msg.lat / 1e7
                gps["lon"] = msg.lon / 1e7
                gps["sats"] = msg.satellites_visible

            elif mtype == "VFR_HUD":
                vfr["alt"] = msg.alt
                vfr["speed"] = msg.groundspeed

            elif mtype == "ATTITUDE":
                ekf["roll"] = msg.roll
                ekf["pitch"] = msg.pitch
                ekf["yaw"] = msg.yaw

            elif mtype == "LOCAL_POSITION_NED":
                ekf["x"] = msg.x
                ekf["y"] = msg.y
                ekf["z"] = msg.z

            elif mtype == "EKF_STATUS_REPORT":
                ekf["flags"] = msg.flags
                ekf["vel_var"] = msg.velocity_variance
                ekf["pos_horiz_var"] = msg.pos_horiz_variance
                ekf["pos_vert_var"] = msg.pos_vert_variance

            elif mtype == "HEARTBEAT":
                flight["mode"] = mavutil.mode_string_v10(msg)
                flight["armed"] = bool(
                    msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
                )

            elif mtype == "RC_CHANNELS":
                rc8_raw = msg.chan8_raw

            elif mtype == "STATUSTEXT":
                text = msg.text.decode(errors="ignore").rstrip("\x00") if isinstance(msg.text, bytes) else str(msg.text).rstrip("\x00")
                ui.add_log(text)
                logger.add_error(text)

        if rc8_raw is not None:
            gcs_control_enabled = rc8_raw > 1500

        if gps["lat"] is not None:
            ui.map.update_position(gps["lat"], gps["lon"])

        telem = ""
        if gps["lat"] is not None:
            telem += (
                "GPS:\n"
                f"  Lat: {gps['lat']:.6f}\n"
                f"  Lon: {gps['lon']:.6f}\n"
                f"  Satellites: {gps['sats']}\n\n"
            )
        if vfr["alt"] is not None:
            telem += f"Altitude: {vfr['alt']:.2f} m\n"
            telem += f"Speed: {vfr['speed']:.2f} m/s\n"
        if telem:
            ui.update_telem(telem)

        if gcs_control_enabled:
            send_manual_control(
                joy["lx"],
                joy["ly"],
                joy["rx"],
                joy["ry"]
            )

    def log_tick():
        logger.write({
            "telemetry": {
                "lat": gps["lat"],
                "lon": gps["lon"],
                "satellites": gps["sats"],
                "altitude_gps_m": vfr["alt"],
                "groundspeed_mps": vfr["speed"],
            },
            "flight": {
                "mode": flight["mode"],
                "armed": flight["armed"],
            },
            "ekf": {
                "attitude": {
                    "roll": ekf["roll"],
                    "pitch": ekf["pitch"],
                    "yaw": ekf["yaw"],
                },
                "local_position": {
                    "x": ekf["x"],
                    "y": ekf["y"],
                    "z": ekf["z"],
                },
                "status": {
                    "flags": ekf["flags"],
                    "velocity_variance": ekf["vel_var"],
                    "pos_horiz_variance": ekf["pos_horiz_var"],
                    "pos_vert_variance": ekf["pos_vert_var"],
                }
            }
        })

    mav_timer = QTimer()
    mav_timer.timeout.connect(poll_mav)
    mav_timer.start(50)

    log_timer = QTimer()
    log_timer.timeout.connect(log_tick)
    log_timer.start(1000)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
