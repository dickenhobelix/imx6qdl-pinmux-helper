from pinmux_helper_imx6 import mux_description, pin_drive_characteristics


def test_parse_line_smoketest():
    input = "MX6QDL_PAD_CSI0_DAT6__ECSPI1_MISO       0x100b1"
    expected_output_lines = [
        "Pad CSI0_DAT6 is muxed to function ECSPI1_MISO",
        "Pin Drive Characteristics",
        "HYS: True (Schmitt Trigger Input)",
        "PUS: 100k down",
        "PUE: False (Keeper Enabled)",
        "PKE: Pull/Keeper disabled",
        "ODE: False (Open Drain Disabled)",
        "Speed: medium (100, 150 MHz)",
        "DSE: 40 Ohm (25 Ohm @ 3.3V, 40 Ohm @ 1.8V)",
        "SRE: fast",
        "SION: False",
    ]
    output = str(mux_description(input))
    idx = 0
    for line in output.splitlines():
        if line != "":
            assert line == expected_output_lines[idx]
            idx += 1


def test_parse_line_fail_on_invalid_descriptions():
    invalid_lines = [
        "lalala lalala"
        "MX7DL__lala"
        "lala__lalal"
        ""
        " "
        "lala_lalal_lala"
        "MX6QDL_PAD_LALA_LALA"
        "MX6QDL_PAD_LALA__LALA"
        "MX6QDL_PAD_CSI0_DAT6__ECSPI1_MISO "
        "MX6QDL_PAD_CSI0_DAT6__ECSPI1_MISO funky"
    ]
    for line in invalid_lines:
        assert (
            str(mux_description(line))
            == "Pad <unknown> is muxed to function <unknown>\n\nPin Drive Characteristics\n<unknown>"
        )


def test_parse_pinmux_function():
    prefix = "MX6QDL_PAD_"
    pads = ["PAD1", "PAD2", "PAD3"]
    functions = ["func1", "func2", "func3"]
    for pad in pads:
        for function in functions:
            line = f"{prefix}{pad}__{function}  0x123456"

            assert (
                str(mux_description(line)).splitlines()[0]
                == f"Pad {pad} is muxed to function {function}"
            )


def test_parse_pin_drive_characteristics_default_value():
    assert (
        str(pin_drive_characteristics("0x80000000"))
        == "Default settings (bit 31 set - do not change default pinmux)"
    )


def test_parse_pin_drive_characteristics_hytheresis():
    assert "HYS: True (Schmitt Trigger Input)" in str(
        pin_drive_characteristics(hex(1 << 16))
    )
    assert "HYS: True (Schmitt Trigger Input)" in str(
        pin_drive_characteristics(hex(1 << 16 | 0xFFF000))
    )
    assert "HYS: False (CMOS Input)" in str(pin_drive_characteristics(hex(0)))
    assert "HYS: False (CMOS Input)" in str(pin_drive_characteristics(hex(0xFFF0)))


def test_parse_push_pull():
    results = {"100k down": 0, "47k up": 1, "100k up": 2, "22k up": 3}

    for desc in results.keys():
        val = results[desc]
        assert f"PUS: {desc}" in str(pin_drive_characteristics(hex(val << 14)))
        assert f"PUS: {desc}" in str(pin_drive_characteristics(hex(val << 14 | 0xFFF)))


def test_parse_pull_or_keeper_enabled():
    assert "PUE: True (Pull Enabled)" in str(pin_drive_characteristics(hex(1 << 13)))
    assert "PUE: False (Keeper Enabled)" in str(pin_drive_characteristics(hex(0)))


def test_parse_pull_keeper_enable():
    assert "PKE: Pull/Keeper enabled" in str(pin_drive_characteristics(hex(1 << 12)))
    assert "PKE: Pull/Keeper disabled" in str(pin_drive_characteristics(hex(0)))


def test_parse_open_drain_enable():
    assert "ODE: True (Open Drain Enabled)" in str(
        pin_drive_characteristics(hex(1 << 11))
    )
    assert "ODE: False (Open Drain Disabled)" in str(pin_drive_characteristics(hex(0)))


def test_parse_speed():
    results = {
        "low (50 MHz)": 0,
        "medium (100, 150 MHz)": 2,
        "high (100, 150, 200 MHz)": 3,
    }

    for desc in results.keys():
        val = results[desc]
        assert f"Speed: {desc}" in str(pin_drive_characteristics(hex(val << 6)))


def test_parse_dse():
    assert "DSE: disable" in str(pin_drive_characteristics(hex(0 << 3)))
    assert "DSE: 260 Ohm (150 Ohm @ 3.3V, 260 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(1 << 3))
    )
    assert "DSE: 130 Ohm (75 Ohm @ 3.3V, 130 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(2 << 3))
    )
    assert "DSE: 90 Ohm (50 Ohm @ 3.3V, 90 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(3 << 3))
    )
    assert "DSE: 60 Ohm (37 Ohm @ 3.3V, 60 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(4 << 3))
    )
    assert "DSE: 50 Ohm (30 Ohm @ 3.3V, 50 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(5 << 3))
    )
    assert "DSE: 40 Ohm (25 Ohm @ 3.3V, 40 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(6 << 3))
    )
    assert "DSE: 33 Ohm (20 Ohm @ 3.3V, 33 Ohm @ 1.8V)" in str(
        pin_drive_characteristics(hex(7 << 3))
    )


def test_parse_sre():
    assert "SRE: fast" in str(pin_drive_characteristics(hex(1)))
    assert "SRE: slow" in str(pin_drive_characteristics(hex(0)))


def test_parse_sion():
    assert "SION: True" in str(pin_drive_characteristics(hex(1 << 30)))
    assert "SION: False" in str(pin_drive_characteristics(hex(0)))
