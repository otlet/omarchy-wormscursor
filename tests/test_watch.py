import math

import blank_cursor
import watch


def test_circ_diff_basic():
    assert abs(watch.circ_diff(10, 350)) == 20


def test_circ_diff_zero():
    assert watch.circ_diff(5, 5) == 0


def test_valid_instance():
    assert watch.valid_instance("abc123")
    assert not watch.valid_instance("")
    assert not watch.valid_instance("a/b")
    assert not watch.valid_instance("a\\b")
    assert not watch.valid_instance("a\x00b")


def test_parse_cursorpos():
    text = '{"x":123,"y":456}'
    assert watch.parse_cursorpos(text) == (123, 456)


def test_aim_first_update():
    a = watch.Aim()
    assert a.update(0, 0, 0.0) == 0.0


def test_aim_right():
    a = watch.Aim()
    a.update(0, 0, 0.0)
    deg = a.update(20, 0, 0.016)
    assert abs(watch.circ_diff(deg, 0)) < 1, deg


def test_aim_down_held():
    a = watch.Aim()
    a.update(0, 0, 0.0)
    a.update(20, 0, 0.016)
    deg = a.update(20, 20, 0.032)
    assert 8 < deg < 20, deg
    held = deg
    for i in range(8):
        held = a.update(20, 20, 0.08 + i * 0.05)
    assert abs(watch.circ_diff(held, 45)) < 2, held


def test_aim_idle_freeze():
    a = watch.Aim()
    a.update(0, 0, 0.0)
    a.update(20, 0, 0.016)
    deg = a.update(20, 20, 0.032)
    held = deg
    for i in range(8):
        held = a.update(20, 20, 0.08 + i * 0.05)
    frozen = a.update(20, 20, 1.0)
    assert abs(watch.circ_diff(frozen, held)) < 0.01, frozen
    for i in range(watch.IDLE_RESET + 5):
        frozen = a.update(20, 20, 1.1 + i * 0.016)
    assert abs(watch.circ_diff(frozen, held)) < 0.01, frozen


def test_check_runs():
    watch.check()


def test_blank_cursor_is_transparent_xcursor():
    assert blank_cursor.BLOB[:4] == b"Xcur"
    assert len(blank_cursor.BLOB) == 68
    assert "text" in blank_cursor.NAMES
    assert "pointer" in blank_cursor.NAMES


def test_wrap():
    a = watch.Aim()
    a.prev = (0.0, 0.0)
    a.t = 0.0
    a.disp = 10.0
    a.target = 10.0
    a.sx = math.cos(math.radians(10))
    a.sy = math.sin(math.radians(10))
    ang = math.radians(350)
    deg = a.update(math.cos(ang) * 20, math.sin(ang) * 20, 0.016)
    assert deg > 350 or deg < 10, deg
