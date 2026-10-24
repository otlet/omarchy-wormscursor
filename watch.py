#!/usr/bin/env python3
"""Poll the Hyprland cursor and print x, y, and the slewed aim angle."""

import math
import os
import socket
import sys
import time

AIM_DIST = 8.0
AIM_SMOOTH = 0.5
HYST_DEG = 3.0
TURN_DPS = 720.0
IDLE_RESET = 60


def circ_diff(a, b):
    d = a - b
    return d - 360.0 * math.floor((d + 180.0) / 360.0)


class Aim:
    def __init__(self):
        self.prev = None
        self.accx = 0.0
        self.accy = 0.0
        self.sx = 1.0
        self.sy = 0.0
        self.target = None
        self.disp = 0.0
        self.idle = 0
        self.t = None

    def update(self, x, y, now):
        if self.prev is None:
            self.prev = (x, y)
            self.t = now
            return self.disp
        dx = x - self.prev[0]
        dy = y - self.prev[1]
        self.prev = (x, y)
        dt = now - self.t if self.t is not None else 0.0
        self.t = now
        if dt <= 0:
            dt = 1.0 / 144.0
        if dx == 0 and dy == 0:
            self.idle += 1
            if self.idle >= IDLE_RESET:
                self.accx = 0.0
                self.accy = 0.0
        else:
            self.idle = 0
            self.accx += dx
            self.accy += dy
            dist = math.hypot(self.accx, self.accy)
            if dist >= AIM_DIST:
                nx = self.accx / dist
                ny = self.accy / dist
                self.sx = self.sx * (1 - AIM_SMOOTH) + nx * AIM_SMOOTH
                self.sy = self.sy * (1 - AIM_SMOOTH) + ny * AIM_SMOOTH
                self.accx = 0.0
                self.accy = 0.0
                deg = math.degrees(math.atan2(self.sy, self.sx)) % 360.0
                if self.target is None or abs(circ_diff(deg, self.target)) > HYST_DEG:
                    first = self.target is None
                    self.target = deg
                    if first:
                        self.disp = deg
                        return self.disp
        if self.target is not None:
            diff = circ_diff(self.target, self.disp)
            step = TURN_DPS * dt
            if abs(diff) <= step:
                self.disp = self.target
            else:
                self.disp += math.copysign(step, diff)
            self.disp %= 360.0
        return self.disp


def check():
    right = Aim()
    right.update(0, 0, 0.0)
    deg = right.update(20, 0, 0.016)
    assert abs(circ_diff(deg, 0)) < 1, deg

    down = Aim()
    down.update(0, 0, 0.0)
    down.update(20, 0, 0.016)
    deg = down.update(20, 20, 0.032)
    assert 8 < deg < 20, deg
    held = deg
    for i in range(8):
        held = down.update(20, 20, 0.08 + i * 0.05)
    assert abs(circ_diff(held, 45)) < 2, held
    frozen = down.update(20, 20, 1.0)
    assert abs(circ_diff(frozen, held)) < 0.01, frozen
    for i in range(IDLE_RESET + 5):
        frozen = down.update(20, 20, 1.1 + i * 0.016)
    assert abs(circ_diff(frozen, held)) < 0.01, frozen

    wrap = Aim()
    wrap.prev = (0.0, 0.0)
    wrap.t = 0.0
    wrap.disp = 10.0
    wrap.target = 10.0
    wrap.sx = math.cos(math.radians(10))
    wrap.sy = math.sin(math.radians(10))
    ang = math.radians(350)
    deg = wrap.update(math.cos(ang) * 20, math.sin(ang) * 20, 0.016)
    assert deg > 350 or deg < 10, deg
    print("ok")


def main():
    inst = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", "")
    path = f"/run/user/{os.getuid()}/hypr/{inst}/.socket.sock"
    aim = Aim()
    while True:
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(path)
            sock.sendall(b"j/cursorpos")
            data = b""
            while True:
                chunk = sock.recv(512)
                if not chunk:
                    break
                data += chunk
            sock.close()
            text = data.decode()
            x = int(text.split('"x":', 1)[1].split(",", 1)[0])
            y = int(text.split('"y":', 1)[1].split("}", 1)[0])
            deg = aim.update(x, y, time.monotonic())
            print(f"{x} {y} {deg:.2f}", flush=True)
        except Exception:
            time.sleep(0.5)
            continue
        time.sleep(0.016)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        check()
    else:
        main()
